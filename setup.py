from setuptools import setup

setup(
    name='boxgen',
    version='1.0.0',
    description='Generate images of box designs, to print on '
                'card stock and cut out.',
    author='Ellen Marie Dash',
    author_email='me@duckie.co',
    url='https://github.com/duckinator/boxgen',
    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'boxgen=boxgen:main',
        ],
    },
    packages=['boxgen'],
    python_requires='>=3.6',
    install_requires=[
        # Not sure how svgwrite versions things,
        # so don't assume semantic versioning.
        "svgwrite=1.1.12",
    ],
)
