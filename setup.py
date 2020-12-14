from setuptools import setup, find_packages

setup(
    name='szakdolgozat_IAPW0K',
     version='1.0',
     author='Boszori, Barbara Eszter',
     packages=find_packages(),
     entry_points='''
         [gui_scripts]
         szakdolgozat_IAPW0K=wiz.py
     ''',
     install_requires=[
         'spacy',
         'en-core-web-sm',
         'pandas',
         'pandastable',
         'mysql',
         'tkinter'
     ]
)
