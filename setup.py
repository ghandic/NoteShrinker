from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='NoteShrink',
      version='0.1.0',
      description='Smart shrinking of the size and color palette of images',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Image Processing :: Documents',
      ],
      keywords='noteshrink',
      url='http://github.com/challisa/noteshrink',
      author='Andrew Challis',
      author_email='andrewchallis@hotmail.com',
      license='MIT',
      packages=['NoteShrink'],
      install_requires=[
          'pillow',
          'scipy',
          'numpy'
      ],
      entry_points={
          'console_scripts': ['note-shrink=NoteShrink.cli:main'],
      },
      include_package_data=True,
      zip_safe=False)
