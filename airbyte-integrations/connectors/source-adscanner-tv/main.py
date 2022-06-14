#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_adscanner_tv import SourceAdscannerTv

if __name__ == "__main__":
    source = SourceAdscannerTv()
    launch(source, sys.argv[1:])
