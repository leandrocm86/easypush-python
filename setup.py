import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='easypush',
    version='1.0',
    author='Leandro Medeiros',
    author_email='leandrocm86@gmail.com',
    description='Python module and client for EasyPush - a serverless utility to share text between devices.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/leandrocm86/easypush-python',
    project_urls={
        "Bug Tracker": "https://github.com/leandrocm86/easypush-python/issues"
    },
    license='MIT',
    py_modules=['easypush', 'easypush_cli'],
    entry_points={
        'console_scripts': [
            'easypush=easypush_cli:main'
        ]
    },
    install_requires=[],
)
