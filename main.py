import subprocess
import time


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
      retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                  ["pg_isready", "-h", host], check=True, capture_output=True, text=True
            )
