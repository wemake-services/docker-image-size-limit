# -*- coding: utf-8 -*-

import argparse
import sys
from typing import NoReturn

import pkg_resources
from docker import DockerClient, from_env
from humanfriendly import format_size, parse_size

_version = pkg_resources.get_distribution(
    'docker_image_size_limit',
).version


def main() -> NoReturn:
    """Main CLI entrypoint."""
    client = from_env()
    arguments = _parse_args()
    oversize = check_image_size(client, arguments.image, arguments.size)

    exit_code = 0
    if oversize > 0:
        print('{0} exceeds {1} limit by {2}'.format(  # noqa: T001
            arguments.image,
            arguments.size,
            format_size(oversize, binary=True),
        ))
        exit_code = 1
    sys.exit(exit_code)


def check_image_size(client: DockerClient, image: str, limit: str) -> int:
    """
    Checks the image size of given image name.

    Compares it to the given size in bytes or in human readable format.

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
