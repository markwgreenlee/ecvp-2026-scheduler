#!/usr/bin/env python3
"""Generate dist/manifest.json for the web build from app.json.

Expo stopped emitting a web app manifest with `expo export -p web`, so the
`expo.web` block in app.json (name, theme colour, display mode, ...) never
reached the browser. Without a manifest Chrome on Android will not offer
"Install app"; iOS installs anyway via the apple-touch-icon meta tags that the
deploy workflow injects.

This reads app.json so the manifest cannot drift from the Expo config, and
writes the manifest Chrome expects. Run from the project root, after the export:

    npx expo export -p web
    python3 scripts/make_manifest.py

The matching <link rel="manifest"> tag is injected by the deploy workflow.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Shipped by public/icons/ -> dist/icons/. Sizes must match the real pixel
# dimensions or Chrome ignores the entry. Declared "any" only: the artwork runs
# close to the edges, so a maskable declaration would let Android crop into the
# wordmark.
ICONS = [("icons/icon-192.png", "192x192"), ("icons/icon-512.png", "512x512")]


def build(config):
    expo = config["expo"]
    web = expo.get("web", {})
    base = web.get("baseUrl", "").rstrip("/")
    start_url = web.get("startUrl", f"{base}/")

    manifest = {
        # Chrome keys the installed app on id; pinning it to start_url keeps an
        # existing install attached if start_url ever changes.
        "id": start_url,
        "name": web.get("name", expo["name"]),
        "short_name": web.get("shortName", expo["name"]),
        "start_url": start_url,
        "scope": web.get("scope", f"{base}/"),
        "display": web.get("display", "standalone"),
        "orientation": web.get("orientation", "portrait"),
        "theme_color": web.get("themeColor", "#ffffff"),
        "background_color": web.get("backgroundColor", "#ffffff"),
        "icons": [
            {"src": f"{base}/{src}", "sizes": sizes, "type": "image/png", "purpose": "any"}
            for src, sizes in ICONS
        ],
    }
    if web.get("description"):
        manifest["description"] = web["description"]
    return manifest


def main():
    if not DIST.is_dir():
        raise SystemExit("dist/ not found - run `npx expo export -p web` first")

    manifest = build(json.loads((ROOT / "app.json").read_text()))

    missing = [rel for rel, _ in ICONS if not (DIST / rel).exists()]
    if missing:
        raise SystemExit(f"icons missing from dist/: {missing}")

    out = DIST / "manifest.json"
    # ensure_ascii=False keeps the en dash in the description readable; the file
    # is served as UTF-8.
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(manifest['icons'])} icons)")


if __name__ == "__main__":
    main()
