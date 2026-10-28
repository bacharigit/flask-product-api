
import json
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

URL = "http://flask:5000/api/hello"
CHECK_INTERVAL = 30
TIMEOUT = 5


def check_api():
    start = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()

    status = None
    state = "DOWN"
    error_message = None

    try:
        with urlopen(URL, timeout=TIMEOUT) as response:
            status = response.status

        state = "UP" if 200 <= status < 300 else "DOWN"

    except HTTPError as error:
        status = error.code
        error_message = str(error)

    except (URLError, TimeoutError, OSError) as error:
        error_message = str(error)

    elapsed = time.perf_counter() - start

    record = {
        "@timestamp": timestamp,
        "service": {"name": "flask"},
        "event": {"dataset": "api.health_check"},
        "monitor": {"status": state},
        "http": {"response": {"status_code": status}},
        "url": {"full": URL},
        "event.duration": int(elapsed * 1_000_000_000),
        "response_time_ms": round(elapsed * 1000, 3),
    }

    if error_message:
        record["error"] = {"message": error_message}

    print(json.dumps(record), flush=True)


if __name__ == "__main__":
    print(json.dumps({
        "message": "Health monitor started",
        "interval_seconds": CHECK_INTERVAL,
        "url": URL,
    }), flush=True)

    while True:
        check_api()
        time.sleep(CHECK_INTERVAL)
