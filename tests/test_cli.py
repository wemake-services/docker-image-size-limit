# -*- coding: utf-8 -*-

import subprocess


def test_disl_exceeds_limit(docker_client, image_name):
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
    assert 'exceeds' in output
    assert image_name in output


def test_disl_normal(docker_client, image_name):
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
