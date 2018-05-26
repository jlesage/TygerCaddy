#!/bin/bash

#wait for webserver to start before trying to test
sleep 5

#check to see if local webserver is serving pages
response=`curl -s -o /dev/null -I -w "%{http_code}" http://127.0.0.1`

#look for a response code of 200
if [ $response -eq "301" ] || [ $response -eq "302" ]; then
  echo "Site is live! HTTP Response $response OK"
  exit 0
else
  echo "Something went wrong! HTTP Response code was $response"
  exit 1
fi
