import subprocess
import time


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
