# Directory Summary — project1

Short summary of the files in this directory (`/Users/macbookpro/Desktop/GS-META/project1`).

## Files

| Name | Type | What it is for |
|------|------|----------------|
| `demo_requests.py` | Python script | Demo based on the `psf/requests` README example. Sends an authenticated GET request to `https://httpbin.org/basic-auth/user/pass` with `requests`, prints status code, content-type, encoding, text and JSON, and asserts the README's claims (200, JSON content-type, utf-8, `authenticated: True`). |
| `demo_httpx.py` | Python script | Demo based on the `encode/httpx` README example. Sends a GET request to `https://www.example.org/` with `httpx`, prints response, status code, content-type and body preview, and asserts the README's claims (200, `text/html; charset=UTF-8`, Example Domain HTML). |
| `.venv/` | Directory (virtual environment) | Python 3.9.6 virtual environment for this project (created from `/Applications/Xcode.app/.../bin`, `include-system-site-packages = false`). Contains `bin/`, `lib/`, `include/` and `pyvenv.cfg`; holds the installed dependencies (`requests`, `httpx`, etc.) isolated from the system Python. |
| `test-notes.md` | Markdown (this file) | This summary note describing the contents of the directory. |

## Notes

- Both demo scripts are self-checking: they run with `timeout=30`, print response details, and exit with `OK: all README checks passed` when the assertions pass.
- No `README`, `requirements.txt`, or package/config files are present at the top level yet.
Capture test after consent v1.1 re-acceptance, 20 Nov 2026
