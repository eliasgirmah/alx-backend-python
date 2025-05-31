#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

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

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value from mocked org"""
        with patch('client.GithubOrgClient.org', new_callable=property) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked.url"}

            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "http://mocked.url")
