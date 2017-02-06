#!/bin/bash

# Check correct number of arguments
if [ $# -ne 2 ];then
  printf "USAGE: $0 [python|go] [server port]\n"
  exit
fi
LANGUAGE=$1
PORT=$2
ALL_CORRECT=true

# function to compare message files
function compare {
  if diff -q test_message.txt test_output.txt; then
    printf "\nSUCCESS: Message received matches message sent!\n"
  else
    ALL_CORRECT=false
    diff test_message.txt test_output.txt
  fi
  printf "________________________________________\n\n"
}

function test {
  printf "Go Tigers!\n" > test_message.txt
  $2 $3 > test_output.txt &
  sleep 1
  $1 127.0.0.1 $3 < test_message.txt
  sleep 1
  kill $!
  sleep 1
  compare
  rm -f test_output.txt
}

# Print header
printf "\nTESTING CLIENT/SERVER IMPLEMENTATIONS\n"
printf "_________________________________________\n\n"

###############################################
# Run tests
###############################################
printf "\nTesting C client -> C server\n\n"
test ./client-c ./server-c $PORT

if [ $LANGUAGE == "python" ]; then
  printf "Testing Python client -> Python server\n\n"
  test "python client-python.py" "python server-python.py" $PORT

  printf "\nTesting Python client -> C server\n\n"
  test "python client-python.py" ./server-c $PORT

  printf "\nTesting C client -> Python server\n\n"
  test ./client-c "python server-python.py" $PORT
fi

if [ $LANGUAGE == "go" ]; then
  printf "\nTesting Go client -> Go server\n\n"
  test ./client-go ./server-go $PORT

  printf "Testing Go client -> C server\n\n"
  test ./client-go ./server-c $PORT

  printf "Testing C client -> Go server\n\n"
  test ./client-c ./server-go $PORT
fi

###############################################
# Results message
###############################################
if [ $ALL_CORRECT == true ]; then
  printf "\SUCCESS: Ypu passed all the tests here!\n"
  printf "However, these are not the only tests we will use for grading.\n"
  printf "Double check the client/server specifications in the assignment "
  printf "before submitting.\n"
else
  printf "At least 1 of the above tests didn't pass.\n"
  printf "Check the client/server specifications and debugging tips in the assignment.\n"
fi
