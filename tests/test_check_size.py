from docker.models.images import Image

from docker_image_size_limit import check_image_size


def test_check_size_binary_overflow(
    docker_image: Image,
) -> None:
    """Checks size with binary limit."""
    overflow = check_image_size(docker_image, '1024')

    assert overflow > 0


def test_check_size_binary_correct(
    docker_image: Image,
) -> None:
    """Checks size with binary limit."""
    overflow = check_image_size(docker_image, '1073741824')

    assert overflow < 0


def test_check_size_human_overflow(
    docker_image: Image,
) -> None:
    """Checks size with human readable limit."""
    overflow = check_image_size(docker_image, '10MB')

    assert overflow > 0


def test_check_size_human_correct(
    docker_image: Image,
) -> None:
    """Checks size with human readable limit."""
    overflow = check_image_size(docker_image, '10 GiB')

    assert overflow < 0
