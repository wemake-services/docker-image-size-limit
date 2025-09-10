import pathlib
import sys

from docker_image_size_limit import main

if __name__ == '__main__':  # pragma: no cover
    interpreter_binary_name = pathlib.Path(sys.executable).name
    main(
        prog_name=f'{interpreter_binary_name} -m docker_image_size_limit',
    )
