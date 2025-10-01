#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json

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

    

class TestGetJson(unittest.TestCase):
    """
    Tests the get_json function from utils, mocking external HTTP calls.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload,mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result,test_payload)