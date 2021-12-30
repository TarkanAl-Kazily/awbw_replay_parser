"""Initialize the awbw_replay package"""
from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='AWBW Replay',
    url='https://github.com/TarkanAl-Kazily/awbw_replay_parser/',
    author='Tarkan Al-Kazily',
    author_email='tarkan.alkazily@gmail.com',
    # Needed to actually package something
    packages=['awbw_replay'],
    # Needed for dependencies
    install_requires=['parse, phpserialize'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Python library to parse AWBW game replay files',
    # We will also need a readme eventually (there will be a warning)
    # pylint: disable=consider-using-with
    long_description=open('README.md', 'r', encoding='utf-8').read(),
)
