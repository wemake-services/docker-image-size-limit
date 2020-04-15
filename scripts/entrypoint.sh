#!/bin/bash

# Diagnostic output:
echo "Using image: $INPUT_IMAGE"
echo "Size limit: $INPUT_SIZE"
echo 'disl --version:'
disl --version
echo '================================='
echo

# Runs disl:
output=$(disl "$INPUT_IMAGE" "$INPUT_SIZE")
status="$?"

# Sets the output variable for Github Action API:
# See: https://help.github.com/en/articles/development-tools-for-github-action
echo "::set-output name=output::$output"
echo '================================='
echo

# Fail the build in case status code is not 0:
if [ "$status" != 0 ]; then
  echo 'Failing with output:'
  echo "$output"
  echo "Process failed with the status code: $status"
  exit "$status"
fi
