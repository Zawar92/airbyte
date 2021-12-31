#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_ import Source

if __name__ == "__main__":
    source = Source()
    launch(source, sys.argv[1:])
