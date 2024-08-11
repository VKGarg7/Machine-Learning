import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis_Vansh_102218059",
    version="1.0",
    description="topsis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/VKGarg7/Machine-Learning/tree/main/Topsis_Vansh_102218059",
    author="Vansh Kumar Garg",
    author_email="14garg04@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)