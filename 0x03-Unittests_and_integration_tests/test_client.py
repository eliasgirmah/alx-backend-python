#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos method"""

import unittest
from unittest.mock import patch, Mock
from client import GithubOrgClient
import fixtures  # make sure fixtures.py is in the same folder or in PYTHONPATH


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Setup class-wide patch for requests.get with fixture side effects"""
        cls.org_payload = fixtures.org_payload
        cls.repos_payload = fixtures.repos_payload
        cls.expected_repos = fixtures.expected_repos
        cls.apache2_repos = fixtures.apache2_repos

        # Start patching requests.get
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Side effect function to return appropriate fixture JSON based on URL
        def side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload.get('repos_url'):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repos"""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos with a specific license"""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
