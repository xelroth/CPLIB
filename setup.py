from setuptools import find_packages, setup
setup(
    name='CPLIB',
    packages=find_packages(include=['CPLIB']),
    version='1.0',
    description='The provided Python library allows you to interact with cPanel and FTP servers. It provides functions for managing cron jobs, FTP accounts, databases, and file operations such as creating folders, uploading files, and more ',
    author='Zelroth',
    license='MIT',
    install_requires=[
        'requests',
        'ftplib',
        'json',
        'base64',
        'urllib',
        'os',
        'math'
    ]
    
)

