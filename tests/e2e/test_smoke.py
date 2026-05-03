import httpx


SERVICE_URLS = [
    "http://localhost:8001/health",
    "http://localhost:8002/health",
    "http://localhost:8003/health",
    "http://localhost:8004/health",
    "http://localhost:8005/health",
]


def test_all_services_are_healthy():
    for url in SERVICE_URLS:
        response = httpx.get(url, timeout=5)
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

