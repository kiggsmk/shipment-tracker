import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
import pybreaker

from app.core.config import (
    TRUCK_SERVICE_URL,
    TRUCK_SERVICE_TIMEOUT,
    TRUCK_SERVICE_RETRIES,
    TRUCK_SERVICE_RETRY_DELAY,
    CIRCUIT_BREAKER_FAIL_MAX,
    CIRCUIT_BREAKER_RESET_TIMEOUT
)

# 🔥 Circuit Breaker
breaker = pybreaker.CircuitBreaker(
    fail_max=CIRCUIT_BREAKER_FAIL_MAX,
    reset_timeout=CIRCUIT_BREAKER_RESET_TIMEOUT
)


# 🔁 Retry + Timeout
@retry(
    stop=stop_after_attempt(TRUCK_SERVICE_RETRIES),
    wait=wait_fixed(TRUCK_SERVICE_RETRY_DELAY)
)
def _make_request(url: str, headers: dict):
    with httpx.Client(timeout=TRUCK_SERVICE_TIMEOUT) as client:
        response = client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Truck service returned {response.status_code}")

        return response.json()


# 🔌 Circuit Breaker wrapper
@breaker
def get_truck(truck_id: str, token: str):
    url = f"{TRUCK_SERVICE_URL}/trucks/{truck_id}"
    headers = {"Authorization": f"Bearer {token}"}

    return _make_request(url, headers)


# ✅ Public validation function
def validate_truck_ownership(truck_id: str, user_id: str, token: str):
    try:
        truck = get_truck(truck_id, token)
        return truck.get("user_id") == user_id

    except pybreaker.CircuitBreakerError:
        raise Exception("Truck service unavailable (circuit breaker open)")

    except Exception:
        return False