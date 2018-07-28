import os
import sys
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a VERSION -m 'version VERSION'")
    print("  git push --tags")
    sys.exit()


setup(name='NoteShrinker',
      version='0.1.1',
      description='Smart shrinking of the size and color palette of images',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Graphics',
      ],
      keywords='noteshrink',
      url='https://github.com/ghandic/NoteShrinker',
      author='Andrew Challis',
      author_email='andrewchallis@hotmail.com',
      license='MIT',
      packages=['NoteShrinker'],
      install_requires=[
          'pillow',
          'scipy',
          'numpy>=1.1.0'
      ],
      entry_points={
          'console_scripts': ['note-shrinker=NoteShrinker.cli:main'],
      },
      include_package_data=True,
      zip_safe=False)
