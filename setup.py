from distutils.core import setup

setup(
    name='JetFileII',
    version='0.0.1',
    author="John O'Neil",
    author_email='oneil.john@gmail.com',
    packages=['JetFileII'],#, 'towelstuff.test'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    #license='LICENSE.txt',
    description='Partial implementation of JetFileII API used for Chainzone (Texcellent) LED Signs. Sigma 3000 compatible.',
    long_description=open('README.md').read(),
    install_requires=[
        "serial >= 2.5.2",
    ],
)


