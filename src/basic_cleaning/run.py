#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning,
exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
# Following the reviewer suggestion, I add this line to make the code reproducable.
np.random.seed(42)

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go_function(args):
    '''
    returns clean_sample.csv into W&B

    input:
            input_artifact: csv
    output:
            output_artifact: csv
    '''

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info("Downloading input artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    data_frame = pd.read_csv(artifact_local_path)

    # Drop outliers
    idx = data_frame['price'].between(args.min_price, args.max_price)
    data_frame = data_frame[idx].copy()
    # Convert last_review to datetime
    data_frame['last_review'] = pd.to_datetime(data_frame['last_review'])

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save the cleaned data into CSV
    data_frame.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input artifact ",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Output type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Output description",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum allowed price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum allowed price",
        required=True
    )

    Args = parser.parse_args()

    go_function(Args)
