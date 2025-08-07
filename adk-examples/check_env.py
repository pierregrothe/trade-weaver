import sys

print(f"--- Checking Python executable: {sys.executable}\n")
# We only check key packages, not dependencies of dependencies.
# Note that package names (for pip) can differ from import names.
# e.g., 'google-cloud-firestore' is imported as 'google.cloud.firestore'

core_imports = [
    "eodhd", "fastapi", "google.adk", "google.cloud.firestore",
    "google.cloud.secretmanager", "google.generativeai", "lxml",
    "pandas", "dotenv", "requests", "uvicorn"
]

dev_imports = ["ruff", "mypy", "pytest"] # 'codespell' is a command-line tool, not typically imported

all_imports = core_imports + dev_imports
missing_packages = []

print("--- Verifying main packages ---\n")
for package_name in all_imports:
    try:
        # Use __import__ to import using a string name
        __import__(package_name)
        print(f"✅ {package_name:.<30} OK")
    except ImportError:
        print(f"❌ {package_name:.<30} FAILED")
        missing_packages.append(package_name)

print("\n--- Summary ---")
if not missing_packages:
    print("🎉 All essential packages are installed correctly. You're ready to go!")
else:
    print("\nThe following packages could not be imported:")
    for pkg in missing_packages:
        print(f"  - {pkg}")