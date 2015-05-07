#!/bin/bash
# [w]ait [u]ntil [p]ort [i]s [a]ctually [o]pen
[ -n "$1" ] && [ -n "$2" ] && while ! curl --output /dev/null \
  --silent --head --fail \
  http://${1}:${2}; do sleep 1 && echo -n .; done;
exit $?
