# docker-image-size-limit

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build status](https://github.com/wemake-services/docker-image-size-limit/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake-services/docker-image-size-limit/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/wemake-services/docker-image-size-limit/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-services/docker-image-size-limit)
[![Python Version](https://img.shields.io/pypi/pyversions/docker-image-size-limit.svg)](https://pypi.org/project/docker-image-size-limit/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Limit your `docker` image size with a simple CLI command.
Perfect to be used inside your CI process.

Read the [announcing post](https://sobolevn.me/2019/03/announcing-docker-image-size-limit).


## Installation

```bash
pip install docker-image-size-limit
```

Or use our [Github Action](https://github.com/wemake-services/docker-image-size-limit#github-action) or [pre-built docker image](https://github.com/wemake-services/docker-image-size-limit#docker-image).


## Usage

We support just a single command:

```bash
$ disl your-image-name:label 300MiB
your-image-name:label exceeds 300MiB limit by 114.4 MiB
```

Add `--max-layers` flag to also lint the maximum amount of layers possible
in your image:

```bash
# If your image has 7 layers:
$ disl your-image-name:label 300MiB --max-layers=5
your-image-name:label exceeds 5 maximum layers by 2

# If your image has 5 layers:
$ disl your-image-name:label 300MiB --max-layers=5
# ok!
```

Add `--current-size` flag to show the current size your image:

```bash
$ disl your-image-name:label 300MiB --current-size
your-image-name:label size is 414.4 MiB
your-image-name:label exceeds 300MiB limit by 114.4 MiB
```


Add `--exit-zero` flag to force the exit code to be 0 even if there are errors:

```bash
$ disl your-image-name:label 300MiB --exit-zero
your-image-name:label exceeds 300MiB limit by 114.4 MiB

$ echo $?
0
```

You can combine all flags together:

```bash
$ disl your-image-name:label 300MiB --max-layers=5 --current-size --exit-zero
your-image-name:label size is 414.4 MiB
your-image-name:label exceeds 300MiB limit by 114.4 MiB
your-image-name:label exceeds 5 maximum layers by 2
```

Run `disl` as a module:

```bash
$ python -m docker_image_size_limit your-image-name:label 300MiB
your-image-name:label exceeds 300MiB limit by 114.4 MiB
```



## Options

You can specify your image as:

- Image name: `python`
- Image name with tag: `python:3.6.6-alpine`

You can specify your size as:

- Raw number of bytes: `1024`
- Human-readable megabytes: `30 MB` or `30 MiB`
- Human-readable gigabytes: `1 GB` or `1 GiB`
- Any other size supported by [`humanfriendly`](https://humanfriendly.readthedocs.io/en/latest/api.html#humanfriendly.parse_size)


## Programmatic usage

You can also import and use this library as `python` code:

```python
from docker import from_env
from docker_image_size_limit import check_image_size

oversize = check_image_size(from_env(), 'image-name:latest', '1 GiB')
assert oversize < 0, 'Too big image!'  # negative oversize - is a good thing!
```

We also ship [PEP-561](https://www.python.org/dev/peps/pep-0561/)
compatible type annotations with this library.


## GitHub Action

You can also use this check as a [GitHub Action](https://github.com/marketplace/actions/docker-image-size-limit):

```yaml
- uses: wemake-services/docker-image-size-limit@master
  with:
    image: "$YOUR_IMAGE_NAME"
    size: "$YOUR_SIZE_LIMIT"
    # optional fields:
    max_layers: 5
    show_current_size: false
    exit_zero: false
```

Here's [an example](https://github.com/wemake-services/docker-image-size-limit/actions?query=workflow%3Adisl).


## Docker Image

We have a [pre-built image](https://hub.docker.com/r/wemakeservices/docker-image-size-limit) available.

First, pull our pre-built docker image:

```bash
docker pull wemakeservices/docker-image-size-limit
```

Then you can use it like so:

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock --rm \
  -e INPUT_IMAGE="$YOUR_IMAGE_NAME" \
  -e INPUT_SIZE="$YOUR_SIZE_LIMIT" \
  -e INPUT_MAX_LAYERS="$YOUR_MAX_LAYERS" \
  -e INPUT_SHOW_CURRENT_SIZE="true" \
  -e INPUT_EXIT_ZERO="true" \
  wemakeservices/docker-image-size-limit
```


## Should I use it?

You can use this script instead:

```bash
LIMIT=1024  # adjust at your will
IMAGE='your-image-name:latest'

SIZE="$(docker image inspect "$IMAGE" --format='{{.Size}}')"
test "$SIZE" -gt "$LIMIT" && echo 'Limit exceeded'; exit 1 || echo 'Ok!'
```

But I prefer to reuse tools over
custom `bash` scripts here and there.


## License

MIT.
