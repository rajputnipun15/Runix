import requests
import sys

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_templates():
    session = requests.Session()

    # Attempt to obtain Bearer token via login (optional for this endpoint)
    login_url = f"{BASE_URL}/api/v1/auth/login"
    credentials = {"email": "demo@runix.internal", "password": "Demopassword123!"}
    token = None

    try:
        resp = session.post(login_url, json=credentials, timeout=TIMEOUT)
        if resp.status_code == 200:
            try:
                login_json = resp.json()
            except ValueError:
                raise AssertionError(f"Login response is not JSON: {resp.text}")
            # common token fields
            token = (
                login_json.get("access_token")
                or login_json.get("token")
                or login_json.get("accessToken")
                or login_json.get("jwt")
            )
            # Some APIs return token_type + access_token
            if not token and isinstance(login_json, dict):
                if "token_type" in login_json and "access_token" in login_json:
                    token = login_json.get("access_token")
            assert token, f"Login succeeded but no token found in response: {login_json}"
        else:
            # Login failed; proceed without auth because /templates is not auth-required per PRD
            print(f"Login returned {resp.status_code}; proceeding without auth for templates endpoint.")
    except requests.RequestException as e:
        print(f"Login request failed ({e}); proceeding without auth for templates endpoint.")

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    templates_url = f"{BASE_URL}/api/v1/templates"
    try:
        r = session.get(templates_url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"Templates request failed: {e}")

    assert r.status_code == 200, f"Expected 200 from {templates_url}, got {r.status_code}. Body: {r.text}"

    try:
        body = r.json()
    except ValueError:
        raise AssertionError("Templates response is not valid JSON")

    # Normalize to a list of items
    templates_items = None
    if isinstance(body, list):
        templates_items = body
    elif isinstance(body, dict):
        # common wrapper keys
        for k in ("templates", "data", "items", "results"):
            if isinstance(body.get(k), list):
                templates_items = body.get(k)
                break
        if templates_items is None:
            # If the dict itself seems like a single template object or map, try to extract list-like values
            # As a fallback, treat empty list
            templates_items = []
    else:
        templates_items = []

    expected_templates = [
        "react-vite-ts",
        "node-typescript",
        "python-fastapi",
        "mern",
        "blank-docker",
    ]

    # Collect searchable strings from returned items
    found_strings = set()
    for item in templates_items:
        if isinstance(item, str):
            found_strings.add(item)
        elif isinstance(item, dict):
            for key in ("id", "slug", "name"):
                val = item.get(key)
                if isinstance(val, str):
                    found_strings.add(val)
            # also inspect all string values for substrings matching expected templates
            for v in item.values():
                if isinstance(v, str):
                    found_strings.add(v)

    # Assert each expected template exists (either exact match or substring match)
    missing = []
    for exp in expected_templates:
        matched = any((exp == s or exp in s) for s in found_strings)
        if not matched:
            missing.append(exp)

    assert not missing, f"Missing expected templates: {missing}. Found values: {sorted(found_strings)}"

    print("TC008 passed: retrieved templates list contains expected starter templates.")

if __name__ == "__main__":
    try:
        test_get_templates()
    except AssertionError as e:
        print(f"TC008 failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"TC008 unexpected error: {e}")
        sys.exit(2)
    sys.exit(0)