#!/bin/bash

sudo mn -c
pgrep -f python | xargs kill -9
