#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Test the access_nested_map function from utils"""
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map,path), expected)
    

    @parameterized.expand([
            ({}, ("a",), KeyError, "a"),
            ({"a": 1}, ("a", "b"), KeyError, "b"),
        ])
    def test_access_nested_map_exception(self,nested_path,path, expected_exception, expected_msg):
        with self.assertRaisesRegex(expected_exception, expected_msg):
            access_nested_map(nested_path, path)

    
    