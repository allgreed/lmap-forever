import os
import sys


def get_envvar_or_gtfo(var_name):
    try:
        return os.environ[var_name]
    except KeyError as e:
        gtfo(f"Missing required environment variable {e}")


def gtfo(reason, code=1):
    print(reason, file=sys.stderr)
    exit(1)
