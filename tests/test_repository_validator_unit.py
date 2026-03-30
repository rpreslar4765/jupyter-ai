"""Simple unit tests that don't require external dependencies."""

from jupyter_ai.repository_validator import (
    RepositoryValidator,
    LEGITIMATE_REPOSITORIES,
)


def test_legitimate_repositories_constant():
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


def test_repository_validator_initialization():
    """Test that RepositoryValidator can be initialized."""
    validator = RepositoryValidator()
    assert validator is not None
    assert validator.legitimate_repos is not None
    assert validator.url_patterns is not None


def test_is_legitimate_name_with_valid_package():
    """Test that legitimate package names are recognized."""
    validator = RepositoryValidator()
    assert validator.is_legitimate_name("jupyter_ai_router")
    assert validator.is_legitimate_name("jupyterlab_chat")


def test_is_legitimate_name_with_invalid_package():
    """Test that illegitimate package names are rejected."""
    validator = RepositoryValidator()
    assert not validator.is_legitimate_name("malicious_package")
    assert not validator.is_legitimate_name("jupyter_ai_fake")


def test_is_legitimate_url_with_valid_urls():
    """Test that legitimate URLs are recognized."""
    validator = RepositoryValidator()
    assert validator.is_legitimate_url(
        "https://github.com/jupyter-ai-contrib/jupyter-ai-router"
    )
    assert validator.is_legitimate_url(
        "https://github.com/jupyterlab/jupyter-ai"
    )


def test_is_legitimate_url_with_invalid_urls():
    """Test that illegitimate URLs are rejected."""
    validator = RepositoryValidator()
    assert not validator.is_legitimate_url(
        "https://github.com/malicious-org/jupyter-ai-router"
    )
    assert not validator.is_legitimate_url("https://evil.com/package")
    assert not validator.is_legitimate_url(None)


def test_package_name_normalization():
    """Test that package names with hyphens and underscores are normalized."""
    validator = RepositoryValidator()
    # Both hyphenated and underscored versions should match
    assert validator.is_legitimate_name("jupyter-ai-router")
    assert validator.is_legitimate_name("jupyter_ai_router")
    assert validator.is_legitimate_name("jupyterlab-chat")
    assert validator.is_legitimate_name("jupyterlab_chat")


def test_custom_validator_configuration():
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
