from importlib import metadata


def get_version(distribution_name: str) -> str:
    """Our helper to get version of a package."""
    return metadata.version(distribution_name)
