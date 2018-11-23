import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eth_keyfun",
    version="1.0",
    author="Chirag Jariwala(CJHackerz)",
    author_email="chirag_a@srmuniv.edu.in",
    description="A small tool to bruteforce weak ethereum private keys and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sector443/eth_keyfun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)