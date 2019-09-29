import praw
import os


def run_stream(subreddit: str, min_len: int = 15):
    reddit = praw.Reddit(user_agent="my-ua", client_id=os.environ["SUBR_PARSER_ID"],
                         client_secret=os.environ["SUBR_PARSER_KEY"])

    subreddit = reddit.subreddit(subreddit)

    for submission in subreddit.stream.submissions():  # type: praw.Reddit.submission
        if len(submission.title) > 15:
            yield submission


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("subreddit")
    parser.add_argument("--min-len", "-m", default=15)
    args = parser.parse_args()

    for submission in run_stream(args.subreddit, args.min_len):
        print(f"{submission.id}, {submission.title}")