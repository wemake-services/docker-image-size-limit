import sys

import pytest

from docker_image_size_limit import main


def test_main_overflow(
    image_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Checks size with binary limit."""
    monkeypatch.setattr(sys, 'argv', ['', image_name, '1 MB'])
    with pytest.raises(SystemExit) as exit_value:
        main()
    assert exit_value.value.code == 1  # noqa: WPS441


def test_main_correct(
    image_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Checks size with binary limit."""
    monkeypatch.setattr(sys, 'argv', ['', image_name, '1 GB'])
    with pytest.raises(SystemExit) as exit_value:
        main()
    assert exit_value.value.code == 0  # noqa: WPS441
