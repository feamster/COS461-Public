#!/bin/bash

# parse command line arguments
if [ $# -eq 1 ];then
  ROUTER=$1
else
  ROUTER="BOTH"
fi

# testing functions

function test {
  printf "\nTesting $2 with $1router\n"
  printf "____________________________\n"
  python network.py $2 $1 
  printf "\n"
}

function testAll {
  test $1 small_net.json
  test $1 small_net_events.json
  test $1 pg244_net.json
  test $1 pg244_net_events.json
  test $1 pg242_net.json
  test $1 pg242_net_events.json
}

# run tests
if [ $ROUTER == "DV" ]; then
  testAll "DV"
  exit
fi

if [ $ROUTER == "LS" ]; then
  testAll "LS"
  exit
fi

testAll "DV"
testAll "LS"
