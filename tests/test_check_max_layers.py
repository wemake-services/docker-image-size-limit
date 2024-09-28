from docker.models.images import Image

from docker_image_size_limit import check_image_layers


def test_check_image_layers_overflow(
    docker_image: Image,
) -> None:
    """Checks image layers with overflow."""
    overflow = check_image_layers(docker_image, 1)

    assert overflow > 0


def test_check_image_layers_correct(
    docker_image: Image,
) -> None:
    """Checks image layers with overflow."""
    overflow = check_image_layers(docker_image, 100)

    assert overflow < 0
