# -*- coding: utf-8 -*-

import argparse
import os
import sys
from typing import NoReturn

import docker
from humanfriendly import format_size, parse_size

if sys.version_info >= (3, 8):  # pragma: no cover
    from importlib import metadata as importlib_metadata  # noqa: WPS433
else:  # pragma: no cover
    import importlib_metadata  # noqa: WPS433, WPS440

#: We use this variable to show version spec.
_version = importlib_metadata.version(
    os.path.basename(os.path.dirname(__file__)),
)


def main() -> NoReturn:
    """Main CLI entrypoint."""
    client = docker.from_env()
    arguments = _parse_args()
    oversize = check_image_size(client, arguments.image, arguments.size)

    exit_code = 0
    if oversize > 0:
        print('{0} exceeds {1} limit by {2}'.format(  # noqa: WPS421
            arguments.image,
            arguments.size,
            format_size(oversize, binary=True),
        ))
        exit_code = 1
    sys.exit(exit_code)


def check_image_size(
    client: docker.DockerClient,
    image: str,
    limit: str,
) -> int:
    """
    Checks the image size of given image name.

    Compares it to the given size in bytes or in human readable format.

    Args:
        client: docker client to work with images.
        image: image name.
        limit: human-readable size limit.

    Returns:
        Tresshold overflow in bytes.
        Can be negative in case ``image_limit`` is bigger
        than the actual image. We only care for values ``> 0``.

    """
    image_size = client.images.get(image).attrs['Size']

    try:
        image_limit = int(limit)
    except ValueError:
        image_limit = parse_size(limit, binary=True)

    return image_size - image_limit


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Keep your docker images small',
    )
    parser.add_argument(
        '--version', action='version', version=_version,
    )
    parser.add_argument(
        'image', type=str, help='Docker image name to be checked',
    )
    parser.add_argument(
        'size', type=str, help='Human-readable size limit: 102 MB, 1GB',
    )
    return parser.parse_args()
