
"""Data Processing Pipeline - CLI Template

DS 3500 - MP1
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input", "-i",
        required=True,
        type=Path,
        help="Path to the input file"
    )

    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to the YAML configuration file"
    )

    parser.add_argument(
        "--output", "-o",
        required=True,
        type=Path,
        help="Path to the output CSV file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file():
        logger.info("Input file validated: %s", filepath)
        return True
    else:
        logger.error("Input file not found: %s", filepath)
        return False


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input, args.output, args.config
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    data_before = data.copy()

    try:
        cleaned_data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(data_before, cleaned_data)
    print(report)

    logger.info(
        "Processing complete: %s → %s rows",
        report["rows_before"],
        report["rows_after"]
    )

    try:
        cleaned_data.to_csv(args.output, index=False)
    except (OSError, ValueError) as error:
        logger.error("Could not save cleaned data: %s", error)
        sys.exit(1)

    logger.info("Saved cleaned data to %s", args.output)


if __name__ == "__main__":
    main()