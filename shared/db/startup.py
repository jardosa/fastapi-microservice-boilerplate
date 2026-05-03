import logging
import time

from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


def create_all_with_retry(metadata, engine, attempts: int = 10, delay_seconds: float = 2.0) -> None:
    last_error: OperationalError | None = None
    for attempt in range(1, attempts + 1):
        try:
            metadata.create_all(bind=engine)
            return
        except OperationalError as exc:
            last_error = exc
            logger.warning("Database is not ready, retrying schema creation (%s/%s)", attempt, attempts)
            time.sleep(delay_seconds)
    if last_error is not None:
        raise last_error
