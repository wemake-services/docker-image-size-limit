# -*- coding: utf-8 -*-

import argparse
import sys
import pkg_resources

from docker import from_env
from humanfriendly import parse_size, format_size

_version = pkg_resources.get_distribution(
    'docker_image_size_limit',
).version


def main():
    client = from_env()
    arguments = _parse_args()
    oversize = check_image_size(arguments.image, arguments.size)

    if oversize:
        print('{0} exceeds {1} limit by {2}'.format(
            arguments.image,
            arguments.size,
            format_size(oversize, binary=True),
        ))
        sys.exit(1)


def check_image_size(image: str, size: str) -> int:
    image_size = client.images.get(image).attrs['Size']
    image_limit = parse_size(size, binary=True)

    if image_size > image_limit:
        return image_limit - image_size
    return 0


def _parse_args():
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


if __name__ == '__main__':
    main()
