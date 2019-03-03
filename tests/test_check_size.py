# -*- coding: utf-8 -*-

from docker_image_size_limit import check_image_size


def test_check_size_binary_overflow(docker_client, image_name):
    """Checks size with binary limit."""
    overflow = check_image_size(docker_client, image_name, '1000')

    assert overflow > 0


def test_check_size_human_overflow(docker_client, image_name):
    """Checks size with human readable limit."""
    overflow = check_image_size(docker_client, image_name, '10MB')

    assert overflow > 0
