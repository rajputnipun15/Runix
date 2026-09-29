import requests
import sys

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_api_v1_auth_login_authenticate_user_credentials():
    url = f"{BASE_URL}/api/v1/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": "demo@runix.internal",
        "password": "Demopassword123!"
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise SystemExit(f"HTTP request failed: {e}")

    # Validate status code
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}: {resp.text}"

    # Validate JSON body and presence of token
    try:
        body = resp.json()
    except ValueError:
        raise AssertionError(f"Response is not valid JSON: {resp.text}")

    possible_token_keys = [
        "access_token", "token", "jwt", "session_token", "session", "id_token"
    ]

    token = None
    token_key = None

    # Direct keys
    if isinstance(body, dict):
        for k in possible_token_keys:
            if k in body:
                token = body[k]
                token_key = k
                break

    # Nested under "data"
    if not token and isinstance(body, dict) and "data" in body and isinstance(body["data"], dict):
        for k in possible_token_keys:
            if k in body["data"]:
                token = body["data"][k]
                token_key = f"data.{k}"
                break

    assert token is not None, f"No token found in response JSON. Response keys: {list(body.keys())}, body: {body}"
    assert isinstance(token, str) and token.strip() != "", "Token is empty or not a string"

    print(f"Test passed: received token under key '{token_key}' with length {len(token)}")

if __name__ == "__main__":
    test_post_api_v1_auth_login_authenticate_user_credentials()