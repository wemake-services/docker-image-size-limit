#!/bin/bash

# Passed args from GitHub Actions:
: "${INPUT_IMAGE:=$1}"  # Required
: "${INPUT_SIZE:=$2}"  # Required
: "${INPUT_MAX_LAYERS:=$3}"  # Optional
: "${INPUT_SHOW_CURRENT_SIZE:=$4}"  # Optional
: "${INPUT_EXIT_ZERO:=$5}"  # Optional

# Default values, needed because `Dockerfile` can be used directly:
# These values must match ones in `action.yml`!
: "${INPUT_MAX_LAYERS:=-1}"
: "${INPUT_SHOW_CURRENT_SIZE:=false}"
: "${INPUT_EXIT_ZERO:=false}"

# Diagnostic output:
echo "Using image: $INPUT_IMAGE"
echo "Size limit: $INPUT_SIZE"
echo "Max layers: $INPUT_MAX_LAYERS"
echo "Show Current Size: $INPUT_SHOW_CURRENT_SIZE"
echo "Exit Zero: $INPUT_EXIT_ZERO"
echo 'disl --version:'
disl --version
echo '================================='
echo

SHOW_CURRENT_SIZE_FLAG=''
if [ "$INPUT_SHOW_CURRENT_SIZE" = 'true' ]; then
  SHOW_CURRENT_SIZE_FLAG='--current-size'
fi

EXIT_ZERO_FLAG=''
if [ "$INPUT_EXIT_ZERO" = 'true' ]; then
  EXIT_ZERO_FLAG='--exit-zero'
fi


# Runs disl:
output=$(disl "$INPUT_IMAGE" "$INPUT_SIZE" --max-layers="$INPUT_MAX_LAYERS" "$SHOW_CURRENT_SIZE_FLAG" "$EXIT_ZERO_FLAG")
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
