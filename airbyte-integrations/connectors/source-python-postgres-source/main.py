#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_python_postgres_source import SourcePythonPostgresSource

if __name__ == "__main__":
    source = SourcePythonPostgresSource()
    launch(source, sys.argv[1:])
