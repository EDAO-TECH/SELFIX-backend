from setuptools import setup, find_packages

setup(
    name='selfix',
    version='1.0.0',
    author='Teng Zhi Li',
    author_email='support@nevermissed.org',
    description='SELFIX - Self-Healing Infrastructure eXtension',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://nevermissed.org/selfix',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add dependencies here, if any
    ],
    entry_points={
        'console_scripts': [
            'selfix=selfix.cli.selfix:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: System Administrators',
        'Development Status :: 5 - Production/Stable',
        'Topic :: System :: Recovery Tools',
    ],
    python_requires='>=3.7',
)
