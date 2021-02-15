import setuptools

setuptools.setup(
    name="timeplot",
    version="0.0.1",
    description="A module for plotting events on a timeline",
    author="Erika Salomon",
    author_email="ecsalomon@gmail.com",
    packages=["timeplot"],
    install_requires=["matplotlib", "pandas"],
    python_requires=">=3.8.6",
)
