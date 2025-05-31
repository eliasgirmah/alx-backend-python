#!/usr/bin/env python3
"""Integration test for GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get to return fixtures depending on URL"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Side effect function to return appropriate JSON depending on URL
        def get_json(url, *args, **kwargs):
            if url == org_payload["repos_url"]:
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            elif url == f"https://api.github.com/orgs/{org_payload['login']}":
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            else:
                raise ValueError(f"Unmocked URL: {url}")

        cls.mock_get.side_effect = get_json

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license key"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
