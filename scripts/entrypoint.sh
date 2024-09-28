#!/bin/bash

# Default values:
: "${INPUT_MAX_LAYERS:=-1}"

# Diagnostic output:
echo "Using image: $INPUT_IMAGE"
echo "Size limit: $INPUT_SIZE"
echo "Max layers: $INPUT_MAX_LAYERS"
echo 'disl --version:'
disl --version
echo '================================='
echo

# Runs disl:
output=$(disl "$INPUT_IMAGE" "$INPUT_SIZE" --max-layers="$INPUT_MAX_LAYERS")
status="$?"

# Sets the output variable for Github Action API:
# See: https://help.github.com/en/articles/development-tools-for-github-action
echo "output=$output" >> $GITHUB_OUTPUT
echo '================================'
echo

# Fail the build in case status code is not 0:
if [ "$status" != 0 ]; then
  echo 'Failing with output:'
  echo "$output"
  echo "Process failed with the status code: $status"
  exit "$status"
fi
