"""aisr-site: build or preview the static site."""

import argparse
import functools
import http.server
import os
from pathlib import Path

from aisr_site.build import DIST, build


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    """Static preview close to Workers assets behaviour, plus byte ranges so video can seek."""

    def __init__(self, *args, media_root: Path | None, **kwargs):
        self.media_root = media_root
        super().__init__(*args, directory=str(DIST), **kwargs)

    def translate_path(self, path: str) -> str:
        if self.media_root and path.startswith("/_media/"):
            return str(self.media_root / path.removeprefix("/_media/").split("?")[0])
        return super().translate_path(path)

    def send_head(self):
        path = Path(self.translate_path(self.path))
        if not path.exists():
            self.send_response(404)
            body = (DIST / "404.html").read_bytes()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return None
        range_header = self.headers.get("Range")
        if not (range_header and path.is_file()):
            return super().send_head()
        size = path.stat().st_size
        start_s, _, end_s = range_header.removeprefix("bytes=").partition("-")
        start = int(start_s) if start_s else size - int(end_s)
        end = int(end_s) if (end_s and start_s) else size - 1
        f = path.open("rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        self.wfile.write(f.read(end - start + 1))
        f.close()
        return None


def main() -> None:
    parser = argparse.ArgumentParser(prog="aisr-site")
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build", help="Build dist/ (published works only unless --drafts)")
    b.add_argument("--drafts", action="store_true", help="Include draft works (never deploy this build)")
    s = sub.add_parser("serve", help="Build and preview locally")
    s.add_argument("--drafts", action="store_true")
    s.add_argument("--media-root", type=Path, help="Local mirror of the media bucket, served at /_media/")
    s.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.command == "build":
        out = build(include_drafts=args.drafts)
        print(f"built {out}")
        return

    media = f"http://localhost:{args.port}/_media" if args.media_root else None
    build(include_drafts=args.drafts, media_base_url=media)
    handler = functools.partial(PreviewHandler, media_root=args.media_root.resolve() if args.media_root else None)
    print(f"serving http://localhost:{args.port}/")
    os.chdir(DIST)
    http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()
