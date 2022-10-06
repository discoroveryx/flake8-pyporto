from __future__ import with_statement

import setuptools

requires = [
    'flake8 > 5.0.4',
]

setuptools.setup(
    name='flake8_pyporto',
    license='MIT',
    version='1.0',
    description='PyPorto extension for flake8',
    author='Me',
    author_email='discoroveryx@gmail.com',
    url='https://github.com/discoroveryx/flake8-pyporto',
    packages=[
        'flake8_pyporto',
    ],
    install_requires=requires,
    entry_points={
        'flake8.extension': [
            'PYP001 = flake8_pyporto:PyPorto',
        ],
    },
    classifiers=[
        'Framework :: Flake8',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
