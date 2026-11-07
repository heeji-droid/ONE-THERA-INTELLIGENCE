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

    out = pathlib.Path(args.out)
    out.write_text(html[:m.end(1)] + payload + html[m.start(3):], encoding="utf-8")
    d = json.loads(payload)
    print(f"{out} · {len(d['insights'])} insights · {d['coverage']['horizon']} · "
          f"{len(d.get('cases', []))} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
