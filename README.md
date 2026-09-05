# av-ld_json_extractor

A lightweight Python library designed to extract ld+json from `<script>` tags within HTML documents

## Installation

Using [`uv`](https://github.com/astral-sh/uv):

```bash
uv add av-ld_json_extractor
```

### Quick Start

#### 1. Extract JSON-LD Data from HTML

```python
from selectolax.lexbor import LexborHTMLParser
from av_ld_json_extractor import ld_json_iter

html_content = """
<!DOCTYPE html>
<html>
<head>
    <script type="application/ld+json">
        {"@context": "[https://schema.org](https://schema.org)", "@type": "Organization", "name": "Example Corp"}
    </script>
    <script type="application/ld+json">
        {"@type": "Product", "name": "Gaming Laptop", "price": 1200}
    </script>
</head>
</html>
"""

parser = LexborHTMLParser(html_content)

for data in ld_json_iter(parser):
    print(data)
```

```
# Output:
# {'@context': '[https://schema.org](https://schema.org)', '@type': 'Organization', 'name': 'Example Corp'}
# {'@type': 'Product', 'name': 'Gaming Laptop', 'price': 1200}
```

#### 2. Find Specific @type (Objects & Lists)

```python
from selectolax.lexbor import LexborHTMLParser
from av_ld_json_extractor import find_ld_json

html_content = """
<script type="application/ld+json">
    [
        {"@type": "BreadcrumbList", "itemListElement": []},
        {"@type": "Product", "name": "Wireless Mouse", "price": 25}
    ]
</script>
"""

parser = LexborHTMLParser(html_content)

# Automatically searches inside both single JSON objects and array lists
product = find_ld_json("Product", parser)
print(product)
```

```
# Output:
# {'@type': 'Product', 'name': 'Wireless Mouse', 'price': 25}
```
