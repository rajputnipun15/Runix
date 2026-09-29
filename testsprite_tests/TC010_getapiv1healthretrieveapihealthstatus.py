import requests
import sys
from requests.exceptions import RequestException, Timeout, HTTPError

BASE_URL = "http://localhost:8000"
BASE_PATH = "/api/v1"
TIMEOUT = 30.0

def test_get_api_v1_health_retrieve_api_health_status():
    session = requests.Session()
    headers = {"Accept": "application/json"}
    token = None

    # Attempt to obtain Bearer token (optional for health endpoint)
    login_url = f"{BASE_URL}{BASE_PATH}/auth/login"
    login_payload = {
        "email": "demo@runix.internal",
        "password": "Demopassword123!"
    }

    try:
        resp = session.post(login_url, json=login_payload, headers=headers, timeout=TIMEOUT)
    except (RequestException, Timeout) as e:
        # Could not reach auth endpoint; continue to health check unauthenticated
        resp = None

    if resp is not None and resp.status_code == 200:
        try:
            data = resp.json()
            # Common token keys
            for key in ("access_token", "token", "accessToken", "jwt", "auth_token"):
                if key in data and isinstance(data[key], str) and data[key].strip():
                    token = data[key].strip()
                    break
            # Some APIs return nested structure like { "data": { "access_token": "..." } }
            if token is None and "data" in data and isinstance(data["data"], dict):
                for key in ("access_token", "token", "accessToken", "jwt", "auth_token"):
                    if key in data["data"] and isinstance(data["data"][key], str):
                        token = data["data"][key].strip()
                        break
        except ValueError:
            # Non-JSON response; ignore and proceed unauthenticated
            token = None

    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Perform health check
    health_url = f"{BASE_URL}{BASE_PATH}/health"
    try:
        health_resp = session.get(health_url, headers=headers, timeout=TIMEOUT)
    except (RequestException, Timeout) as e:
        raise AssertionError(f"Health endpoint request failed: {e}")

    # Assert HTTP 200
    try:
        assert health_resp.status_code == 200, f"Expected status 200, got {health_resp.status_code}. Response text: {health_resp.text}"
    except AssertionError:
        # Provide more debugging if non-200
        raise

    # Validate response body content for expected health indicator
    content_type = health_resp.headers.get("Content-Type", "")
    body_text = health_resp.text or ""

    if "application/json" in content_type.lower():
        try:
            js = health_resp.json()
        except ValueError:
            raise AssertionError("Health response claimed JSON but body is not valid JSON")

        # Acceptable health indicators:
        # {"status":"ok"}, {"ok": true}, {"status":"healthy"}, {"message":"ok"}, etc.
        if isinstance(js, dict):
            if "status" in js:
                val = js["status"]
                assert str(val).lower() in ("ok", "healthy", "true"), f"Unexpected status value: {val}"
            elif "ok" in js:
                val = js["ok"]
                if isinstance(val, bool):
                    assert val is True, f"Health 'ok' boolean is not True: {val}"
                else:
                    assert str(val).lower() in ("ok", "true", "1"), f"Unexpected ok value: {val}"
            elif "message" in js:
                assert "ok" in str(js["message"]).lower(), f"Unexpected message value: {js['message']}"
            else:
                # If no known keys, fallback to checking any value contains 'ok'
                flat = str(js).lower()
                assert "ok" in flat or "healthy" in flat, f"Health JSON did not contain expected indicators. JSON: {js}"
        else:
            # JSON but not an object -> check text
            assert "ok" in str(js).lower() or "healthy" in str(js).lower(), f"Unexpected JSON body: {js}"
    else:
        # Not JSON: check plain text for 'ok' or 'healthy'
        lowered = body_text.lower()
        assert "ok" in lowered or "healthy" in lowered, f"Health response did not contain 'ok' or 'healthy'. Body: {body_text}"

    print("TC010 passed: /api/v1/health returned 200 with expected health status.")

if __name__ == "__main__":
    try:
        test_get_api_v1_health_retrieve_api_health_status()
    except AssertionError as e:
        print(f"TC010 failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"TC010 encountered an unexpected error: {e}")
        sys.exit(2)
    sys.exit(0)