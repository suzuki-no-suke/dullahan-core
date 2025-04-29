from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="dullahan-core",
    version="0.1.250429.1",
    author="Hiroyuki Suzuki",
    author_email="suzuki.wotsuku.hiroyuki.do.work@gmail.com",
    description="A core library for the DuLLahan project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suzuki-no-suke/DuLLahan-Core",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=7.0", "black>=22.0", "isort>=5.0"],
        "bots": ["python-ulid>=2.0.0"],
    },
) 