#!/usr/bin/env bash
cd "$(dirname "${BASH_SOURCE}")"
virtualenv env
env/bin/pip install tweepy
chmod 755 index.py
