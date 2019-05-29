from setuptools import setup

if __name__ == '__main__':
    setup(
        name='crous_menu',
        py_modules=['crous_menu'],
        entry_points='''
            [console_scripts]
            crous_menu=crous_menu:main
        ''',
        description='Script to fetch the CROUS menu for Barnave',
        author="Tom Cornebize",
        author_email="tom.cornebize@gmail.com",
        install_requires=[
            'requests',
            'beautifulsoup4',
            'colorama',
        ],
    )
