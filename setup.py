from setuptools import setup

import fastats

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='fastats',
      version=fastats.__version__,
      description=fastats.__description__,
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Intended Audience :: Science/Research',
      ],
      keywords='FASTA',
      url=fastats.__url__,
      author=fastats.__author__,
      author_email=fastats.__author_email__,
      license=fastats.__license__,
      packages=['fastats'],
      install_requires=[
          'click',
          'biopython',
          'numpy'
      ],
      test_suite='nose.collector',
      tests_require=[],
      entry_points={
          'console_scripts': ['fastats=fastats.fastats:main'],
      },
      include_package_data=True,
      zip_safe=False)
