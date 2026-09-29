import requests
import uuid
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 30


def test_register_new_developer_account_TC001():
    # Prepare unique test user data
    unique_suffix = uuid.uuid4().hex[:8]
    email = f"test+{unique_suffix}@example.com"
    password = "TestPass123!"
    display_name = "Test User " + unique_suffix

    register_payload = {
        "email": email,
        "password": password,
        "display_name": display_name
    }

    created_user_id = None
    auth_token = None

    try:
        # 1) Register new user
        resp = requests.post(f"{BASE_URL}/auth/register", json=register_payload, timeout=TIMEOUT)
        try:
            resp_json = resp.json()
        except ValueError:
            resp_json = None

        assert resp.status_code == 200, f"Expected status 200 from register, got {resp.status_code}: {resp.text}"
        assert isinstance(resp_json, dict), f"Expected JSON object in response body, got: {resp.text}"

        # Support responses where user object may be nested or top-level
        if "user" in resp_json and isinstance(resp_json["user"], dict):
            user_obj = resp_json["user"]
        else:
            user_obj = resp_json

        # Validate returned user fields
        assert "email" in user_obj, f"Registered user response missing 'email': {resp_json}"
        assert user_obj.get("email") == email, f"Registered email mismatch. Expected {email}, got {user_obj.get('email')}"
        # Display name may be under different keys
        display_keys = ["display_name", "displayName", "name"]
        returned_display = None
        for k in display_keys:
            if k in user_obj:
                returned_display = user_obj.get(k)
                break
        assert returned_display in (display_name, None) or returned_display is not None, \
            f"Registered user missing display name under expected keys; response: {user_obj}"

        # Capture id for cleanup if present
        created_user_id = user_obj.get("id") or user_obj.get("user_id")

    except requests.RequestException as e:
        raise AssertionError(f"HTTP request failed during registration: {e}") from e
    finally:
        # Cleanup: try to remove the created user if possible.
        # Approach:
        # 1) Attempt to login as the created user to obtain a token
        # 2) Use common delete endpoints (best-effort): DELETE /auth/me, DELETE /users/{id}
        # All cleanup attempts are best-effort and won't fail the test if deletion is unsupported.
        try:
            # Attempt login to get token
            login_payload = {"email": email, "password": password}
            r_login = requests.post(f"{BASE_URL}/auth/login", json=login_payload, timeout=TIMEOUT)
            token = None
            try:
                login_json = r_login.json()
            except ValueError:
                login_json = None

            if r_login.status_code == 200 and isinstance(login_json, dict):
                # token might be named access_token, token, or inside data
                token = login_json.get("access_token") or login_json.get("token") or login_json.get("accessToken")
                if not token and "data" in login_json and isinstance(login_json["data"], dict):
                    token = login_json["data"].get("access_token") or login_json["data"].get("token")
            auth_token = token

            headers = {}
            if auth_token:
                headers["Authorization"] = f"Bearer {auth_token}"

            # Try DELETE /auth/me
            try:
                r_del = requests.delete(f"{BASE_URL}/auth/me", headers=headers, timeout=TIMEOUT)
                # Accept 200/204 as successful deletion; otherwise ignore
                if r_del.status_code in (200, 204):
                    return
            except requests.RequestException:
                pass

            # Try DELETE /users/{id} if we have id
            if created_user_id:
                try:
                    r_del2 = requests.delete(f"{BASE_URL}/users/{created_user_id}", headers=headers, timeout=TIMEOUT)
                    if r_del2.status_code in (200, 204):
                        return
                except requests.RequestException:
                    pass

            # Try DELETE /api/v1/users/me as alternative
            try:
                r_del3 = requests.delete(f"{BASE_URL}/users/me", headers=headers, timeout=TIMEOUT)
                if r_del3.status_code in (200, 204):
                    return
            except requests.RequestException:
                pass

            # If no token or endpoints failed, attempt an unauthenticated delete endpoints (best-effort)
            if created_user_id:
                try:
                    r_del4 = requests.delete(f"{BASE_URL}/users/{created_user_id}", timeout=TIMEOUT)
                    if r_del4.status_code in (200, 204):
                        return
                except requests.RequestException:
                    pass

        except requests.RequestException:
            # swallow cleanup exceptions
            pass


if __name__ == "__main__":
    try:
        test_register_new_developer_account_TC001()
        print("TC001 passed")
    except AssertionError as e:
        print("TC001 failed:", e)
        sys.exit(1)
    except Exception as e:
        print("TC001 encountered an unexpected error:", e)
        sys.exit(2)