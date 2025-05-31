#!/usr/bin/env python3
"""Unit tests for utils module"""
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')  # Correct order: after parameterized
    def test_org(self, org_name, expected, mock_get_json):
        """Test GithubOrgClient.org returns correct data"""
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch('client.get_json')  # MUST patch get_json here too!
    def test_public_repos_url(self, mock_get_json):
        """Test GithubOrgClient._public_repos_url returns expected value"""
        # Mock the org property to avoid network calls
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value={"repos_url": "http://mocked.url"}
        ):
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "http://mocked.url")
        # Ensure get_json isn't called (since we mocked the property)
        mock_get_json.assert_not_called()