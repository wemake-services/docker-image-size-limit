import argparse
import os
import sys
from typing import List, NoReturn, Tuple

import docker
from docker.models.images import Image
from humanfriendly import format_size, parse_size

from docker_image_size_limit.version import get_version

#: We use this variable to show version spec.
_version = get_version(
    os.path.basename(os.path.dirname(__file__)),
)


def main() -> NoReturn:
    """Main CLI entrypoint."""
    client = docker.from_env()
    arguments = _parse_args()
    extra_size, extra_layers = _check_image(
        client,
        image=arguments.image,
        max_size=arguments.max_size,
        max_layers=arguments.max_layers,
    )

    exit_code = 0
    if extra_size > 0:
        print('{0} exceeds {1} limit by {2}'.format(  # noqa: WPS421
            arguments.image,
            arguments.max_size,
            format_size(extra_size, binary=True),
        ))
        exit_code = 1
    if extra_layers > 0:
        print('{0} exceeds {1} maximum layers by {2}'.format(  # noqa: WPS421
            arguments.image,
            arguments.max_layers,
            extra_layers,
        ))
        exit_code = 1
    sys.exit(exit_code)


def _check_image(
    client: docker.DockerClient,
    image: str,
    max_size: str,
    max_layers: int,
) -> Tuple[int, int]:
    image_info = client.images.get(image)
    size_overflow = check_image_size(image_info, limit=max_size)
    if max_layers > 0:
        layers_overflow = check_image_layers(image_info, limit=max_layers)
    else:
        layers_overflow = 0
    return size_overflow, layers_overflow


def check_image_size(
    image: Image,
    limit: str,
) -> int:
    """
    Checks the image size of given image name.

    Compares it to the given size in bytes or in human readable format.

    Args:
        image: image object from docker.
        limit: human-readable size limit.

    Returns:
        Tresshold overflow in bytes.
        Can be negative in case ``image_limit`` is bigger
        than the actual image. We only care for values ``> 0``.

    """
    image_size: int = image.attrs['Size']

    try:
        image_limit = int(limit)
    except ValueError:
        image_limit = parse_size(limit, binary=True)

    return image_size - image_limit


def check_image_layers(
    image: Image,
    limit: int,
) -> int:
    """
    Checks the number of layers in an image.

    Args:
        image: image object from docker.
        limit: maximum number of layers.

    Returns:
        Tresshold overflow in number of layers.

    """
    layers: List[str] = image.attrs['RootFS']['Layers']
    return len(layers) - limit


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
        'max_size', type=str, help='Human-readable size limit: 102 MB, 1GB',
    )
    parser.add_argument(
        '--max-layers',
        type=int,
        help='Maximum number of image layers',
        default=-1,
    )
    return parser.parse_args()
