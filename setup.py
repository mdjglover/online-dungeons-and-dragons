from setuptools import setup, find_packages

setup(
    name='online_dungeons_and_dragons',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-socketio',
    ],
)