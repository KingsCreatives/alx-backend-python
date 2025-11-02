"""
Basic tests to verify CI/CD pipeline infrastructure
"""
import pytest
from django.test import TestCase


class BasicInfrastructureTest(TestCase):
    """Tests to verify our testing setup works"""
    
    def test_basic_math(self):
        """Verify Python works"""
        assert 1 + 1 == 2
    
    def test_string_operations(self):
        """Verify basic string operations"""
        result = "Hello" + " " + "World"
        assert result == "Hello World"
    
    def test_list_operations(self):
        """Verify list operations"""
        my_list = [1, 2, 3]
        my_list.append(4)
        assert len(my_list) == 4
        assert my_list[-1] == 4


def test_django_import():
    """Verify Django can be imported"""
    import django
    assert django.VERSION[0] >= 4  # Django 4.x or higher


def test_pytest_works():
    """Simple pytest assertion"""
    assert True is True
    assert False is not True