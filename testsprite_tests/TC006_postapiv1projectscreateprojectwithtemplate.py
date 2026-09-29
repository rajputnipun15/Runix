import requests
import time
import sys

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
TIMEOUT = 30


def test_create_project_with_template_TC006():
    login_url = f"{BASE_URL}{API_PREFIX}/auth/login"
    projects_url = f"{BASE_URL}{API_PREFIX}/projects"

    # Credentials specified in the PRD instructions
    login_payload = {
        "email": "demo@runix.internal",
        "password": "Demopassword123!"
    }

    token = None
    project_id = None

    try:
        # Authenticate to obtain Bearer token
        try:
            r = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Login request failed: {e}")

        assert r is not None, "No response from login endpoint"
        assert r.status_code == 200, f"Expected 200 from login, got {r.status_code}: {r.text}"

        try:
            login_json = r.json()
        except ValueError:
            raise AssertionError(f"Login response not JSON: {r.text}")

        # Extract token with flexible keys
        if isinstance(login_json, dict):
            if "access_token" in login_json:
                token = login_json["access_token"]
            elif "token" in login_json:
                token = login_json["token"]
            elif "data" in login_json and isinstance(login_json["data"], dict) and "access_token" in login_json["data"]:
                token = login_json["data"]["access_token"]
            elif "accessToken" in login_json:
                token = login_json["accessToken"]
            elif "id_token" in login_json:
                token = login_json["id_token"]
        if not token:
            raise AssertionError(f"Unable to extract auth token from login response: {login_json}")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Create a new project with template
        unique_name = f"test-project-{int(time.time())}"
        create_payload = {
            "name": unique_name,
            "template": "react-vite-ts",
            "visibility": "private"
        }

        try:
            r = requests.post(projects_url, json=create_payload, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Project creation request failed: {e}")

        # Expect 201 Created
        assert r is not None, "No response from create project endpoint"
        if r.status_code != 201:
            # include body in message for debugging
            raise AssertionError(f"Expected 201 for project creation, got {r.status_code}: {r.text}")

        try:
            project_json = r.json()
        except ValueError:
            raise AssertionError(f"Create project response not JSON: {r.text}")

        # Extract project id robustly
        if isinstance(project_json, dict):
            if "id" in project_json:
                project_id = project_json["id"]
            elif "project" in project_json and isinstance(project_json["project"], dict) and "id" in project_json["project"]:
                project_id = project_json["project"]["id"]
            elif "data" in project_json and isinstance(project_json["data"], dict) and "id" in project_json["data"]:
                project_id = project_json["data"]["id"]

        assert project_id, f"Project ID not found in response: {project_json}"

        # Validate returned fields
        returned_name = None
        returned_template = None
        returned_visibility = None

        # Try to find fields in common locations
        def _get_field(d, key):
            if not isinstance(d, dict):
                return None
            if key in d:
                return d[key]
            if "project" in d and isinstance(d["project"], dict) and key in d["project"]:
                return d["project"][key]
            if "data" in d and isinstance(d["data"], dict) and key in d["data"]:
                return d["data"][key]
            return None

        returned_name = _get_field(project_json, "name")
        returned_template = _get_field(project_json, "template")
        returned_visibility = _get_field(project_json, "visibility")

        assert returned_name == create_payload["name"], f"Returned name mismatch: expected {create_payload['name']}, got {returned_name}"
        assert returned_template == create_payload["template"], f"Returned template mismatch: expected {create_payload['template']}, got {returned_template}"
        assert returned_visibility == create_payload["visibility"], f"Returned visibility mismatch: expected {create_payload['visibility']}, got {returned_visibility}"

        print(f"Project created successfully: id={project_id}, name={returned_name}, template={returned_template}, visibility={returned_visibility}")

    finally:
        # Clean up: delete the created project if present
        if project_id:
            delete_url = f"{projects_url}/{project_id}"
            try:
                resp = requests.delete(delete_url, headers=headers, timeout=TIMEOUT)
                # Accept 200 or 204 as successful deletion
                if resp.status_code not in (200, 204):
                    print(f"Warning: delete project returned unexpected status {resp.status_code}: {resp.text}")
                else:
                    print(f"Project {project_id} deleted (status {resp.status_code}).")
            except Exception as e:
                print(f"Warning: failed to delete project {project_id}: {e}")


if __name__ == "__main__":
    try:
        test_create_project_with_template_TC006()
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        sys.exit(2)
    else:
        print("TEST PASSED")