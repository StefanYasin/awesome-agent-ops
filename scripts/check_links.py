#!/usr/bin/env python3
"""Fetch every list entry and verify that it resolves.

A link passes when it answers with HTTP 200, or with HTTP 301 that leads to a
final 200. With --check-archived, the GitHub API is also queried so archived
repositories are reported as failures.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
ENTRY_RE = re.compile(r"^- \[[^\]]+\]\((https://github\.com/[^)\s]+)\) - .+$")
REPO_RE = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)$")
USER_AGENT = "awesome-agent-ops-linkcheck/1.0 (+https://github.com/StefanYasin/awesome-agent-ops)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def read_urls() -> list[str]:
    text = README.read_text(encoding="utf-8")
    urls = [match.group(1) for line in text.splitlines() if (match := ENTRY_RE.match(line))]
    return list(dict.fromkeys(urls))


def request_opener():
    return urllib.request.build_opener(NoRedirect())


def fetch_once(url: str, timeout: float) -> tuple[int | None, str | None]:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        response = request_opener().open(req, timeout=timeout)
        code = response.status
        location = response.headers.get("Location")
        response.close()
        return code, location
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Location")


def check_url(url: str, timeout: float, retries: int = 3) -> dict:
    last_error = "no attempt made"
    for attempt in range(retries):
        try:
            code, location = fetch_once(url, timeout)
            if code == 200:
                return {"url": url, "ok": True, "status": 200, "final_url": url}
            if code == 301:
                if not location:
                    return {"url": url, "ok": False, "status": 301, "reason": "301 without Location header"}
                if location.startswith("/"):
                    location = url + location
                final_url = urllib.parse.urljoin(url, location)
                with urllib.request.urlopen(
                    urllib.request.Request(final_url, headers={"User-Agent": USER_AGENT}, method="GET"),
                    timeout=timeout,
                ) as response:
                    final_code = response.status
                    reached = response.geturl()
                if final_code == 200:
                    return {"url": url, "ok": True, "status": 301, "final_url": reached}
                return {
                    "url": url,
                    "ok": False,
                    "status": 301,
                    "final_url": reached,
                    "reason": f"301 led to HTTP {final_code}",
                }
            if code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                last_error = f"HTTP {code}"
                time.sleep(2 * (attempt + 1))
                continue
            return {"url": url, "ok": False, "status": code, "reason": f"HTTP {code}"}
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = str(error)
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    return {"url": url, "ok": False, "reason": last_error}


def check_archived(url: str, token: str | None, timeout: float) -> dict:
    match = REPO_RE.match(url)
    if not match:
        return {"url": url, "archived": None, "warning": "not a canonical repository URL"}
    repo = match.group(1)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.load(response)
        return {
            "url": url,
            "repo": repo,
            "archived": bool(data.get("archived")),
            "full_name": data.get("full_name"),
            "stars": data.get("stargazers_count"),
        }
    except urllib.error.HTTPError as error:
        return {"url": url, "archived": None, "warning": f"GitHub API HTTP {error.code}"}
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return {"url": url, "archived": None, "warning": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", help="write a machine-readable report")
    parser.add_argument("--check-archived", action="store_true", help="query the GitHub API for archived repos")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    urls = read_urls()
    if not urls:
        print("No entries found in README.md")
        return 1

    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(check_url, url, args.timeout): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: item["url"])
    failures = [item for item in results if not item.get("ok")]

    archived_results: list[dict] = []
    if args.check_archived:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(check_archived, url, token, args.timeout): url for url in urls}
            for future in concurrent.futures.as_completed(futures):
                archived_results.append(future.result())
        archived_results.sort(key=lambda item: item["url"])
        for item in archived_results:
            if item.get("archived"):
                failures.append(
                    {
                        "url": item["url"],
                        "ok": False,
                        "reason": "repository is archived",
                        "archived": True,
                    }
                )
            elif item.get("warning"):
                print(f"warning: archived check skipped for {item['url']}: {item['warning']}")

    for item in failures:
        reason = item.get("reason") or "unknown failure"
        print(f"FAIL {item['url']}: {reason}")

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(urls),
        "passed": len(urls) - len({item["url"] for item in failures}),
        "failures": failures,
        "results": results,
        "archive_checks": archived_results,
    }
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")

    if failures:
        print(f"\n{len(urls) - len({item['url'] for item in failures})}/{len(urls)} links passed")
        return 1

    print(f"{len(urls)}/{len(urls)} links passed (HTTP 200, or 301 to 200)")
    if args.check_archived:
        checked = sum(1 for item in archived_results if item.get("archived") is not None)
        print(f"{checked}/{len(urls)} repositories checked for archive status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
