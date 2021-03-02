#!/usr/bin/env python
import setuptools

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setuptools.setup(
    name='xontrib-history-encrypt',
    version='0.0.8',
    license='MIT',
    author='anki-code',
    author_email='no@no.no',
    description="History backend that can encrypt the xonsh shell commands history.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['xonsh', 'cryptography', 'ujson'],
    packages=['xontrib', 'xontrib.history_encrypt'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.py']},
    platforms='any',
    url='https://github.com/anki-code/xontrib-history-encrypt',
    project_urls={
        "Documentation": "https://github.com/anki-code/xontrib-history-encrypt/blob/master/README.md",
        "Code": "https://github.com/anki-code/xontrib-history-encrypt",
        "Issue tracker": "https://github.com/anki-code/xontrib-history-encrypt/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
    ]
)
