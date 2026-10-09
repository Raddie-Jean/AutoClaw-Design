"""Check local links and SVG validity before sharing the static package."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent / "docs"


class LocalLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.urls.append(value)


def main() -> None:
    assert (ROOT / "index.html").exists(), "Missing site entry"
    errors: list[str] = []
    checked = 0
    pages = list(ROOT.rglob("*.html"))
    for page in pages:
        links = LocalLinks()
        links.feed(page.read_text(encoding="utf-8"))
        for value in links.urls:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("//"):
                continue
            destination = (page.parent / unquote(parsed.path)).resolve()
            checked += 1
            if not destination.is_file() and not (destination.is_dir() and (destination / "index.html").is_file()):
                errors.append(f"{page.relative_to(ROOT)} → {value}")

    vectors = list(ROOT.rglob("*.svg"))
    for file in vectors:
        ET.parse(file)
    if errors:
        raise SystemExit("Broken local links:\n" + "\n".join(errors))
    print(f"OK: {len(pages)} HTML pages, {checked} local links, {len(vectors)} SVG files")


if __name__ == "__main__":
    main()
