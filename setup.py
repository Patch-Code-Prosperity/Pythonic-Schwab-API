from setuptools import setup, find_packages

setup(
    name='pythonicachwabapi',       # Replace with your project name
    version='0.1.01',                # Replace with your project's version
    packages=find_packages(),       # Automatically find packages in your_project
    include_package_data=True,      # Include package data specified in MANIFEST.in
    install_requires=[
        # List your dependencies here, e.g.,
        # 'requests',
        # 'numpy',
    ],
    entry_points={
        'console_scripts': [
            # Define console scripts here if needed
            # 'your_script=your_module:main',
        ],
    },
    author='Cfomodz',             # Replace with your name
    author_email='your_email@example.com',  # Replace with your email
    description='A brief description of your project',  # Replace with your project description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This ensures README.md is treated as markdown
    url='https://github.com/yourusername/your_project',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',         # Replace with the minimum Python version required
)

