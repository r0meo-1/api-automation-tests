from __future__ import annotations

import threading
import pytest
import requests
from qa_portfolio.server import make_server


@pytest.fixture(scope="session")
def base_url():
    server = make_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    url = f"http://{host}:{port}"
    requests.get(f"{url}/health", timeout=2).raise_for_status()
    try:
        yield url
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.fixture()
def api(base_url):
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    try:
        yield session, base_url
    finally:
        session.close()
