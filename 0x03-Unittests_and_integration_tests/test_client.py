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
    

    def test_public_repos_url(self) -> None:
        
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, mock_payload["repos_url"])

            mock_org.assert_called_once()
    

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Tests GithubOrgClient.public_repos by mocking _public_repos_url and get_json.
        """
        
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        expected_repos = ["repo1", "repo2", "repo3"]
        
        mock_get_json.return_value = test_payload

    
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test/repos"

            
            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, expected_repos)

            
            mock_public_repos_url.assert_called_once()

        mock_get_json.assert_called_once()
        
