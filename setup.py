from distutils.core import setup
setup(
    name = 'shawk',
    packages = ['shawk'],
    version = '0.2',
    description = 'A simple and user-friendly SMTP to SMS library',
    author = 'Josh Hawkins',
    author_email = 'jkhaccounts@gmail.com',
    url = 'https://github.com/hawkins/shawk',
    download_url = 'https://github.com/hawkins/shawk/tarball/0.1',
    keywords = ['sms', 'smtp', 'hawkins', 'simple'], # arbitrary keywords
    classifiers = [],
    install_requires=[
        'imapclient==0.13',
    ],
)
