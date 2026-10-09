
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_data(df, filepath):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(filepath, index=False)

    logger.debug("Saved %s rows to %s", len(df), filepath)

    return filepath
