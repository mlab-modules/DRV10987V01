from setuptools import setup, find_packages

# Základní informace o balíčku
name = 'MLAB_DRV10987'
version = '1.0.0'
description = 'A Python module for controlling BLDC motors using the DRV10987V01 MLAB module.'
author = 'Roman Dvorak'
author_email = 'romandvorak@mlab.cz'
url = 'https://www.mlab.cz/module/DRV10987V01'
license = 'MIT'

install_requires = [
]

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    packages=find_packages(),
    install_requires=install_requires,
    # classifiers=[
    #     "Development Status :: 4 - Beta",
    #     "Intended Audience :: Developers,Science/Research",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    #     "Programming Language :: Python::3",
    # ]
)
