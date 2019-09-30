# Kafka Streams with Faust
A test on using Faust, this app uses `kafka-python` and `praw` libraries to stream Reddit 
posts from a subreddit to a Kafka cluster so that Faust can consume them. As a test of 
Fausts ability to deseralize arbitary objects, the `praw.Reddit.Submission` objects that
represent a Reddit post are not manipulated in anyway and are simply seralized to bytes 
as-is. Faust is then used to pull the messages down and de-seralizes each submission back 
into `praw.Reddit.Submission` objects.

## Examples
Start Zookeeper and Kafka
```bash
$ zookeeper-server-start.sh config/zookeeper.properties
$ kafka-server-start.sh config/server.properties
```

To run the producer, simply pass it a subreddit through the CLi
```bash
$ python subreddit-producer.py programming
INFO:root:Sending submission: db59gv - On the Expressive Power of Programming Languages [PWLConf 2019]
INFO:root:Sending submission: db6oe9 - When TDD Is Not a Good Fit
INFO:root:Sending submission: db6t0w - Sound Healing Mobile App for Patients - Portfolio
```
By default, `praw` will first yield 100 historical submissions before starting to stream new ones.
If you wish to skip disable this behavior call the producer with `--skip-existing`
```bash
$ python subreddit-producer.py programming --skip-existing
```
To run the consumer, call it like a python module and pass the argument `worker`
```bash
$ python -m subreddit-consumer worker
┌ƒaµS† v1.8.0─┬──────────────────────────────────────────────────────-┐
│ id          │ reddit-consumer                                       │
│ transport   │ [URL('kafka://localhost:9092')]                       │
│ store       │ memory:                                               │
│ web         │ http://localhost:6066/                                │
│ log         │ -stderr- (warn)                                       │
│ pid         │ 16643                                                 │
│ hostname    │ titan                                                 │
│ platform    │ CPython 3.7.3 (Linux x86_64)                          │
│ drivers     │                                                       │
│   transport │ aiokafka=1.0.4                                        │
│   web       │ aiohttp=3.6.1                                         │
│ datadir     │ /home/whoami/dev/reddit-kafka/reddit-consumer-data    │
│ appdir      │ /home/whoami/dev/reddit-kafka/reddit-consumer-data/v1 │
└─────────────┴────────────────────────────────────────────────-──────┘
starting➢ 😊
[2019-09-29 20:37:32,893: WARNING]: db59gv - On the Expressive Power of Programming Languages [PWLConf 2019]
[2019-09-29 20:37:33,310: WARNING]: db6oe9 - When TDD Is Not a Good Fit
[2019-09-29 20:37:35,324: WARNING]: db6t0w - Sound Healing Mobile App for Patients - Portfolio
```

## Installation
The current version of RocksDB in the PyPI repository is old and will fail without the correct packages. 
Before running the  `requirements.txt` file on a Debian based distro grab all the dependancies
```bash
apt-get install build-essential libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev
```

You will also need a OAuth keys from Reddit to run PRAW. [Read more here.](https://praw.readthedocs.io/en/latest/getting_started/authentication.html)