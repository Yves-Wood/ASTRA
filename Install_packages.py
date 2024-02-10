import subprocess

def install_packages(package_list):
    for package in package_list:
        subprocess.check_call(["pip", "install", package])

if __name__ == "__main__":
    # List of required packages
    packages = ["numpy", "astropy", "astroquery", "pyvo", "requests", "keyring", "beautifulsoup4", "html5lib"]

    print("Installing required packages...")
    install_packages(packages)
    print("Packages installed successfully!")