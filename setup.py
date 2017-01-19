from setuptools import setup, find_packages

setup(name='pyliterature',
    version='0.1.4',
    description='A Python web wrapper and text mining package for the scientific journal, including Nature, Science, ScienceDirect, Wiley, ACS publication, RSC publication and so on.',

    author='Xing Wang',
    author_email='xingwang1991@gmail.com',

    url='https://github.com/superstar54/pyliterature',
    packages=['pyliterature', ],
    test_suite="tests",
    license='MIT License',
    install_requires = ['beautifulsoup4', 'spynner >= 2.19', 'nltk >= 3.2.2'],
    platforms = 'any',
)