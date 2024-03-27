# Quickstart Guide

This repo contains VHDL basics and associated tests.

## Step 1: Environment setup

This repo is intended to be run on some flavour of Linux. I do most of my dev work on Ubuntu at the moment.

### Python environment

* Create a new python venv: `python3 -m venv venv`
* Activate your new environment: `source venv/bin/activate`
* Install the required packages from `requirements.txt`: `pip install -r tools/requirements.txt`

### Install a simulator

* Install GHDL (an open source VHDL simulator): `sudo apt-get install ghdl`

## Step 2: Run a test

The entry point for all tests is through `pytest` (https://docs.pytest.org/en/7.1.x/contents.html) which can be run from the top level of this repo. 
Some useful `pytest` basics:
* `pytest --collect-only`: just find all the tests and print a list
* `pytest -k "<EXPRESSION>"`: run all tests whose name matches `EXPRESSION`. e.g. `pytest -k "pipe"`

## Step 3: Create Your Profile

Complete your profile by adding relevant information such as your name, profile picture, and any other details you'd like to share.

## Step 4: Get Started

Now that you're all set up, dive into our platform and start using it for your needs. Whether it's connecting with others, sharing content, or exploring resources, the possibilities are endless!

## Step 5: Reach Out for Help

If you have any questions or need assistance, don't hesitate to reach out to our support team. We're here to help!

That's it! You're ready to make the most of our platform. Happy exploring!
