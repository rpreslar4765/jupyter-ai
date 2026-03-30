"""
Validator for ensuring only legitimate Jupyter AI repositories are installed.

This module provides functionality to validate that installed packages
are from legitimate sources (jupyter-ai-contrib organization) to prevent
dependency confusion attacks and typosquatting.
"""

import importlib.metadata
import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class RepositoryInfo:
    """Information about a repository."""

    name: str
    source_url: Optional[str] = None
    is_legitimate: bool = False


# List of legitimate Jupyter AI repositories from jupyter-ai-contrib organization
LEGITIMATE_REPOSITORIES = {
    "jupyterlab_chat",
    "jupyter_server_documents",
    "jupyter_ai_router",
    "jupyter_ai_persona_manager",
    "jupyter_ai_litellm",
    "jupyter_ai_magic_commands",
    "jupyter_ai_chat_commands",
    "jupyter_ai_jupyternaut",
    "jupyter_ai_tools",
    "jupyter_server_mcp",
    "jupyterlab_diff",
}

# Patterns for legitimate repository URLs
LEGITIMATE_URL_PATTERNS = [
    r"^https://github\.com/jupyter-ai-contrib/",
    r"^https://github\.com/jupyterlab/jupyter-ai",
]


class RepositoryValidator:
    """Validates that repositories are from legitimate sources."""

    def __init__(
        self,
        legitimate_repos: Optional[Set[str]] = None,
        url_patterns: Optional[List[str]] = None,
    ):
        """
        Initialize the validator.

        Args:
            legitimate_repos: Set of legitimate repository names.
                             Defaults to LEGITIMATE_REPOSITORIES.
            url_patterns: List of regex patterns for legitimate URLs.
                         Defaults to LEGITIMATE_URL_PATTERNS.
        """
        self.legitimate_repos = legitimate_repos or LEGITIMATE_REPOSITORIES
        self.url_patterns = [
            re.compile(pattern)
            for pattern in (url_patterns or LEGITIMATE_URL_PATTERNS)
        ]

    def is_legitimate_name(self, package_name: str) -> bool:
        """
        Check if a package name is in the list of legitimate repositories.

        Args:
            package_name: Name of the package to check.

        Returns:
            True if the package name is legitimate, False otherwise.
        """
        # Normalize package name (replace hyphens with underscores)
        normalized_name = package_name.replace("-", "_")
        return normalized_name in self.legitimate_repos

    def is_legitimate_url(self, url: Optional[str]) -> bool:
        """
        Check if a URL matches legitimate repository URL patterns.

        Args:
            url: URL to check.

        Returns:
            True if the URL matches a legitimate pattern, False otherwise.
        """
        if not url:
            return False

        return any(pattern.match(url) for pattern in self.url_patterns)

    def get_package_info(self, package_name: str) -> RepositoryInfo:
        """
        Get information about an installed package.

        Args:
            package_name: Name of the package.

        Returns:
            RepositoryInfo object with package information.
        """
        try:
            dist = importlib.metadata.distribution(package_name)
            metadata = dist.metadata

            # Try to extract source URL from metadata
            source_url = None
            if "Home-page" in metadata:
                source_url = metadata["Home-page"]
            elif "Project-URL" in metadata:
                # Project-URL can have multiple values
                for url_entry in metadata.get_all("Project-URL", []):
                    if "Source" in url_entry or "Homepage" in url_entry:
                        # Format is "Label, URL"
                        parts = url_entry.split(",", 1)
                        if len(parts) == 2:
                            source_url = parts[1].strip()
                            break

            is_legitimate = (
                self.is_legitimate_name(package_name) or
                self.is_legitimate_url(source_url)
            )

            return RepositoryInfo(
                name=package_name,
                source_url=source_url,
                is_legitimate=is_legitimate,
            )
        except importlib.metadata.PackageNotFoundError:
            return RepositoryInfo(
                name=package_name,
                is_legitimate=False,
            )

    def validate_dependencies(
        self,
        dependencies: List[str],
    ) -> Dict[str, RepositoryInfo]:
        """
        Validate a list of dependencies.

        Args:
            dependencies: List of package names to validate.

        Returns:
            Dictionary mapping package names to their RepositoryInfo.
        """
        results = {}
        for dep in dependencies:
            # Extract package name from dependency specification
            # (e.g., "package>=1.0.0" -> "package")
            package_name = re.split(r"[<>=!]", dep)[0].strip()
            results[package_name] = self.get_package_info(package_name)

        return results

    def get_illegitimate_packages(
        self,
        dependencies: List[str],
    ) -> List[RepositoryInfo]:
        """
        Get list of illegitimate packages from dependencies.

        Args:
            dependencies: List of package names to validate.

        Returns:
            List of RepositoryInfo for packages that are not legitimate.
        """
        results = self.validate_dependencies(dependencies)
        return [
            info for info in results.values()
            if not info.is_legitimate
        ]


def validate_jupyter_ai_dependencies() -> Dict[str, RepositoryInfo]:
    """
    Validate all Jupyter AI core dependencies.

    Returns:
        Dictionary mapping package names to their validation results.
    """
    core_dependencies = [
        "jupyterlab_chat",
        "jupyter_server_documents",
        "jupyter_ai_router",
        "jupyter_ai_persona_manager",
        "jupyter_ai_litellm",
        "jupyter_ai_magic_commands",
        "jupyter_ai_chat_commands",
        "jupyter_ai_jupyternaut",
    ]

    validator = RepositoryValidator()
    return validator.validate_dependencies(core_dependencies)


def check_installation_security() -> bool:
    """
    Check if the current Jupyter AI installation is secure.

    Returns:
        True if all dependencies are legitimate, False otherwise.
    """
    validator = RepositoryValidator()
    results = validate_jupyter_ai_dependencies()

    illegitimate = [
        info for info in results.values()
        if not info.is_legitimate
    ]

    if illegitimate:
        print("WARNING: The following packages may not be from legitimate sources:")
        for info in illegitimate:
            print(f"  - {info.name}")
            if info.source_url:
                print(f"    Source: {info.source_url}")
        return False

    print("All Jupyter AI dependencies are from legitimate sources.")
    return True
