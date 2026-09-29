import requests
import sys
from typing import Optional

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"
TIMEOUT = 30

PRIMARY_CREDENTIAL = {"email": "demo@runix.internal", "password": "Demopassword123!"}
FALLBACK_CREDENTIAL = {"email": "nipun@gmail.com", "password": "12345678"}


def extract_bearer_token(resp_json: dict) -> Optional[str]:
    # Common token field names
    candidates = [
        "access_token",
        "token",
        "accessToken",
        "auth_token",
        "data.access_token",
        "data.token",
        "data.accessToken",
        "result.access_token",
        "result.token",
    ]
    # flatten nested common paths like "data.token"
    for c in candidates:
        if "." in c:
            top, sub = c.split(".", 1)
            if top in resp_json and isinstance(resp_json[top], dict) and sub in resp_json[top]:
                val = resp_json[top][sub]
                if isinstance(val, str) and val:
                    return val
        else:
            if c in resp_json and isinstance(resp_json[c], str) and resp_json[c]:
                return resp_json[c]
    # fallback: if resp_json has a single string value anywhere, return it (rare)
    for v in resp_json.values():
        if isinstance(v, str) and v:
            return v
    return None


def login_try_credentials(credentials: dict) -> str:
    url = f"{API_BASE}/auth/login"
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=credentials, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"Login request failed for {credentials.get('email')}: {e}")
    if resp.status_code != 200:
        raise AssertionError(f"Login failed for {credentials.get('email')}: status {resp.status_code}, body: {resp.text}")
    try:
        j = resp.json()
    except ValueError:
        raise AssertionError("Login response was not valid JSON")
    token = extract_bearer_token(j)
    if not token:
        raise AssertionError(f"Login response did not contain a recognizable token. Full response JSON: {j}")
    return token


def test_get_user_projects():
    # Attempt primary credentials first, then fallback
    token = None
    last_error = None
    for creds in (PRIMARY_CREDENTIAL, FALLBACK_CREDENTIAL):
        try:
            token = login_try_credentials(creds)
            break
        except AssertionError as e:
            last_error = e
    if not token:
        raise AssertionError(f"Unable to obtain auth token with provided credentials. Last error: {last_error}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    url = f"{API_BASE}/projects"
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"GET /projects request failed: {e}")

    assert resp.status_code == 200, f"Expected 200 OK from GET /projects, got {resp.status_code}. Body: {resp.text}"

    # Validate response body - accept either a JSON list or an object containing a list under common keys
    try:
        body = resp.json()
    except ValueError:
        raise AssertionError("GET /projects did not return valid JSON")

    # If it's a list, ensure elements are objects (projects)
    if isinstance(body, list):
        projects = body
    elif isinstance(body, dict):
        # common wrappers
        if "projects" in body and isinstance(body["projects"], list):
            projects = body["projects"]
        elif "data" in body and isinstance(body["data"], list):
            projects = body["data"]
        elif "items" in body and isinstance(body["items"], list):
            projects = body["items"]
        else:
            # If dict but not containing an obvious list, fail the assertion
            raise AssertionError(
                "GET /projects returned JSON object but did not contain a projects list under 'projects', 'data', or 'items'. "
                f"Response JSON keys: {list(body.keys())}"
            )
    else:
        raise AssertionError(f"Unexpected JSON type for GET /projects: {type(body)}")

    # projects should be a list (can be empty). If not empty, ensure each project is a dict and has at least an id or name.
    assert isinstance(projects, list), "Parsed projects payload is not a list"
    for idx, p in enumerate(projects):
        assert isinstance(p, dict), f"Project at index {idx} is not an object: {p}"
        # At least one identifying field should be present
        if not any(k in p for k in ("id", "project_id", "name")):
            raise AssertionError(f"Project at index {idx} missing expected fields (id/name). Project: {p}")

    return True


if __name__ == "__main__":
    try:
        test_get_user_projects()
        print("TC005 passed: GET /api/v1/projects returned 200 and valid project list structure.")
        sys.exit(0)
    except AssertionError as e:
        print(f"TC005 failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"TC005 encountered unexpected error: {e}")
        sys.exit(2)