"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the complete data pipeline")
    parser.add_argument("--input", "-i", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except (ValueError, OSError) as exc:
        logger.error("Unable to load input or configuration: %s", exc)
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    rows_before_validation = len(data)

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError as exc:
        logger.error("Validation failed: %s", exc)
        sys.exit(1)

    logger.info(
        "Validation complete: %s -> %s rows",
        rows_before_validation,
        len(data),
    )

    data_before = data.copy()

    try:
        cleaned_data = process_data(data, config)
    except ValueError as exc:
        logger.error("Processing failed: %s", exc)
        sys.exit(1)

    report = create_cleaning_report(data_before, cleaned_data)

    logger.info(
        "Processing complete: %s -> %s rows",
        len(data_before),
        len(cleaned_data),
    )

    try:
        save_data(cleaned_data, args.output)
    except (OSError, ValueError) as exc:
        logger.error("Unable to save output: %s", exc)
        sys.exit(1)

    logger.info("Cleaned data saved to %s", args.output)
    print(report)


if __name__ == "__main__":
    main()