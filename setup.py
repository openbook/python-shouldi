import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='shouldi'
    packages=setuptools.find_packages(),
    version='0.1.0',
    description='Uses data from the NGO Carbon Intensity API to give recommendations on whether to use electricity based on the current and forecasted carbon emissions of the UK National Grid',
    author='Andy Brace <contact@openbook.uk.com',
    license='',
)
