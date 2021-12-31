#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_python_http_getincidence import SourcePythonHttpGetincidence

if __name__ == "__main__":
    source = SourcePythonHttpGetincidence()
    launch(source, sys.argv[1:])
