#!/usr/bin/env python3
"""Unit tests for utils module
"""
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')  # PATCH MUST BE AFTER parameterized
    def test_org(self, org_name, expected, mock_get_json):  # parameters: org_name, expected, then mock
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked.url"}

            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "http://mocked.url")
