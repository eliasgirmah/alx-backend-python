#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos method"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures


@parameterized_class((
    "org_payload",
    "repos_payload",
    "expected_repos",
    "apache2_repos"
), [
    (
        fixtures.org_payload,
        fixtures.repos_payload,
        fixtures.expected_repos,
        fixtures.apache2_repos,
    )
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get('repos_url'):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos returns expected repo names"""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test GithubOrgClient.public_repos returns only apache2 licensed repos"""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
