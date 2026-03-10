#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import cast

import yaml


ROOT = Path(__file__).resolve().parents[1]
LINKS_FILE = ROOT / "_data" / "links.yml"
ICON_CSS_FILE = ROOT / "addon1" / "semantic.min.css"
ICON_PATTERN = re.compile(r"i\.icon\.([a-z0-9.-]+):before")


def load_supported_icons() -> set[str]:
    css_text = ICON_CSS_FILE.read_text(encoding="utf-8", errors="ignore")
    return {match.group(1).replace(".", " ") for match in ICON_PATTERN.finditer(css_text)}


def as_dict(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return {str(key): cast(object, item) for key, item in value.items()}
    return {}


def as_string(value: object) -> str:
    if isinstance(value, str):
        return value
    return ""


def iter_link_icons() -> list[tuple[str, str]]:
    with LINKS_FILE.open("r", encoding="utf-8") as fh:
        loaded = yaml.safe_load(fh)

    sections: list[object] = loaded if isinstance(loaded, list) else []

    results: list[tuple[str, str]] = []
    for section in sections:
        section_map = as_dict(section)
        categories = section_map.get("categories", [])
        if not isinstance(categories, list):
            continue

        for category in categories:
            category_map = as_dict(category)
            category_name = as_string(category_map.get("name")) or "<unknown>"
            links = category_map.get("links", [])
            if not isinstance(links, list):
                continue

            for link in links:
                link_map = as_dict(link)
                icon = as_string(link_map.get("icon")).strip()
                if not icon:
                    continue
                link_name = as_string(link_map.get("name")) or "<unknown>"
                results.append((f"{category_name} / {link_name}", icon))
    return results


def main() -> int:
    supported_icons = load_supported_icons()
    invalid_icons = []

    for location, icon in iter_link_icons():
        if icon not in supported_icons:
            invalid_icons.append((location, icon))

    if invalid_icons:
        print("Unsupported icons found:")
        for location, icon in invalid_icons:
            print(f"- {location}: {icon}")
        return 1

    print("All icons in _data/links.yml are supported by addon1/semantic.min.css.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
