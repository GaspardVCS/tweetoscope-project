# Tweetoscope project

## Table of Contents 
[1. Setting up](#setting-up) <br>
[2. Run the project in local with docker-compose](#run-the-project-in-local-with-docker-compose) <br>
[3. Kubernetes](#kubernetes) <br>
[4. Overview of the files](#overview-of-the-files) <br>
[5. What still needs to be done](#what-still-needs-to-be-done)

## Setting up

For this project you will need: <br>
<ol>
  <li> docker and docker-compose </li>
  <li> python 3.6 or above</li>
  <li> minikube</li>
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

## Kubernetes

### On minikube

Start minikube
```
minikube start
```
Once it has started, deploy the kafka server:
```
kubectl apply -f kubernetes/kafka-zookeeper.yml
```
Check that the two pods are runnning:
```
kubectl get pod
```
If so, deploy the services:
```
kubectl apply -f kubernetes/services.yml
```
Once everything is runnig, you can check the messages send to the alert topic or to the stat topic (Change the name to what you see in your terminal)
```
kubectl logs stat-deployment-7564db7ffd-ptg2t
```
If you want to add replicas of any component, for example the learner, run:
```
kubectl scale --replicas=3 deployment/learner-deployment
```

### On Intercel

To deploy on Intercell, you will need to connect to your student-machine. <br>

Copy the kafka-zookeeper-intercell.yml and services-intercell.yml on your machine. <br> 

Adapt the namespace to your machine id in both files. <br>

You can now launch every kubernetes by precising the namespace in the beginning of your command by "kubeclt -n cpusdi1_XX" (instead of just kubectl)

## Overview of the files

### tweet_generator
Tweet generator folder.

### tweet_collector
tweet.py: implements the Tweet object <br>
cascade.py: implements the Cascade object <br>
processor.py: implements the Processor object <br>
main_tweet_collector.py: main file to launch to start the tweet collector. <br>
tweetoscopeCollectorParams.py: implements an object to reads the collector pameters file. <br>
collector-params*: text files that give the useful parameters to launch the collector.


### hawkes_estimator
estimator.py: implements the Estimator object<br>
main_estimator.py: file to start the Hawkes estimator.

### predictor
predictor.py: implements the Predictor object.
main_predictor.py: file to start the predictor.


### learner
learner.py: implements the Learner object. Each random forest model retrained everytime 20 new samples have be send to them. They retrain on all the dataset until it reaches a length of 1000.
main_learner.py: file to start the learners. 

### kafka_consumers

### tests
Folder where all the unit tests are. We use Pytest to run our unit tests.

## What still needs to be done
1. change dockerfile images from ubuntu to alpine. I had problem with the python imports, so I kept this change for later. But the tweet generator has an alpine image
2. Find the best hyperparameters for the random forests. To do so, we can run the simulation for a certain time. Write down the sample send in the coresponding kafka topic. From that we can create a train, test and validation set. Thanks to a GridSearch we would then be able to find the best hyperparameters for the RandomForest models, for the time windows 600 and 1200.
3. Graphana
4. In the cicd, there are still problems with the unit test pipeline. Basically, it failed because it didn't find the pip/pip3 command. But it worked at least once with the exact same code, so I don't understand the problem. I kept it for later if there is still time to investigate.
5. If point 4. is done, add some real unit tests, not just the fake ones created to test the cicd pipeline.
6. Automatic code quality report