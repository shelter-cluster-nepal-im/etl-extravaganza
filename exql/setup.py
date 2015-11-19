from setuptools import setup, find_packages

setup(name='exql',
      version='0.1',
      description='Excel to SQL Management',
      author='Ewan Oglethorpe',
      author_email='ewanogle@gmail.com',
      packages = ['exql'], 
      install_requires = ['dropbox', 'openpyxl','click', 'sqlalchemy','python-dateutil','psycopg2']
)
