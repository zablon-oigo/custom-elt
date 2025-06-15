import subprocess
import time


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
