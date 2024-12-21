import subprocess
import sys
from os.path import basename


def test_disl_exceeds_limit(image_name: str) -> None:
    """Runs `disl` command with met limit."""
    process = subprocess.Popen(
        [
            'disl',
            image_name,
            '5MB',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    assert process.returncode == 1
    assert 'limit by' in output
    assert image_name in output


def test_disl_normal(image_name: str) -> None:
    """Runs `disl` command with unmet limit."""
    process = subprocess.Popen(
        [
            'disl',
            image_name,
            '1 GiB',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )

    assert process.returncode is None


def test_disl_max_layers(image_name: str) -> None:
    """Runs `disl` command with unmet limit."""
    process = subprocess.Popen(
        [
            'disl',
            image_name,
            '1 GiB',
            '--max-layers',
            '1',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    assert process.returncode == 1
    assert 'maximum layers by' in output
    assert image_name in output


def test_disl_current_size(image_name: str) -> None:
    """Runs `disl` command with --current-size flag."""
    process = subprocess.Popen(
        [
            'disl',
            image_name,
            '1 kb',
            '--current-size',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    assert process.returncode == 1
    assert 'current size is' in output
    assert image_name in output


def test_disl_exit_zero(image_name: str) -> None:
    """Runs `disl` command with --exit-zero flag."""
    process = subprocess.Popen(
        [
            'disl',
            image_name,
            '1 kb',
            '--current-size',
            '--exit-zero',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    assert process.returncode == 0
    assert 'current size is' in output
    assert image_name in output


def test_docker_image_size_limit_as_module(image_name: str) -> None:
    """Runs `disl` command with --exit-zero flag."""
    interpreter_binary_name = basename(sys.executable)
    process = subprocess.Popen(
        [
            '{0}'.format(interpreter_binary_name),
            '-m',
            'docker_image_size_limit',
            image_name,
            '1 kb',
            '--current-size',
            '--exit-zero',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    assert process.returncode == 0
    assert 'current size is' in output
    assert image_name in output


def test_docker_image_size_limit_as_module_help_flag(image_name: str) -> None:  # noqa: WPS118,E501
    """Runs `disl` command via it python module."""
    interpreter_binary_name = basename(sys.executable)
    process = subprocess.Popen(
        [
            '{0}'.format(interpreter_binary_name),
            '-m',
            'docker_image_size_limit',
            '--help',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    assert process.returncode == 0
    assert 'docker_image_size_limit' in output
