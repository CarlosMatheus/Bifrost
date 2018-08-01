# Bifrost

## Getting Started

These instructions will get you a copy of the project up and running on your local machine if you use Linux. 
Instructions for Windows and Mac are similar.

### Prerequisites

You will just have to install python and the requirements. The instructions below will show you how to do this for Linux (Ubuntu 16.04).

First, install Python3 setup tools and pip:

```
$ sudo apt-get install python3-setuptools
$ sudo easy_install3 pip
```

Then install requirements using pip:

```
$ pip install -r requirements.txt
```

### Usage:

#### Run

To run the game, go to the directory where you cloned the repository and simply run the following:

```
$ python3 bifrost.py
```

#### Set the settings up:



## About

Bifrost is a Slack bot that aim to connect your company employees.
It work by asking every one day after day to send a message throw the bot to some friend.
The message can be about anything, what matter to the bot is to track the people contact and build a map of people contact.
With this data, it is build a large database of people contacts.
This DB is periodically passed throw an algorithm to make suggestions

Project developed in 24 hours for the Code in Quero 2018 Hackathon Competition by:

* **Aloysio da Silva Galvão** - [aloysiogl](https://github.com/aloysiogl)
* **Carlos Matheus Barros da Silva** - [CarlosMatheus](https://github.com/CarlosMatheus)
* **Felipe Vieira Coimbra** - [FelipeCoimbra](https://github.com/FelipeCoimbra)
* **Luis Henrique Aguiar Lima** - [Hikkust](https://github.com/Hikkust)

## How it works

### Overview

With a certain period the bot will ask to every one on the channel to send a message to a friend.
The message should be sent throw the bot, it will work as a messager.
When the bot send a message to other person it stores that data in a database, the message and the sender and receiver.
From the data it stored, with a period, will be passed throw an algorithm to create suggestions of connections on the company.


### Structure

#### SlackBot

#### Graph Modelling

#### Hierarchical Clustering by social affinity
