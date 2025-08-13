import sys
import tomllib
import re
import os
from importlib import metadata
from pathlib import Path


def get_import_name(package_name: str) -> str | None:
    """
    Dynamically finds the importable name for a package by inspecting its
    installed files. This is a fully dynamic approach with no hardcoding.
    """
    try:
        dist = metadata.distribution(package_name)

        # Method 1: The official way using 'top_level.txt'.
        if top_level_text := dist.read_text("top_level.txt"):
            first_line = top_level_text.strip().splitlines()[0]
            if "." not in first_line:
                return first_line

        # Method 2: If top_level.txt is missing or a namespace, deduce from files.
        if dist.files:
            module_paths = {p.parent for p in dist.files if p.name == "__init__.py"}
            if module_paths:
                shortest_path = min(module_paths, key=lambda p: len(p.parts))
                return str(shortest_path).replace("/", ".")

        return None

    except metadata.PackageNotFoundError:
        return None


def get_dependencies_from_toml(toml_path="pyproject.toml"):
    # This function remains the same
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        core_deps = data.get("project", {}).get("dependencies", [])
        dev_deps = (
            data.get("project", {}).get("optional-dependencies", {}).get("dev", [])
        )
        return core_deps, dev_deps
    except FileNotFoundError:
        print(f"❌ ERROR: '{toml_path}' not found.")
        return None, None


def check_packages(package_list):
    not_found = []
    failed_imports = []
    for pkg_name in package_list:
        # **THE FINAL FIX IS HERE:** Added '[' to the regex character class.
        # This now correctly handles names with extras, like 'uvicorn[standard]'.
        base_name = re.split(r"[=<>~\[]", pkg_name)[0].strip()

        import_name = get_import_name(base_name)

        if not import_name:
            print(f"⚪️ {base_name:.<30} METADATA NOT FOUND OR AMBIGUOUS")
            not_found.append(pkg_name)
            continue

        try:
            __import__(import_name)
            if "__mypyc" in import_name:
                import_name = "mypy"
            print(f"✅ {import_name:.<30} OK (from package: {base_name})")
        except ImportError:
            print(f"❌ {import_name:.<30} FAILED TO IMPORT (from package: {base_name})")
            failed_imports.append(pkg_name)

    return not_found, failed_imports


# The main execution block also remains the same
if __name__ == "__main__":
    print(f"--- Using Python executable: {sys.executable}\n")
    core_deps, dev_deps = get_dependencies_from_toml()

    if core_deps is not None:
        print("--- Verifying Core Dependencies ---")
        core_not_found, core_failed_imports = check_packages(core_deps)

        print("\n--- Verifying Dev Dependencies ---")
        dev_not_found, dev_failed_imports = check_packages(dev_deps)

        print("\n--- HONEST SUMMARY ---")
        all_good = not (
            core_not_found or core_failed_imports or dev_not_found or dev_failed_imports
        )

        if all_good:
            print("🎉 Success! All dependencies are installed and importable.")
        else:
            print("Found some issues:\n")
            if core_not_found or dev_not_found:
                print("Packages NOT FOUND by metadata:")
                for pkg in core_not_found + dev_not_found:
                    print(f"  - {pkg}")

            if core_failed_imports or dev_failed_imports:
                print("\nPackages with IMPORT ISSUES:")
                for pkg in core_failed_imports + dev_failed_imports:
                    print(f"  - {pkg}")
