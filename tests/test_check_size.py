# -*- coding: utf-8 -*-

from docker_image_size_limit import check_image_size


def test_check_size_binary_overflow(docker_client, image_name):
    """Checks size with binary limit."""
    overflow = check_image_size(docker_client, image_name, '1024')

    assert overflow > 0


def test_check_size_binary_correct(docker_client, image_name):
    """Checks size with binary limit."""
    overflow = check_image_size(docker_client, image_name, '1073741824')

    assert overflow < 0


def test_check_size_human_overflow(docker_client, image_name):
    """Checks size with human readable limit."""
    overflow = check_image_size(docker_client, image_name, '10MB')

    assert overflow > 0


def test_check_size_human_correct(docker_client, image_name):
    """Checks size with human readable limit."""
    overflow = check_image_size(docker_client, image_name, '10 GiB')

    assert overflow < 0
