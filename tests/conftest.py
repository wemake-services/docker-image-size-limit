import docker
import pytest


@pytest.fixture(scope='session')
def docker_client() -> docker.DockerClient:
    """Creates docker client suitable for tests."""
    return docker.from_env()


@pytest.fixture(scope='session')
def image_name() -> str:
    """Returns image name that is used in tests."""
    return 'python:3.6.6-alpine'


@pytest.fixture(scope='session', autouse=True)
def _docker_pull_image(
    docker_client: docker.DockerClient, image_name: str,  # noqa: WPS442
) -> None:
    """Pulls docker image from Docker Hub."""
    docker_client.images.pull(image_name)
