from setuptools import setup, find_packages

setup(
    name="analizador_manifests",
    version="0.1.0",
    description="Analizador de Manifests MPD y HLS",
    author="Analizador Manifests Team",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "analizador-manifests=analizador_manifests.cli:main",
        ],
    },
)
