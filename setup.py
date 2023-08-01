import pathlib
from setuptools import find_packages, setup
import os

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

def read_requirements():
    with open('requirements.txt', 'r') as file:
        return [line.strip() for line in file if not line.startswith('#')]


def find_yaml_files(directory):
    """
    configs are not under src/sherlock and are under config.
    This function finds these config files and adds them to package_data
    """
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.yaml'):
                paths.append(os.path.join('..', path, filename))
    return paths


dev_requires = [
    "black>=22.1.0",
    "importlib-resources>=5.4.0",
    "ipython>=7.31.0",
    "notebook>=6.4.8",
    "pre-commit>=2.17.0",
    "seaborn>=0.11.2",
]
test_requires = []
extras_require = {  # Optional
    "dev": dev_requires,
    "test": test_requires,
}


package_data={
        # If any package contains *.yaml files, include them:
        '': ['*.yaml'],
        # And specifically include any *.yaml files found in the sherlock package:
        'sherlock': find_yaml_files('config'),
    },

setup_kwargs = {
    "name": "sherlock",
    "version": "0.1.0",
    "description": "AI assistant that helps you get access to tribal knowledge faster.",
    "long_description": long_description,
    "author": "Sherlock Team",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "package_data": package_data,
    "package_dir": {"": "src"},
    "packages": find_packages("src"),
    "install_requires": read_requirements(),
    "extras_require": extras_require,
    "python_requires": ">=3.8,<4.0",
}

setup(**setup_kwargs)