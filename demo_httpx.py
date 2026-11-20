"""Demo based on the encode/httpx README example.

README shows:
    >>> import httpx
    >>> r = httpx.get('https://www.example.org/')
    >>> r
    <Response [200 OK]>
    >>> r.status_code
    200
    >>> r.headers['content-type']
    'text/html; charset=UTF-8'
    >>> r.text
    '<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
"""
import httpx


def main():
    r = httpx.get("https://www.example.org/", timeout=30)
    print(f"response: {r}")
    print(f"status_code: {r.status_code}")
    print(f"content-type: {r.headers['content-type']}")
    print(f"text[:80]: {r.text[:80]!r}")

    # Confirm the README's claims
    assert r.status_code == 200, r.status_code
    assert r.headers["content-type"].lower() == "text/html; charset=utf-8"
    assert r.text.startswith("<!doctype html>")
    assert "<title>Example Domain</title>" in r.text
    print("OK: all README checks passed")


if __name__ == "__main__":
    main()
