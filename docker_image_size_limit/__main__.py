import sys
from os.path import basename

from docker_image_size_limit import main

if __name__ == '__main__':  # pragma: no cover
    interpreter_binary_name = basename(sys.executable)
    main(
        prog_name='{0} -m docker_image_size_limit'.format(
            interpreter_binary_name,
        ),
    )
