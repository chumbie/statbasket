from distutils.core import setup

#  used to pull readme.md into file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='statbasket',         # How you named your package folder (MyLib)
  packages=['statbasket'],   # Chose the same as "name"
  version='1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='A small statistics package for data science students and enthusiasts',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='John Weldon',                   # Type in your name
  author_email='john.weldon117@gmail.com',      # Type in your E-Mail
  url='https://github.com/chumbie/statbasket',   # Provide either the link to your github or to your website
  download_url='https://github.com/chumbie/statbasket/archive/refs/tags/v_01.0.03.tar.gz',    # I explain this later on
  keywords=[
      'statistics', 
      'data-science', 
      'students', 
      'lite', 
      'pure-python'],   # Keywords that define your package best
  install_requires=[],           # I get to this in a second
      
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
  ],
)