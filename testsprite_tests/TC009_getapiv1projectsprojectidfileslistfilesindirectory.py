import requests
import uuid
import sys

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
TIMEOUT = 30.0

def extract_token(resp_json):
    # Common token locations
    if not isinstance(resp_json, dict):
        return None
    for key in ("access_token", "token", "accessToken"):
        if key in resp_json and isinstance(resp_json[key], str):
            return resp_json[key]
    # nested structures
    if "data" in resp_json and isinstance(resp_json["data"], dict):
        for key in ("access_token", "token", "accessToken"):
            if key in resp_json["data"] and isinstance(resp_json["data"][key], str):
                return resp_json["data"][key]
    return None

def extract_project_id(resp_json):
    if not isinstance(resp_json, dict):
        return None
    for key in ("id", "project_id", "projectId"):
        if key in resp_json:
            return resp_json[key]
    if "data" in resp_json and isinstance(resp_json["data"], dict):
        for key in ("id", "project_id", "projectId"):
            if key in resp_json["data"]:
                return resp_json["data"][key]
    return None

def test_getapiv1projectsprojectidfileslistfilesindirectory():
    session = requests.Session()
    token = None
    project_id = None
    created_project = False

    try:
        # 1) Authenticate to obtain Bearer token
        login_url = f"{BASE_URL}{API_PREFIX}/auth/login"
        login_payload = {
            "email": "demo@runix.internal",
            "password": "Demopassword123!"
        }
        try:
            r = session.post(login_url, json=login_payload, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Login request failed: {e}")

        assert r.status_code == 200, f"Login expected 200, got {r.status_code}, body: {r.text}"
        try:
            login_json = r.json()
        except ValueError:
            raise AssertionError(f"Login response is not JSON: {r.text}")

        token = extract_token(login_json)
        assert token, f"Failed to extract token from login response: {login_json}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # 2) Create a new project to ensure a valid project_id (since none provided)
        create_project_url = f"{BASE_URL}{API_PREFIX}/projects"
        unique_name = f"test-project-{uuid.uuid4().hex[:8]}"
        project_payload = {
            "name": unique_name,
            "template": "blank-docker",
            "visibility": "private"
        }
        try:
            r = session.post(create_project_url, json=project_payload, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Create project request failed: {e}")

        assert r.status_code in (200, 201), f"Create project expected 200/201, got {r.status_code}, body: {r.text}"
        try:
            project_json = r.json()
        except ValueError:
            raise AssertionError(f"Create project response is not JSON: {r.text}")

        project_id = extract_project_id(project_json)
        assert project_id, f"Failed to extract project_id from create response: {project_json}"
        created_project = True

        # 3) List files and directories in the project workspace
        list_files_url = f"{BASE_URL}{API_PREFIX}/projects/{project_id}/files"
        try:
            r = session.get(list_files_url, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"List files request failed: {e}")

        assert r.status_code == 200, f"List files expected 200, got {r.status_code}, body: {r.text}"
        content_type = r.headers.get("Content-Type", "")
        assert "application/json" in content_type.lower(), f"Expected JSON response, got Content-Type: {content_type}"

        try:
            files_json = r.json()
        except ValueError:
            raise AssertionError(f"List files response is not JSON: {r.text}")

        # Validate structure: expect either a list of items or a dict representing the tree
        if isinstance(files_json, list):
            # If it's a list, it's acceptable; assert items have at least 'name' or 'type' keys if present
            for item in files_json:
                assert isinstance(item, dict), f"File tree item expected dict, got {type(item)}"
                assert ("name" in item) or ("path" in item) or ("type" in item), f"File item missing expected keys: {item}"
        elif isinstance(files_json, dict):
            # If dict, expect some tree-like keys
            # Accept keys like 'children' or 'files' or top-level 'name'
            assert any(k in files_json for k in ("children", "files", "name")), f"File tree dict missing expected keys: {files_json.keys()}"
        else:
            raise AssertionError(f"Unexpected files response type: {type(files_json)}")

        print("TC009 passed: listed files/directories successfully.")

    finally:
        # Cleanup: delete the created project if possible
        if created_project and project_id:
            delete_url = f"{BASE_URL}{API_PREFIX}/projects/{project_id}"
            try:
                r = session.delete(delete_url, headers=headers, timeout=TIMEOUT)
                # Acceptable delete responses: 200, 202, 204
                if r.status_code not in (200, 202, 204):
                    print(f"Warning: project delete returned unexpected status {r.status_code}, body: {r.text}", file=sys.stderr)
            except requests.RequestException as e:
                print(f"Warning: project delete request failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    test_getapiv1projectsprojectidfileslistfilesindirectory()