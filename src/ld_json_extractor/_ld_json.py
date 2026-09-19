import json
import logging
from collections.abc import Iterator
from types import NoneType

from selectolax.lexbor import LexborHTMLParser

logger = logging.getLogger("ld_json_extractor")

Json = dict | list | int | float | str | NoneType

LD_JSON_MIME = "application/ld+json"
APP_JSON_MIME = "application/json"


def json_iter(parser: LexborHTMLParser, script_type: str) -> Iterator[Json]:
    for script_el in parser.css(f'script[type="{script_type}"]'):
        try:
            yield json.loads(script_el.text(), strict=False)
        except json.JSONDecodeError as e:
            logger.debug(
                "Skipping invalid JSON in <script type=%r>: %s", script_type, e
            )
            continue
    return None


def find_ld_json(type_: str, parser: LexborHTMLParser) -> dict | None:
    for data in json_iter(parser, script_type=LD_JSON_MIME):
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") == type_:
                    return item
        elif isinstance(data, dict) and data.get("@type") == type_:
            return data
    return None
