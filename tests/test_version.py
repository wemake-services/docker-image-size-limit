import subprocess


def test_disl_version() -> None:
    """Runs `disl` command with `--version` option."""
    process = subprocess.Popen(
        [
            'disl',
            '--version',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )

    assert process.returncode is None
