# -*- coding: utf-8 -*-

import pytest

from docker_image_size_limit import main, sys


def test_main_overflow(docker_client, image_name, monkeypatch):
    """Checks size with binary limit."""
    monkeypatch.setattr(sys, 'argv', ['', image_name, '1 MB'])
    with pytest.raises(SystemExit) as exit_value:
        main()
    assert exit_value.value.code == 1  # noqa: WPS441


def test_main_correct(docker_client, image_name, monkeypatch):
    """Checks size with binary limit."""
    monkeypatch.setattr(sys, 'argv', ['', image_name, '1 GB'])
    with pytest.raises(SystemExit) as exit_value:
        main()
    assert exit_value.value.code == 0  # noqa: WPS441
