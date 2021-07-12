import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages(include=['fireup', 'fireup.*'])
print("Packages: {}".format(packages))

setuptools.setup(
    name="firebase-fireup",                     # This is the name of the package
    version="0.0.7",                        # The initial release version
    author="Esa Firman",                     # Full name of the author
    description="Firebase Storage Uploader",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=packages,    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["fireup"],             # Name of the python package
    install_requires=[
        'firebase-admin==5.0.0',
        'requests==2.25.1',
        'requests-toolbelt==0.9.1',
        'python-jwt==2.0.1'
    ],                     # Install other dependencies if any
    entry_points={
        'console_scripts': [
            'fireup = fireup.fireup:main'
        ]
    },
)
