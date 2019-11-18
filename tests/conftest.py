# -*- coding: utf-8 -*-

import docker
import pytest


@pytest.fixture(scope='session')
def docker_client():
    """Creates docker client suitable for tests."""
    return docker.from_env()


@pytest.fixture(scope='session')
def image_name():
    """Returns image name that is used in tests."""
    return 'python:3.6.6-alpine'


@pytest.fixture(scope='session', autouse=True)
def docker_pull_image(docker_client, image_name):  # noqa: WPS442
    """Pulls docker image from Docker Hub."""
    return docker_client.images.pull(image_name)
