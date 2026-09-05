import json
import logging
from collections.abc import Iterator
from pathlib import Path

from selectolax.lexbor import LexborHTMLParser

logger = logging.getLogger("ld_json_extractor")

def _fix_unescaped_newlines(content: str) -> str:
    result: list[str] = []
    in_string = False
    escape = False

    for ch in content:
        if ch == '"' and not escape:
            in_string = not in_string
        if ch == "\n" and in_string:
            result.append("\\n")
            continue
        result.append(ch)
        escape = ch == "\\" and not escape

    return "".join(result)


def ld_json_iter(parser: LexborHTMLParser) -> Iterator[dict | list]:
    for script_el in parser.css("script[type='application/ld+json']"):
        text = script_el.text()
        try:
            yield json.loads(text)
        except json.JSONDecodeError:
            try:
                yield json.loads(_fix_unescaped_newlines(text))
            except json.JSONDecodeError as e:
                logger.debug("%s %s", type(e), e)
                continue


def find_ld_json(type_: str, parser: LexborHTMLParser) -> dict | None:
    for data in ld_json_iter(parser):
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") == type_:
                    return item
        elif isinstance(data, dict) and data.get("@type") == type_:
            return data
    return None
