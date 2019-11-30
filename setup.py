import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='alchemist-jydiw', # Replace with your own username
    version='0.0.1',
    author='Jerry Lin',
    author_email='jydiw.code@gmail.com',
    description='A ML-assisted chemistry solver',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jydiw/alchemist',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)