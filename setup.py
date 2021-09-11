from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-schema-versions",
    description="Datasette plugin that shows the schema version of every attached database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-schema-versions",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-schema-versions/issues",
        "CI": "https://github.com/simonw/datasette-schema-versions/actions",
        "Changelog": "https://github.com/simonw/datasette-schema-versions/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_schema_versions"],
    entry_points={"datasette": ["schema_versions = datasette_schema_versions"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx", "sqlite-utils"]},
    tests_require=["datasette-schema-versions[test]"],
)
