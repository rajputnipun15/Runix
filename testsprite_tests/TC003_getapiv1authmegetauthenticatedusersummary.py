import requests
import uuid
import sys

BASE = "http://localhost:8000/api/v1"
TIMEOUT = 30

def extract_token(json_obj):
    # Try common token locations
    if not isinstance(json_obj, dict):
        return None
    for key in ("access_token", "token", "accessToken", "jwt"):
        if key in json_obj and isinstance(json_obj[key], str):
            return json_obj[key]
    # nested under data
    data = json_obj.get("data") if isinstance(json_obj.get("data"), dict) else None
    if data:
        for key in ("access_token", "token", "accessToken", "jwt"):
            if key in data and isinstance(data[key], str):
                return data[key]
    return None

def test_get_authenticated_user_summary_tc003():
    session = requests.Session()
    registered_new_user = False
    user_email = "demo@runix.internal"
    user_password = "Demopassword123!"
    token = None

    # Attempt login with known demo credentials
    try:
        resp = session.post(f"{BASE}/auth/login", json={"email": user_email, "password": user_password}, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"Login request failed: {e}")

    if resp.status_code == 200:
        try:
            resp_json = resp.json()
        except ValueError:
            raise AssertionError("Login response is not valid JSON")
        token = extract_token(resp_json)
        assert token, f"Token not found in login response: {resp_json}"
    else:
        # If demo login failed, register a new user and then login
        new_email = f"testuser+{uuid.uuid4().hex[:8]}@example.com"
        new_password = "TestPassword123!"
        register_payload = {"email": new_email, "password": new_password, "display_name": "Test User"}
        try:
            reg_resp = session.post(f"{BASE}/auth/register", json=register_payload, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Register request failed: {e}")

        assert reg_resp.status_code in (200, 201), f"Expected 200 or 201 from register, got {reg_resp.status_code}, body: {reg_resp.text}"
        registered_new_user = True
        user_email = new_email
        user_password = new_password

        # Login with the newly registered user
        try:
            login_resp = session.post(f"{BASE}/auth/login", json={"email": user_email, "password": user_password}, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise AssertionError(f"Login request for new user failed: {e}")

        assert login_resp.status_code == 200, f"Expected 200 from login for new user, got {login_resp.status_code}, body: {login_resp.text}"
        try:
            login_json = login_resp.json()
        except ValueError:
            raise AssertionError("Login response for new user is not valid JSON")
        token = extract_token(login_json)
        assert token, f"Token not found in login response for new user: {login_json}"

    # With token, call GET /auth/me and validate
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        me_resp = session.get(f"{BASE}/auth/me", headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        # Attempt to logout in case of exception before raising
        try:
            session.post(f"{BASE}/auth/logout", headers=headers, timeout=TIMEOUT)
        except Exception:
            pass
        raise AssertionError(f"Request to /auth/me failed: {e}")

    try:
        me_json = me_resp.json()
    except ValueError:
        me_json = None

    # Ensure we cleanup (logout) regardless of assertions
    try:
        assert me_resp.status_code == 200, f"Expected 200 from GET /auth/me, got {me_resp.status_code}, body: {me_resp.text}"
        assert isinstance(me_json, dict), f"Expected JSON object from /auth/me, got: {me_resp.text}"
        # Validate expected user fields - at minimum email should be present and match
        assert "email" in me_json, f"'email' not present in /auth/me response: {me_json}"
        assert me_json.get("email") == user_email, f"Expected email '{user_email}' in /auth/me, got '{me_json.get('email')}'"
    finally:
        # Logout to revoke token/session
        try:
            logout_resp = session.post(f"{BASE}/auth/logout", headers=headers, timeout=TIMEOUT)
            # Accept 200 or 204 as valid logout responses
            if logout_resp.status_code not in (200, 204):
                # If logout failed, raise a warning-style assertion but do not mask original failures
                raise AssertionError(f"Logout returned unexpected status {logout_resp.status_code}: {logout_resp.text}")
        except requests.RequestException as e:
            raise AssertionError(f"Logout request failed: {e}")

if __name__ == "__main__":
    test_get_authenticated_user_summary_tc003()
    print("TC003 passed.")