#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos using fixtures"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class MockResponse:
    """Mock response object for requests.get"""
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return fixture data based on URL"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            else:
                return MockResponse(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list from fixtures"""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtering by license returns expected list"""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
