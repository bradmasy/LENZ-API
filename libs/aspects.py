import aspectlib
import logging
from django.db import transaction

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="\n----------\n%(asctime)s - %(levelname)s - %(message)s\n----------\n",
)


@aspectlib.Aspect
def log_error(target, request, *args, **kwargs):
    try:
        result = yield aspectlib.Proceed(target, request, *args, **kwargs)

    except Exception as log_exception:
        logging.error(f"Error creating LogError object: {log_exception}")

    return result
