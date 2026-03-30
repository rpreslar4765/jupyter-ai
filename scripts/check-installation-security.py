#!/usr/bin/env python
"""
Command-line tool to validate Jupyter AI installation security.

This script checks whether the installed Jupyter AI dependencies
are from legitimate sources.
"""

import sys
from jupyter_ai.repository_validator import (
    validate_jupyter_ai_dependencies,
    RepositoryValidator,
)


def main():
    """Run the security validation check."""
    print("Validating Jupyter AI installation security...")
    print("-" * 60)

    validator = RepositoryValidator()
    results = validate_jupyter_ai_dependencies()

    legitimate_count = 0
    illegitimate_count = 0
    not_installed_count = 0

    for package_name, info in results.items():
        if info.source_url is None and not info.is_legitimate:
            # Package not installed
            print(f"⚠️  {package_name}: NOT INSTALLED")
            not_installed_count += 1
        elif info.is_legitimate:
            print(f"✓  {package_name}: LEGITIMATE")
            if info.source_url:
                print(f"   Source: {info.source_url}")
            legitimate_count += 1
        else:
            print(f"✗  {package_name}: POTENTIALLY ILLEGITIMATE")
            if info.source_url:
                print(f"   Source: {info.source_url}")
            illegitimate_count += 1

    print("-" * 60)
    print(f"\nSummary:")
    print(f"  Legitimate packages: {legitimate_count}")
    print(f"  Not installed: {not_installed_count}")
    print(f"  Potentially illegitimate: {illegitimate_count}")

    if illegitimate_count > 0:
        print("\n⚠️  WARNING: Some packages may not be from legitimate sources!")
        print("Please verify these packages before using Jupyter AI.")
        return 1
    elif not_installed_count > 0:
        print("\n⚠️  NOTE: Some core dependencies are not installed.")
        print("Jupyter AI may not function correctly.")
        return 0
    else:
        print("\n✓  All installed dependencies are from legitimate sources.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
