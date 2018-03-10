import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name='atcodertools',
        version='1.0.0',
        packages=setuptools.find_packages(),
        install_requires=[
            'click',
            'requests',
            'lxml',
            'cssselect'
        ],
        entry_points={
            'console_scripts': [
                'atcodertools = atcodertools.cli:atcodertools'
            ]
        }
    )
