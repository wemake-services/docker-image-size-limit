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


def main(prog_name: str = 'disl') -> NoReturn:  # noqa: WPS210
    """Main CLI entrypoint."""
    client = docker.from_env()
    arguments = _parse_args(prog_name=prog_name)
    extra_size, extra_layers, image_current_size = _check_image(
        client,
        image=arguments.image,
        max_size=arguments.max_size,
        max_layers=arguments.max_layers,
    )
    if arguments.current_size:
        print('{0} current size is {1}'.format(  # noqa: WPS421
            arguments.image,
            format_size(image_current_size, binary=True),
        ))

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
    if arguments.exit_zero:
        exit_code = 0
    sys.exit(exit_code)


def _check_image(
    client: docker.DockerClient,
    image: str,
    max_size: str,
    max_layers: int,
) -> Tuple[int, int, int]:
    image_info = client.images.get(image)
    image_current_size: int = image_info.attrs['Size']
    size_overflow = check_image_size(image_info, limit=max_size)
    if max_layers > 0:
        layers_overflow = check_image_layers(image_info, limit=max_layers)
    else:
        layers_overflow = 0
    return size_overflow, layers_overflow, image_current_size


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


def _parse_args(prog_name: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Keep your docker images small',
        prog=prog_name,
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
    parser.add_argument(
        '--current-size',
        action='store_true',
        help='Display the current size of the Docker image',
        default=False,
        dest='current_size',
    )
    parser.add_argument(
        '--exit-zero',
        action='store_true',
        help='Exit with 0 even if docker image size/layers exceed max_size and max-layers',  # noqa: E501
        default=False,
        dest='exit_zero',
    )
    return parser.parse_args()
