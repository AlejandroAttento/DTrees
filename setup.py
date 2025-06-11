from setuptools import setup, find_packages

setup(
    name="DTrees",
    version="0.1.0",
    author="Alejandro Daniel Attento",
    author_email="alejandro.attento@gmail.com",
    description="Quick library to create decision trees",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-package-name",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'mermaid-py'
    ],
)