from setuptools import setup, find_packages

setup(
    name='datawiz',
     author='Boszori, Barbara Eszter',
     packages=find_packages(),
     entry_points='''
         [gui_scripts]
         datawiz=main.wiz.py
     ''',
     install_requires=[
         'spacy',
         'en-core-web-sm',
         'pandas',
         'pandastable',
         'mysql'
     ]
)
