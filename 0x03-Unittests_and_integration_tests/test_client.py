import unittest
from unittest.mock import PropertyMock, Mock, patch
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
from typing import Dict, List
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
    

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: dict,
        license_key: str,
        expected: bool
    ) -> None:
        """
        Tests that GithubOrgClient.has_license returns the correct boolean value.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
        

@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), 
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos. 
    Mocks only external HTTP calls.
    """
    
    org_payload: Dict
    repos_payload: List[Dict]
    expected_repos: List[str]
    apache2_repos: List[str]

    @classmethod
    def setUpClass(cls):
        """
        Mocks requests.get to return fixtures based on the URL using side_effect.
        This sets up the mock for the entire test class.
        """
       
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        
        org_url = "https://api.github.com/orgs/google"
        repos_url = cls.org_payload["repos_url"]
        
       
        def side_effect(url):
            """Returns the correct Mock response based on the URL."""
            mock_response = Mock()
            if url == org_url:
                mock_response.json.return_value = cls.org_payload
            elif url == repos_url:
                mock_response.json.return_value = cls.repos_payload
            else:
                raise ValueError(f"URL not mocked: {url}")
            return mock_response

        
        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stops the patcher to restore the original requests.get method.
        """
        cls.get_patcher.stop()

