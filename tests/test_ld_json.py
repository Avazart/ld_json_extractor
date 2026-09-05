from selectolax.lexbor import LexborHTMLParser

from ld_json_extractor import find_ld_json, ld_json_iter


def test_ld_json_iter_parses_valid_and_repaired_json() -> None:
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <!-- Standard valid LD+JSON -->
        <script type="application/ld+json">
            {"@type": "Organization", "name": "Company"}
        </script>

        <!-- Invalid LD+JSON with unescaped newline inside a string -->
        <script type="application/ld+json">
            {"@type": "Product", "description": "First line\nsecond line"}
        </script>

        <!-- Completely malformed JSON (should be ignored) -->
        <script type="application/ld+json">
            {"@type": "Article", "title":
        </script>
    </head>
    </html>
    """
    parser = LexborHTMLParser(html)
    results = list(ld_json_iter(parser))

    assert len(results) == 2
    assert results[0] == {"@type": "Organization", "name": "Company"}
    assert results[1] == {
        "@type": "Product",
        "description": "First line\nsecond line",
    }


def test_find_ld_json_handles_dicts_and_array_lists() -> None:
    html = """
    <script type="application/ld+json">
        [
            {"@type": "BreadcrumbList", "id": 1},
            {"@type": "Product", "name": "Item from array"}
        ]
    </script>
    <script type="application/ld+json">
        {"@type": "Organization", "name": "Single object"}
    </script>
    """
    parser = LexborHTMLParser(html)

    product = find_ld_json("Product", parser)
    org = find_ld_json("Organization", parser)
    missing = find_ld_json("NonExistentType", parser)

    assert product == {"@type": "Product", "name": "Item from array"}
    assert org == {"@type": "Organization", "name": "Single object"}
    assert missing is None