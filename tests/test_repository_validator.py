"""Tests for repository validation functionality."""

import pytest
from jupyter_ai.repository_validator import (
    RepositoryValidator,
    RepositoryInfo,
    LEGITIMATE_REPOSITORIES,
    validate_jupyter_ai_dependencies,
    check_installation_security,
)


class TestRepositoryValidator:
    """Test suite for RepositoryValidator class."""

    def test_is_legitimate_name_with_valid_package(self):
        """Test that legitimate package names are recognized."""
        validator = RepositoryValidator()
        assert validator.is_legitimate_name("jupyter_ai_router")
        assert validator.is_legitimate_name("jupyterlab_chat")
        assert validator.is_legitimate_name("jupyter-ai-router")  # with hyphens

    def test_is_legitimate_name_with_invalid_package(self):
        """Test that illegitimate package names are rejected."""
        validator = RepositoryValidator()
        assert not validator.is_legitimate_name("malicious_package")
        assert not validator.is_legitimate_name("jupyter_ai_fake")

    def test_is_legitimate_url_with_valid_urls(self):
        """Test that legitimate URLs are recognized."""
        validator = RepositoryValidator()
        assert validator.is_legitimate_url(
            "https://github.com/jupyter-ai-contrib/jupyter-ai-router"
        )
        assert validator.is_legitimate_url(
            "https://github.com/jupyterlab/jupyter-ai"
        )

    def test_is_legitimate_url_with_invalid_urls(self):
        """Test that illegitimate URLs are rejected."""
        validator = RepositoryValidator()
        assert not validator.is_legitimate_url(
            "https://github.com/malicious-org/jupyter-ai-router"
        )
        assert not validator.is_legitimate_url("https://evil.com/package")
        assert not validator.is_legitimate_url(None)

    def test_get_package_info_with_missing_package(self):
        """Test getting info for a non-existent package."""
        validator = RepositoryValidator()
        info = validator.get_package_info("nonexistent_package_xyz")
        assert info.name == "nonexistent_package_xyz"
        assert not info.is_legitimate

    def test_validate_dependencies(self):
        """Test validating a list of dependencies."""
        validator = RepositoryValidator()
        dependencies = [
            "jupyter_ai_router>=0.0.2",
            "jupyterlab_chat>=0.19.0a0",
        ]
        results = validator.validate_dependencies(dependencies)

        assert "jupyter_ai_router" in results
        assert "jupyterlab_chat" in results
        assert isinstance(results["jupyter_ai_router"], RepositoryInfo)

    def test_get_illegitimate_packages(self):
        """Test getting list of illegitimate packages."""
        validator = RepositoryValidator()
        # Create a custom validator with a known set
        custom_repos = {"package1", "package2"}
        validator = RepositoryValidator(legitimate_repos=custom_repos)

        dependencies = ["package1", "package2", "malicious_package"]
        illegitimate = validator.get_illegitimate_packages(dependencies)

        # malicious_package should be in the illegitimate list
        package_names = [info.name for info in illegitimate]
        assert "malicious_package" in package_names

    def test_custom_validator_configuration(self):
        """Test creating a validator with custom configuration."""
        custom_repos = {"custom_package"}
        custom_patterns = [r"^https://custom\.com/"]

        validator = RepositoryValidator(
            legitimate_repos=custom_repos,
            url_patterns=custom_patterns,
        )

        assert validator.is_legitimate_name("custom_package")
        assert not validator.is_legitimate_name("jupyter_ai_router")
        assert validator.is_legitimate_url("https://custom.com/package")

    def test_legitimate_repositories_constant(self):
        """Test that LEGITIMATE_REPOSITORIES contains expected packages."""
        expected_packages = [
            "jupyterlab_chat",
            "jupyter_server_documents",
            "jupyter_ai_router",
            "jupyter_ai_persona_manager",
            "jupyter_ai_litellm",
            "jupyter_ai_magic_commands",
            "jupyter_ai_chat_commands",
            "jupyter_ai_jupyternaut",
        ]

        for package in expected_packages:
            assert package in LEGITIMATE_REPOSITORIES

    def test_validate_jupyter_ai_dependencies_returns_dict(self):
        """Test that validate_jupyter_ai_dependencies returns a dict."""
        results = validate_jupyter_ai_dependencies()
        assert isinstance(results, dict)
        # Should have results for all core dependencies
        assert len(results) > 0

    def test_check_installation_security_returns_bool(self):
        """Test that check_installation_security returns a boolean."""
        result = check_installation_security()
        assert isinstance(result, bool)

    def test_package_name_normalization(self):
        """Test that package names with hyphens and underscores are normalized."""
        validator = RepositoryValidator()
        # Both hyphenated and underscored versions should match
        assert validator.is_legitimate_name("jupyter-ai-router")
        assert validator.is_legitimate_name("jupyter_ai_router")
        assert validator.is_legitimate_name("jupyterlab-chat")
        assert validator.is_legitimate_name("jupyterlab_chat")
