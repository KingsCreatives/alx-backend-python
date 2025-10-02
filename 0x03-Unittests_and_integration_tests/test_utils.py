#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

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


class TestMemoize(unittest.TestCase):
    """
    Tests the memoize decorator from utils.
    """
    def test_memoize(self):
        """
        Tests that a_method is only called once when a_property is accessed twice.
        """
        class TestClass:
            """Class for testing memoization."""

            def a_method(self):
                """Method to be memoized."""
                return 42

            @memoize
            def a_property(self):
                """Property decorated with memoize."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42


            test_instance = TestClass()

            
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_a_method.assert_called_once()