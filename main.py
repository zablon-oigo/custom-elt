import subprocess
import time
import sys


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait until PostgreSQL is ready to accept connections."""
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
            if "accepting connections" in result.stdout:
                print(f"[INFO] PostgreSQL at {host} is ready.")
                return True
        except subprocess.CalledProcessError:
            print(f"[WARN] PostgreSQL not ready on attempt {attempt}/{max_retries}. Retrying in {delay_seconds}s...")
            time.sleep(delay_seconds)

    print(f"[ERROR] PostgreSQL at {host} did not become ready after {max_retries} attempts.")
    return False


def run_command(command, env, description):
    """Run a subprocess command with error handling."""
    print(f"[INFO] Running: {description}")
    try:
        subprocess.run(command, env=env, check=True)
        print(f"[SUCCESS] {description} completed.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed during: {description}")
        print(e)
        sys.exit(1)


def main():
    # Database configurations
    source = {
        'dbname': 'source_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'source_postgres'
    }

    destination = {
        'dbname': 'destination_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'destination_postgres'
    }

    # Wait for source and destination databases
    if not wait_for_postgres(source['host']):
        sys.exit(1)
    if not wait_for_postgres(destination['host']):
        sys.exit(1)

    print("[INFO] Starting ELT process...")

    # Step 1: Dump source DB to SQL file
    dump_cmd = [
        'pg_dump',
        '-h', source['host'],
        '-U', source['user'],
        '-d', source['dbname'],
        '-f', 'data_dump.sql',
        '-w'
    ]
    run_command(dump_cmd, env={'PGPASSWORD': source['password']}, description="Dumping source database")

    # Step 2: Load dump into destination DB
    load_cmd = [
        'psql',
        '-h', destination['host'],
        '-U', destination['user'],
        '-d', destination['dbname'],
        '-a', '-f', 'data_dump.sql'
    ]
    run_command(load_cmd, env={'PGPASSWORD': destination['password']}, description="Loading dump into destination")

    print("[INFO] ELT process completed successfully.")


if __name__ == "__main__":
    main()
