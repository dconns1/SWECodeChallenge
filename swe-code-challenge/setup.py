from setuptools import setup, find_packages

setup(
    name='SWECodeChallenge',
    version='0.0.0',
    description='A submission of the code challenge for Software Engineer II at Security Innovation as specified by the SWE II Challenge Instructions.pdf',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Devon Connors',
    author_email='dconns1@outlook.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'swe-code-challenge=my_module.SWECodeChallenge:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Debian 12',
    ],
    python_requires='>=3.12',
)