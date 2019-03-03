# docker-image-size-limit

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.org/wemake-services/docker-image-size-limit.svg?branch=master)](https://travis-ci.org/wemake-services/docker-image-size-limit) [![Build status](https://ci.appveyor.com/api/projects/status/mpopx4wpfkrhc1sl?svg=true)](https://ci.appveyor.com/project/wemake-services/docker-image-size-limit)
[![Coverage](https://coveralls.io/repos/github/wemake-services/docker-image-size-limit/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/docker-image-size-limit?branch=master)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/docker-image-size-limit)


## Installation

```bash
pip install docker-image-size-limit
```


## Usage

We support just a single command:

```bash
$ disl your-image-name:label 300MiB
your-image-name:label exceeds 300MiB limit by 14.4 MiB
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


## Should I use it?

You can use this script instead:

```bash
LIMIT=1024
IMAGE='your-image-name:latest'

SIZE="$(docker image inspect "$IMAGE" --format='{{.Size}}')"
test "$SIZE" -gt "$LIMIT" && echo 'Limit exceeded'; false
```

But I prefer to reuse tools over
custom `bash` scripts here and there.


## License

MIT.
