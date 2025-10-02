import unittest
from unittest.mock import PropertyMock, Mock, patch
from parameterized import parameterized

from client import GithubOrgClient
from utils import get_json

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", ),
        ("abc", )
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None :
        
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)

        result = client.org

        self.assertEqual(result, test_payload)

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)