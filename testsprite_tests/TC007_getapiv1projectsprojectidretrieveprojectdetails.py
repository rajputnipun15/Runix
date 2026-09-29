import requests
import uuid
import sys

BASE = "http://localhost:8000"
API_BASE = f"{BASE}/api/v1"
TIMEOUT = 30

def _extract_token(json_data):
    if not isinstance(json_data, dict):
        return None
    # Common token fields
    for key in ("access_token", "token", "auth_token"):
        if key in json_data and isinstance(json_data[key], str):
            return json_data[key]
    # Some APIs nest token under data
    data = json_data.get("data") if isinstance(json_data.get("data"), dict) else None
    if data:
        for key in ("access_token", "token", "auth_token"):
            if key in data and isinstance(data[key], str):
                return data[key]
    return None

def _find_project_id(json_data):
    if not isinstance(json_data, dict):
        return None
    # direct id fields
    for key in ("id", "project_id", "uuid"):
        if key in json_data:
            return json_data[key]
    # nested data
    data = json_data.get("data") if isinstance(json_data.get("data"), dict) else None
    if data:
        for key in ("id", "project_id", "uuid"):
            if key in data:
                return data[key]
    return None

def test_getapiv1projectsprojectidretrieveprojectdetails():
    session = requests.Session()
    token = None
    created_project_id = None

    # 1) Authenticate to obtain Bearer token
    login_url = f"{API_BASE}/auth/login"
    login_payload = {
        "email": "demo@runix.internal",
        "password": "Demopassword123!"
    }
    try:
        r = session.post(login_url, json=login_payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"Login request failed: {e}")

    assert r.status_code == 200, f"Expected 200 from login, got {r.status_code}, body: {r.text}"
    try:
        login_json = r.json()
    except ValueError:
        raise AssertionError(f"Login response is not JSON: {r.text}")

    token = _extract_token(login_json)
    assert token, f"Auth token not found in login response: {login_json}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 2) Create a new project to retrieve later
    create_url = f"{API_BASE}/projects"
    project_name = f"test-project-{uuid.uuid4().hex[:8]}"
    create_payload = {
        "name": project_name,
        "template": "blank-docker",
        "visibility": "private"
    }

    try:
        r = session.post(create_url, json=create_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"Create project request failed: {e}")

    assert r.status_code in (200, 201), f"Expected 201 or 200 from project creation, got {r.status_code}, body: {r.text}"
    try:
        project_json = r.json()
    except ValueError:
        raise AssertionError(f"Create project response is not JSON: {r.text}")

    created_project_id = _find_project_id(project_json)
    assert created_project_id, f"Created project id not found in response: {project_json}"

    # Ensure cleanup happens
    try:
        # 3) Retrieve the created project details
        get_url = f"{API_BASE}/projects/{created_project_id}"
        try:
            r = session.get(get_url, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Get project request failed: {e}")

        assert r.status_code == 200, f"Expected 200 when retrieving created project, got {r.status_code}, body: {r.text}"
        try:
            get_json = r.json()
        except ValueError:
            raise AssertionError(f"Get project response is not JSON: {r.text}")

        # Validate returned project contains expected fields
        returned_id = _find_project_id(get_json)
        assert returned_id, f"Project id missing in GET response: {get_json}"
        # Compare ids as strings to be tolerant of numeric vs string ids
        assert str(returned_id) == str(created_project_id), f"Returned project id {returned_id} does not match created id {created_project_id}"
        # Optionally check name if present
        name_in_resp = None
        if isinstance(get_json, dict):
            name_in_resp = get_json.get("name") or (get_json.get("data") or {}).get("name")
        if name_in_resp is not None:
            assert name_in_resp == project_name, f"Project name mismatch: expected {project_name}, got {name_in_resp}"

        # 4) Negative case: request a non-existent project id and expect 404
        non_existent_id = str(uuid.uuid4())
        non_exist_url = f"{API_BASE}/projects/{non_existent_id}"
        try:
            r = session.get(non_exist_url, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Get non-existent project request failed: {e}")

        assert r.status_code == 404, f"Expected 404 for non-existent project id, got {r.status_code}, body: {r.text}"

    finally:
        # 5) Cleanup: delete the created project
        if created_project_id:
            delete_url = f"{API_BASE}/projects/{created_project_id}"
            try:
                r = session.delete(delete_url, headers=headers, timeout=TIMEOUT)
                # Accept 200, 202, 204 as successful deletion responses
                if r.status_code not in (200, 202, 204):
                    # If deletion is not allowed or fails, raise but include response
                    raise AssertionError(f"Failed to delete project {created_project_id}, status {r.status_code}, body: {r.text}")
            except requests.RequestException as e:
                raise AssertionError(f"Delete project request failed: {e}")

if __name__ == "__main__":
    try:
        test_getapiv1projectsprojectidretrieveprojectdetails()
        print("TC007 passed")
    except AssertionError as e:
        print(f"TC007 failed: {e}")
        sys.exit(1)
    except Exception as ex:
        print(f"TC007 encountered an unexpected error: {ex}")
        sys.exit(2)