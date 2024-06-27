from setuptools import setup, find_packages

setup(
    name='pythonic_schwab_api',
    version='0.2.3',
    packages=find_packages(),
    install_requires=["requests", "python-dotenv", "websockets"],
    author='Cfomodz',
    description='This is an unofficial interface to make getting started with the Schwab API easier.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Patch-Code-Prosperity/Pythonic-Schwab-API',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    license='MIT License'
)

