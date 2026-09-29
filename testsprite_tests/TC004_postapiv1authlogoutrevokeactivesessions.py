import requests
import sys
from requests.exceptions import RequestException

BASE_URL = "http://localhost:8000/api/v1"
LOGIN_PATH = "/auth/login"
LOGOUT_PATH = "/auth/logout"
TIMEOUT = 30

def extract_token_from_response(json_obj):
    # Look for common token keys
    if not isinstance(json_obj, dict):
        return None
    for key in ("access_token", "token", "jwt", "accessToken", "id_token"):
        if key in json_obj and isinstance(json_obj[key], str) and json_obj[key]:
            return json_obj[key]
    # Sometimes token is nested under "data"
    if "data" in json_obj and isinstance(json_obj["data"], dict):
        for key in ("access_token", "token", "jwt", "accessToken", "id_token"):
            if key in json_obj["data"] and isinstance(json_obj["data"][key], str):
                return json_obj["data"][key]
    # Fallback: search for any string value that looks like a JWT (has two dots)
    def find_jwt(obj):
        if isinstance(obj, dict):
            for v in obj.values():
                res = find_jwt(v)
                if res:
                    return res
        elif isinstance(obj, list):
            for item in obj:
                res = find_jwt(item)
                if res:
                    return res
        elif isinstance(obj, str):
            if obj.count(".") == 2:
                return obj
        return None
    return find_jwt(json_obj)

def test_postapiv1authlogoutrevokeactivesessions():
    login_url = BASE_URL + LOGIN_PATH
    logout_url = BASE_URL + LOGOUT_PATH

    login_payload = {
        "email": "demo@runix.internal",
        "password": "Demopassword123!"
    }
    headers = {"Content-Type": "application/json"}

    try:
        # 1) Login to obtain token
        resp = requests.post(login_url, json=login_payload, headers=headers, timeout=TIMEOUT)
    except RequestException as e:
        raise AssertionError(f"Login request failed: {e}")

    assert resp is not None, "No response from login endpoint"
    try:
        resp_json = resp.json()
    except ValueError:
        resp_json = None

    assert resp.status_code == 200, f"Expected 200 OK from login, got {resp.status_code}. Body: {resp.text}"
    assert resp_json is not None, f"Login response did not contain valid JSON. Body: {resp.text}"

    token = extract_token_from_response(resp_json)
    assert token, f"Could not extract token from login response JSON: {resp_json}"

    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        # 2) Call logout with valid token - expect 200
        logout_resp = requests.post(logout_url, headers=auth_headers, timeout=TIMEOUT)
    except RequestException as e:
        raise AssertionError(f"Logout request (with token) failed: {e}")

    assert logout_resp is not None, "No response from logout endpoint (with token)"
    # Accept 200 explicitly as success
    assert logout_resp.status_code == 200, f"Expected 200 OK from logout with valid token, got {logout_resp.status_code}. Body: {logout_resp.text}"

    # 3) Negative check: call logout without token or with invalid token -> expect 401/403
    try:
        no_auth_resp = requests.post(logout_url, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)
    except RequestException as e:
        raise AssertionError(f"Logout request (without token) failed: {e}")

    assert no_auth_resp is not None, "No response from logout endpoint (without token)"
    assert no_auth_resp.status_code in (401, 403), f"Expected 401/403 when calling logout without token, got {no_auth_resp.status_code}. Body: {no_auth_resp.text}"

if __name__ == "__main__":
    try:
        test_postapiv1authlogoutrevokeactivesessions()
        print("TC004 passed.")
    except AssertionError as e:
        print(f"TC004 failed: {e}")
        sys.exit(1)
    except Exception as ex:
        print(f"TC004 encountered an unexpected error: {ex}")
        sys.exit(2)