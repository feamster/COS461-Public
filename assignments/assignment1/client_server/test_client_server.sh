#!/bin/bash
##
## SYNOPSIS
##    test_client_server
##
## DESCRIPTION
##    COS 461 test script for assignment 1.
##    Runs 5 different tests between each possible client/server combination.

# Check correct number of arguments
if [[ $# -ne 2 ]]; then
  printf "USAGE: $0 [python2|python3|go] [server port]\n"
  exit
fi

# take explicit lang arg
if [[ "$1" == "python2" ]]; then
    PYTHON_CALL="python2"
    LANGUAGE="python"
elif [[ "$1" == "python3" ]]; then
    PYTHON_CALL="python3"
    LANGUAGE="python"
else
    PYTHON_CALL="python3"
    LANGUAGE=$1
fi

WORKSPACE=./.workspace
numCorrect=0
TESTS_PER_IMPL=5 # REMEBER TO UPDATE THIS IF NUMBER CHANGES!!!
PORT=$2
SKIP_MESSAGE="One or both programs missing. Skipping. \n\n"
testNum=1

# Locations of student and instructor files
SFL=.. # Student file location
SCC=$SFL/client-c # Student C client
SCS=$SFL/server-c # Student C server
SPC=$SFL/client-python.py # Student python client
SPS=$SFL/server-python.py # Student python server
SGC=$SFL/client-go # Student go client
SGS=$SFL/server-go # Student go server

# function to compare message files
# $1 = first file, $2 = second file, $3 = print separator (no if 0, yes otherwise),
# $4 = print diff (no if 0, yes otherwise)
function compare {
  if diff -q $1 $2 > /dev/null; then
    printf "\nSUCCESS: Message received matches message sent!\n"      
    ((numCorrect++))
  else
    printf "\nFAILURE: Message received doesn't match message sent.\n"
    if [ $4 -ne 0 ]; then
      echo Differences:
      diff $1 $2
    fi
  fi
  if [ $3 -ne 0 ]; then
    printf "________________________________________"               
  fi
  printf "\n" 
}

# $1 = client, $2 = server, $3 = port, $4 = print separator (no if 0, yes otherwise),
# $5 = print diff (no if 0, yes otherwise)
function test {
  $2 $3 > test_output.txt &
  SERVER_PID=$!
  sleep 0.2
  $1 127.0.0.1 $3 < test_message.txt >/dev/null
  EXIT_STATUS=$?
  sleep 0.2
  kill $SERVER_PID
  wait $SERVER_PID 2> /dev/null
  sleep 0.2
  compare test_message.txt test_output.txt $4 $5
  rm -f test_output.txt
  sleep 0.2
}

#####################################################
# Tests, $1 = client, $2 = server, $3 = port
#####################################################

function all-tests {

  printf "\n$testNum. TEST SHORT MESSAGE\n"
  printf "Go Tigers!\n" > test_message.txt
  test "$1" "$2" $3 1 1
  ((testNum++))

  ###############################################################################

  printf "\n$testNum. TEST RANDOM ALPHANUMERIC MESSAGE\n"
  head -c100000 /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' > test_message.txt
  test "$1" "$2" $3 1 0
  ((testNum++))

  ###############################################################################

  printf "\n$testNum. TEST RANDOM BINARY MESSAGE\n"                                             
  head -c100000 /dev/urandom > test_message.txt
  test "$1" "$2" $3 1 0
  ((testNum++))

  ###############################################################################

  printf "\n$testNum. TEST SERVER INFINITE LOOP (multiple sequential clients to same server)\n" 
  $2 $3 > test_output.txt &
  SERVER_PID=$!
  sleep 0.2
  printf "Line 1\n" | $1 127.0.0.1 $3 >/dev/null
  sleep 0.1
  printf "Line 2\n" | $1 127.0.0.1 $3 >/dev/null
  sleep 0.1
  printf "Line 3\n" | $1 127.0.0.1 $3 >/dev/null
  sleep 0.1
  kill $SERVER_PID
  wait $SERVER_PID 2> /dev/null
  sleep 0.2
  printf "Line 1\nLine 2\nLine 3\n" > test_message.txt
  compare test_message.txt test_output.txt 1 1
  rm -f test_output.txt
  sleep 0.2
  ((testNum++))

  ###############################################################################

  # Send 10 random concurent alphanumeric messages to server.
  # Since order of sending and order of receival can differ, we sort the messages
  # on each end and see if the results match.

  printf "\n$testNum. TEST SERVER QUEUE (overlapping clients to same server)\n"                 
  rm -f test_message.txt
  stdbuf -i0 -o0 $2 $3 > test_output.txt &
  SERVER_PID=$!
  sleep 0.2
  for i in {0..9}; do
  	(timeout 1 cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' ; echo) | tee test_message$i.txt | $1 127.0.0.1 $3 >/dev/null &
    CLIENT_PID[$i]=$!
  done
  sleep 2
  for i in {0..9}; do
  	cat test_message$i.txt >> test_message.txt
  done
  sort test_message.txt > test_message_sorted.txt
  rm -f test_message.txt
  kill $SERVER_PID
  wait $SERVER_PID 2> /dev/null
  sleep 1
  sort test_output.txt > test_output_sorted.txt
  rm -f test_output.txt
  compare test_message_sorted.txt test_output_sorted.txt 0 0
  rm -f test_output_sorted.txt test_message_sorted.txt
  sleep 0.2
  ((testNum++))
}

function handle_interrupt {
  kill $SERVER_PID 2> /dev/null
  wait $SERVER_PID &> /dev/null
  for i in {0..9}; do
    kill ${CLIENT_PID[$i]} 2> /dev/null
    wait ${CLIENT_PID[$i]} &> /dev/null
  done
  rm -rf $WORKSPACE
  echo ""
  exit 1
}
# Kill server in case of SIGINT so port is correctly freed
trap handle_interrupt SIGINT

####################################################
# RUN TESTS
####################################################

rm -rf $WORKSPACE
mkdir $WORKSPACE
cd $WORKSPACE

printf "================================================================\n" 
printf "Testing C client against C server (1/4)                         \n" 
printf "================================================================\n" 

if [[ -f $SCC && -f $SCS ]]; then
  all-tests $SCC $SCS $PORT
else
  printf "\n$SKIP_MESSAGE"
  ((testNum+=$TESTS_PER_IMPL))
fi

if [[ $LANGUAGE == "python" ]]; then

  printf "================================================================\n" 
  printf "Testing Python client against Python server (2/4)               \n" 
  printf "================================================================\n" 

  if [[ -f $SPC && -f $SPS ]]; then
    all-tests "$PYTHON_CALL $SPC" "$PYTHON_CALL $SPS" $PORT
  else
    printf "\n$SKIP_MESSAGE"
    ((testNum+=$TESTS_PER_IMPL))
  fi

  printf "================================================================\n" 
  printf "Testing C client against Python server (3/4)                    \n" 
  printf "================================================================\n" 

  if [[ -f $SCC && -f $SPS ]]; then
    all-tests $SCC "$PYTHON_CALL $SPS" $PORT
  else
    printf "\n$SKIP_MESSAGE"
    ((testNum+=$TESTS_PER_IMPL))
  fi

  printf "================================================================\n" 
  printf "Testing Python client against C server (4/4)                    \n" 
  printf "================================================================\n" 

  if [[ -f $SPC && -f $SCS ]]; then
    all-tests "$PYTHON_CALL $SPC" $SCS $PORT
  else
    printf "\n$SKIP_MESSAGE"
    ((testNum+=$TESTS_PER_IMPL))
  fi

elif [[ $LANGUAGE == "go" ]]; then

  printf "================================================================\n" 
  printf "Testing Go client against Go server (2/4)                       \n" 
  printf "================================================================\n" 

  if [[ -f $SGC && -f $SGS ]]; then
    all-tests $SGC $SGS $PORT
  else
    printf "\n$SKIP_MESSAGE"
    ((testNum+=$TESTS_PER_IMPL))
  fi

  printf "================================================================\n" 
  printf "Testing C client against Go server (3/4)                        \n" 
  printf "================================================================\n" 

  if [[ -f $SCC && -f $SGS ]]; then
    all-tests $SCC $SGS $PORT
  else
    printf "\n$SKIP_MESSAGE"
    ((testNum+=$TESTS_PER_IMPL))
  fi

  printf "================================================================\n" 
  printf "Testing Go client against C server (4/4)                        \n" 
  printf "================================================================\n" 

  if [[ -f $SGC && -f $SCS ]]; then
    all-tests $SGC $SCS $PORT
  else
    printf "\n$SKIP_MESSAGE"
    ((testNum+=$TESTS_PER_IMPL))
  fi

else
  printf "Language invalid (must be python or go)\n\n"
  ((testNum+=3*TESTS_PER_IMPL))
fi

rm -rf $WORKSPACE

#####################################################
# Summary Results
#####################################################

printf "================================================================\n\n"
printf "TESTS PASSED: $numCorrect/$((testNum-1))\n"
