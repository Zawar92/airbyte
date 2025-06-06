#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from samples.test_data_for_tranform import input_test_data, output_test_data


def test_transform_data(components_module):
    """
    As far as we transform the data within the generator object,
    we use list() to have the actual output for the test assertion.
    """
    transform_data = components_module.transform_data
    assert list(transform_data(input_test_data)) == output_test_data
