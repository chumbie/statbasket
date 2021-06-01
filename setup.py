import setuptools
from setuptools import setup

ver = '1.0.10'
setup(
    name='statbasket',         # How you named your package folder (MyLib)
    packages=['statbasket'],   # Chose the same as "name"
    version=ver,      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    # Give a short description about your library
    description='A small statistics package for data science students and enthusiasts',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='John Weldon',                   # Type in your name
    author_email='john.weldon117@gmail.com',      # Type in your E-Mail
    url='https://github.com/chumbie/statbasket',   # Provide either the link to your github or to your website
    download_url=f'https://github.com/chumbie/statbasket/archive/refs/tags/v_0{ver}.tar.gz',    # I explain this later on
    keywords=[
      'statistics',
      'data-science',
      'students',
      'lite',
      'pure-python'],   # Keywords that define your package best
    install_requires=['setuptools>=42'],

    classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
    ],
)

