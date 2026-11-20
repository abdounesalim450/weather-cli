"""Demo based on the psf/requests README example.

README shows:
    >>> import requests
    >>> r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
    >>> r.status_code  # 200
    >>> r.headers['content-type']  # 'application/json; charset=utf8'
    >>> r.encoding  # 'utf-8'
    >>> r.text  # '{"authenticated": true, ...'
    >>> r.json()  # {'authenticated': True, ...}
"""
import requests


def main():
    r = requests.get(
        "https://httpbin.org/basic-auth/user/pass",
        auth=("user", "pass"),
        timeout=30,
    )
    print(f"status_code: {r.status_code}")
    print(f"content-type: {r.headers['content-type']}")
    print(f"encoding: {r.encoding}")
    print(f"text: {r.text.strip()}")
    data = r.json()
    print(f"json: {data}")

    # Confirm the README's claims
    assert r.status_code == 200, r.status_code
    assert "application/json" in r.headers["content-type"]
    assert r.encoding == "utf-8"
    assert data["authenticated"] is True
    assert data["user"] == "user"
    print("OK: all README checks passed")


if __name__ == "__main__":
    main()
