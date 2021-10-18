from setuptools import setup, find_packages

requires = ["Flask", "spotipy", "requests", "python-dotenv"]

setup(
    name="SpotifyPreParty",
    version="1.0",
    description="An application that creates a playlist with the top songs from entered artists",
    author="Devan Fischer",
    author_email="devan@createpnw.com",
    keywords="web flask",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
