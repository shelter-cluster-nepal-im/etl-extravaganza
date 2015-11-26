from setuptools import setup, find_packages

setup(name='etl',
      version='0.1',
      description='distribution etl',
      author='Ewan Oglethorpe',
      author_email='ewanogle@gmail.com',
      packages = ['etl', 'clean'], 
      install_requires = ['dropbox', 'openpyxl','click', 'sqlalchemy','python-dateutil'],
	entry_points={
    	'console_scripts': [
		'etl = etl.etl:iterate_reports',
   	 ]
}
)
