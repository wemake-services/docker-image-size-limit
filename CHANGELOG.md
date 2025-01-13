# Version history

We follow Semantic Version.


## Version 2.1.0

### Features

- Adds `--current-size` flag to show the current size of the docker image
- Adds `--exit-zero` flag to force the exit code
  to be 0 even if there are errors
- Adds `__main__.py` entrypoint to be able to run
  it via `python -m docker_image_size_limit`


## Version 2.0.0

### Features

- Adds `--max-layers` flag to lint the maximum number of layers


## Version 1.1.0

### Features

- Drops `python3.8` support

### Misc

- Unlocked `urllib3`, `requests`, and `docker-py`


## Version 1.0.1

### Misc

- Locked version of `urllib3` to `<2` as workaround for https://github.com/docker/docker-py/issues/3113
- Locked version of `requests` to `<2.29`  as workaround for https://github.com/docker/docker-py/issues/3113


## Version 1.0.0

### Features

- Drops `python3.7` support
- Adds `python3.11` support


## Version 0.5.0

### Features

- Drops `python3.6` support
- Adds `python3.10` support


## Version 0.4.1

## Misc

- Updates a lot of dependencies


## Version 0.4.0

### Features

- Adds `python3.9` support

## Misc

- Updates a lot of dev dependencies


## Version 0.3.0

### Features

- Adds Github Action support
- Adds `python3.8` support
- Adds `Dockerfile` and dockerhub integration

### Misc

- Updates `poetry` version
- Updates lots of dependencies


## Version 0.2.0

### Features

- Now real negative size is returned when limit is bigger than image
- Adds `py.typed` file to package the type annotation with the code

### Misc

- Updates `wemake-python-styleguide`
- Uses `nitpick`
- Adds more docs


## Version 0.1.0

- Initial release
