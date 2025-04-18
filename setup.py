from setuptools import setup, find_packages

setup(
    name="baseball_stats",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy',
        'pybaseball',
        'python-dotenv',
        'pandas'
    ],
)