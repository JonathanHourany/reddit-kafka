"""Listens to a topic on a Kafka cluster and processes praw Submission objects"""

import pickle

import faust
import praw

app = faust.App("reddit-consumer", broker="kafka://localhost:9092", store="memory://")
programming_subreddit = app.topic("programming", value_serializer="raw")


@app.agent(programming_subreddit)
async def process(subreddit: faust.Stream[praw.Reddit.submission]):
    async for bytes_payload in subreddit:
        submission = pickle.loads(bytes_payload, fix_imports=False, encoding="bytes")
        print(f"{submission.id}: {submission.title}")


if __name__ == "__main__":
    app.main()
