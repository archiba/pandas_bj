from setuptools import setup

requires = open('requirements.txt').read()

setup(
    name='pandas_bj',
    version='0.0.4',
    packages=['pandas_bj'],
    url='https://github.com/archiba/pandas_bj',
    license='MIT',
    author='Yuki Chiba',
    author_email='yuki.music.0283@gmail.com',
    description='Pandas BJ (Between Join) provides efficient way to use `JOIN` and `BETWEEN` comparison. with pandas.DataFrame.',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=requires,
)
