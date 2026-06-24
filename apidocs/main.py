import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parent.parent

# Each service's base URL can be overridden per machine via env vars,
# mirroring the multi-machine setup in the project README.
SERVICES = [
    {"name": "Catalog",   "dir": ROOT / "catalog",   "url": os.environ.get("CATALOG_URL",   "http://127.0.0.1:8000")},
    {"name": "Order",     "dir": ROOT / "order",     "url": os.environ.get("ORDER_URL",     "http://127.0.0.1:8001")},
    {"name": "Warehouse", "dir": ROOT / "warehouse", "url": os.environ.get("WAREHOUSE_URL", "http://127.0.0.1:8002")},
]

# We import each service in its own subprocess (with a throwaway working
# directory) so their identically named `main`/`models`/`db` modules don't
# clash, and so the .db files they create on import land in a temp dir.
_DUMP_CODE = (
    "import json, sys; "
    "sys.path.insert(0, sys.argv[1]); "
    "import main; "
    "print(json.dumps(main.app.openapi()))"
)


def load_spec(service: dict) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, "-c", _DUMP_CODE, str(service["dir"])],
            cwd=tmp, capture_output=True, text=True, check=True,
        )
    return json.loads(result.stdout)


def build_combined() -> dict:
    """Merge the three services' OpenAPI specs into one document."""
    combined = {
        "openapi": "3.1.0",
        "info": {
            "title": "E-commerce Microservices — Combined API",
            "version": "1.0.0",
            "description": "Combined OpenAPI docs for the Catalog, Order and Warehouse "
                           "services. Operations are grouped by service.",
        },
        "tags": [{"name": s["name"]} for s in SERVICES],
        "paths": {},
        "components": {"schemas": {}},
    }

    for service in SERVICES:
        name = service["name"]
        spec = load_spec(service)
        schemas = spec.get("components", {}).get("schemas", {})

        # Namespace schema names (e.g. StatusResponse exists in all three) so
        # they don't overwrite each other. The trailing quote in the $ref
        # pattern keeps "Order" from also matching "OrderItems".
        spec_str = json.dumps(spec)
        for old in schemas:
            spec_str = spec_str.replace(
                f'"#/components/schemas/{old}"',
                f'"#/components/schemas/{name}.{old}"',
            )
        spec = json.loads(spec_str)

        for old, schema in spec.get("components", {}).get("schemas", {}).items():
            combined["components"]["schemas"][f"{name}.{old}"] = schema

        for path, item in spec["paths"].items():
            for operation in item.values():
                if isinstance(operation, dict):
                    operation["tags"] = [name]
                    # Lets Swagger UI's "Try it out" hit the real service.
                    operation["servers"] = [{"url": service["url"]}]
            combined["paths"][path] = item

    return combined


COMBINED = build_combined()

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/openapi.json", include_in_schema=False)
def combined_openapi():
    return JSONResponse(COMBINED)


@app.get("/docs", include_in_schema=False)
def combined_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="E-commerce Microservices — API Docs",
    )
