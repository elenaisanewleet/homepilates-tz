"""Generate file:// previews and Tilda T123 fragments from the same source."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content.json").read_text())
SITE = ROOT / "site"
TILDA = ROOT / "tilda"


def link(current, target, embed):
    if embed:
        return "/" + target
    return ("../" if current else "") + (target + "/" if target else "") + "index.html"


def render(slug, embed):
    nav = "".join(
        f'<a href="{link(slug, route, embed)}">{escape(label)}</a> '
        for route, label in DATA["pages"].items()
    )
    return f'<nav>{nav}</nav><main><h1>{escape(DATA["pages"][slug])}</h1></main>'


def generate():
    TILDA.mkdir(exist_ok=True)
    for slug, title in DATA["pages"].items():
        directory = SITE / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(
            '<!doctype html>\n<html lang="ru"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)} — HomePilates</title>{render(slug, False)}</html>\n'
        )
        (TILDA / ((slug or "index") + ".html")).write_text(render(slug, True) + "\n")


if __name__ == "__main__":
    generate()
