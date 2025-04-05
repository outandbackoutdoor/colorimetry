import os
import setuptools

with open(os.path.join('colorimetry', 'resources', 'README.md')) as f:
    long_description = f.read()

with open(os.path.join('colorimetry', 'resources', 'requirements.txt')) as f:
    install_requires = list(map(lambda s: s.strip(), f.readlines()))


_VERSION = '0.0.1'

setuptools.setup(
    name='colorimetry',
    version=_VERSION,
    description="Color conversion and matching.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[],
    author='Dustin Oprea',
    author_email='dustin@outandbackoutdoor.com',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'colorimetry': [
            'resources/README.md',
            'resources/requirements.txt',
            'resources/requirements-testing.txt',
        ],
    },
    install_requires=install_requires,
    scripts=[
        'colorimetry/resources/scripts/color_hsluv_grids',
        'colorimetry/resources/scripts/color_match',
        'colorimetry/resources/scripts/color_standard_generate_reference',
    ],
)
