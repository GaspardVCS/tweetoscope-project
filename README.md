# Tweetoscope project

## Table of Contents 
[1. Setting up](#setting-up) <br>
[2. Run the project in local with docker-compose](#run-the-project-in-local-with-docker-compose) <br>
[3. Overview of the files](#overview-of-the-files) <br>
[3. What still needs to be done](#what-still-needs-to-be-done)

## Setting up

For this project you will need: <br>
<ol>
  <li> docker and docker-compose </li>
  <li> python 3.6 or above</li>
</ol>

### clone the project
```
git clone git@gitlab-student.centralesupelec.fr:2018vingtring/tweetoscope-2021-09.git
```
### Set up your python3 virtual environnement

In the root of your repository
```
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

## Run the project in local with docker-compose

Run the kafka server
```
docker-compose -f docker/docker-compose-middleware.yml
```
When the server is running
```
docker-compose -f docker/docker-compose-services.yml
```

If you want to launch consumers on the different topics, you can either launch the wanted python consumer, for example for the tweets topic: <br>
```
python3 kafka_consumers/tweets_consumer.py
```
It is also possible to check on all the topics at once, using tmux.<br>
First install tmux and tmuxp: <br>
```
sudo apt-get install tmux tmuxp
```
In the root of the project: 
```
tmuxp load consumer_tmuxp.json
```

## Overview of the files

### tweet_generator

### tweet_collector

### hawkes_estimator

### predictor

### learner

### kafka_consumers

### tests

## What still needs to be done