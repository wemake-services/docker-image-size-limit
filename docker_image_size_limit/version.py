import sys

if sys.version_info >= (3, 8):  # pragma: no cover
    from importlib import metadata as importlib_metadata  # noqa: WPS433
else:  # pragma: no cover
    import importlib_metadata  # noqa: WPS440, WPS433


def get_version(distribution_name: str) -> str:
    """Our helper to get version of a package."""
    return importlib_metadata.version(distribution_name)  # type: ignore
