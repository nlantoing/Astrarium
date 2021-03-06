from setuptools import find_packages, setup

setup(
    name='Astrarium',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'flask_sqlalchemy',
        'flask_migrate',
        'flask_script',
        'flask_cors',
        'pytest',
        'coverage',
        'pykep'
    ],
)
