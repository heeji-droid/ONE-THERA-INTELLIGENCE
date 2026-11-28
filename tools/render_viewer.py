#!/usr/bin/env python3
"""뷰어 HTML 생성 — 템플릿 + payload.

컨테이너가 회수되면 scratchpad는 사라진다. 2026-09-25에 실제로 그렇게 됐고
발행된 아티팩트에서 되살려야 했다. 템플릿을 저장소에 두면 그 복구가 필요 없다.

    python3 tools/render_viewer.py -o desk.html
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "viewer" / "desk.template.html"
SLOT = re.compile(r'(<script id="payload"[^>]*>)(.*?)(</script>)', re.S)


def build_stamp() -> str:
    """발행본이 어느 저장소 상태에서 나왔는지 적는다.

    뷰어 '버전'은 Artifact 서비스가 매기므로 저장소가 알 수 없고, 그래서
    2026-11-24까지 처리 세션이 손으로 옮겼다(데스크 IX가 '검증할 수 없는 값'으로
    보고했다). 이 각인은 그 번호를 대신하지 않는다 — 대신 **발행본 → 커밋**을
    되짚을 수 있게 한다. 작업 트리가 더러우면 `+local` 을 붙인다: 처리 세션은
    블록을 prepend 한 뒤 커밋 전에 렌더하므로, 평상시 값이 `<sha>+local` 이고
    그 sha 는 블록을 담은 커밋의 **부모**다. 그 사실을 숨기지 않는다.
    """
    def git(*a: str) -> str:
        return subprocess.run(["git", *a], cwd=REPO, capture_output=True,
                              text=True, check=True).stdout.strip()
    try:
        sha = git("rev-parse", "--short", "HEAD")
        dirty = bool(git("status", "--porcelain"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
    return f"{sha}+local" if dirty else sha


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="desk.html")
    ap.add_argument("--payload", help="기존 payload.json 을 쓴다. 생략하면 새로 만든다")
    args = ap.parse_args()

    if args.payload:
        payload = pathlib.Path(args.payload).read_text(encoding="utf-8")
    else:
        # build_payload 는 요약 한 줄을 stdout 에 찍는다. 파일로 받아야 JSON 만 남는다
        with tempfile.TemporaryDirectory() as tmp:
            tmp_payload = pathlib.Path(tmp) / "payload.json"
            subprocess.run(
                [sys.executable, str(REPO / "tools" / "build_payload.py"), "-o", str(tmp_payload)],
                capture_output=True, text=True, cwd=REPO, check=True,
            )
            payload = tmp_payload.read_text(encoding="utf-8")

    json.loads(payload)  # 깨진 payload 를 발행하지 않는다
    if "</script" in payload:
        raise SystemExit("payload 에 </script 가 있어 스크립트 태그가 깨진다")

    html = TEMPLATE.read_text(encoding="utf-8")
    m = SLOT.search(html)
    if not m:
        raise SystemExit(f"{TEMPLATE} 에 <script id=\"payload\"> 가 없다")

    stamp = build_stamp()
    if "__BUILD__" not in html:
        raise SystemExit(f"{TEMPLATE} 에 __BUILD__ 자리가 없다")
    html = html.replace("__BUILD__", stamp)

    out = pathlib.Path(args.out)
    out.write_text(html[:m.end(1)] + payload + html[m.start(3):], encoding="utf-8")
    d = json.loads(payload)
    print(f"{out} · {len(d['insights'])} insights · {d['coverage']['horizon']} · "
          f"{len(d.get('cases', []))} cases · build {stamp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
