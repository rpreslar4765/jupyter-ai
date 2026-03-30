# Repository Security and Validation

## Overview

Jupyter AI v3 is composed of multiple modular packages from the `jupyter-ai-contrib` organization. To ensure the security and integrity of the installation, Jupyter AI includes a repository validation system that verifies dependencies come from legitimate sources.

## Security Concerns

### Dependency Confusion Attacks

Dependency confusion attacks occur when malicious actors publish packages with names similar to private or internal packages. Package managers might inadvertently install the malicious package instead of the legitimate one.

### Typosquatting

Typosquatting involves creating packages with names similar to popular packages (e.g., `jupyter-ai-rooter` instead of `jupyter-ai-router`). Users who make typos when installing packages might accidentally install malicious software.

## Repository Validation

Jupyter AI includes built-in validation to ensure all dependencies are from trusted sources.

### Legitimate Repositories

The following repositories are recognized as legitimate Jupyter AI components:

1. **jupyterlab_chat** - Chat interface for JupyterLab
2. **jupyter_server_documents** - Server-side document handling
3. **jupyter_ai_router** - Core routing layer
4. **jupyter_ai_persona_manager** - AI persona management
5. **jupyter_ai_litellm** - LiteLLM model abstraction
6. **jupyter_ai_magic_commands** - Magic commands implementation
7. **jupyter_ai_chat_commands** - Chat commands functionality
8. **jupyter_ai_jupyternaut** - Default AI persona (Jupyternaut)

All legitimate packages are maintained in the [jupyter-ai-contrib](https://github.com/jupyter-ai-contrib) GitHub organization.

### Validation Process

The validation system checks:

1. **Package names** - Verifies package names match the legitimate repository list
2. **Source URLs** - Validates that package source URLs point to official repositories
3. **URL patterns** - Ensures URLs match expected patterns:
   - `https://github.com/jupyter-ai-contrib/*`
   - `https://github.com/jupyterlab/jupyter-ai`

## Using the Validation API

### Checking Installation Security

To verify your Jupyter AI installation is secure, you have multiple options:

#### Command-line tool (recommended)

```bash
jupyter-ai-check-security
```

This will display a detailed report of all installed dependencies and their validation status.

#### Python script

```bash
python scripts/check-installation-security.py
```

#### Python API

```python
from jupyter_ai.repository_validator import check_installation_security

# Returns True if all dependencies are legitimate
is_secure = check_installation_security()
```

### Validating Specific Packages

To check specific packages:

```python
from jupyter_ai.repository_validator import RepositoryValidator

validator = RepositoryValidator()

# Check a package name
is_legit = validator.is_legitimate_name("jupyter_ai_router")

# Check a source URL
is_legit_url = validator.is_legitimate_url(
    "https://github.com/jupyter-ai-contrib/jupyter-ai-router"
)

# Get detailed package information
info = validator.get_package_info("jupyter_ai_router")
print(f"Package: {info.name}")
print(f"Source: {info.source_url}")
print(f"Legitimate: {info.is_legitimate}")
```

### Validating Dependencies

To validate a list of dependencies:

```python
from jupyter_ai.repository_validator import RepositoryValidator

validator = RepositoryValidator()
dependencies = [
    "jupyter_ai_router>=0.0.2",
    "jupyterlab_chat>=0.19.0a0",
]

results = validator.validate_dependencies(dependencies)
for package, info in results.items():
    if not info.is_legitimate:
        print(f"WARNING: {package} may not be legitimate!")
```

## Configuration

The list of trusted repositories is maintained in `jupyter_ai/trusted_repositories.json`. This file contains:

- Repository names
- GitHub URLs
- PyPI URLs
- Descriptions
- URL patterns for validation

## Best Practices

1. **Always install from PyPI** - Use `pip install jupyter-ai` from the official PyPI repository
2. **Verify package names** - Double-check spelling when installing individual components
3. **Check source URLs** - Verify packages come from `jupyter-ai-contrib` organization
4. **Use version pinning** - Specify exact versions in production environments
5. **Regular audits** - Periodically run `check_installation_security()` to verify your installation

## Reporting Security Issues

If you discover a security issue or suspect a malicious package:

1. **Do NOT** install or use the suspicious package
2. Report the issue to the Jupyter Security Team: [security@jupyter.org](mailto:security@jupyter.org)
3. Include:
   - Package name and version
   - Installation method
   - Source URL (if available)
   - Any suspicious behavior observed

## References

- [Jupyter AI Repository](https://github.com/jupyterlab/jupyter-ai)
- [Jupyter AI Contrib Organization](https://github.com/jupyter-ai-contrib)
- [PyPI Security Guidelines](https://pypi.org/security/)
