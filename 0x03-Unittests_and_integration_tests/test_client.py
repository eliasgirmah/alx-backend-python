#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures  # Ensure this module contains the necessary fixtures

@parameterized_class([
    {
        'org_payload': fixtures.org_payload,
        'repos_payload': fixtures.repos_payload,
        'expected_repos': fixtures.expected_repos,
        'apache2_repos': fixtures.apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define side_effect function to return appropriate mock responses
        def side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get('repos_url'):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repository names"""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repositories by license"""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
