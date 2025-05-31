#!/usr/bin/env python3
"""Unit tests for client module
"""
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test that GithubOrgClient.org returns correct result"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)

        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
    f"https://api.github.com/orgs/{org_name}"
   )


    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns expected value from mocked org"""
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked.url"}

            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "http://mocked.url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo list"""
        # Simulated JSON response from GitHub
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Patch the _public_repos_url property to return a dummy URL
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://mocked.repos.url"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://mocked.repos.url")
