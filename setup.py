from setuptools import find_packages, setup
setup(
    name='shouldi'
    packages=find_packages(include=['requests', 'pytz']),
    version='0.1.0',
    description='Uses data from the NGO Carbon Intensity API to give recommendations on whether to use electricity based on the current and forecasted carbon emissions of the UK National Grid',
    author='Andy Brace <contact@openbook.uk.com',
    license='',
)
