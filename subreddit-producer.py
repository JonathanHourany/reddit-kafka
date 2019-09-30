"""Pushes praw Submission objects as raw bytes to a Kafka broker"""

import logging
import os
import pickle
from typing import Generator

import praw
from kafka import KafkaProducer

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_stream(
    subreddit: str, skip_existing=False
) -> Generator[praw.Reddit.submission]:
    """Infinitely streams posts from a given subreddit"""
    reddit = praw.Reddit(
        user_agent="my-ua",
        client_id=os.environ["SUBR_PARSER_ID"],
        client_secret=os.environ["SUBR_PARSER_KEY"],
    )

    subreddit = reddit.subreddit(subreddit)

    for submission in subreddit.stream.submissions(skip_existing=skip_existing):
        yield submission


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("subreddit", help="Subreddit to stream")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip fetching the 100 newest submissions",
    )

    args = parser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"], value_serializer=pickle.dumps
    )

    for submission in run_stream(args.subreddit):
        logger.info(f"Sending submission: {submission.id} - {submission.title}")
        producer.send(topic=f"{args.subreddit}", value=submission)
