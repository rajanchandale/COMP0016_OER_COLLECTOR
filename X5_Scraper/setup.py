from setuptools import setup

"""
Read into setup and how it works  
"""

setup(
    name='youtube_scraper',
    version='1.0',
    packages=[],
    url='www.x5gon.org',
    license='',
    authors=['Sahan Bulathwela', 'Rajan Chandale'],
    authors_email=['m.bulathwela@ucl.ac.uk', 'rajanchandale@gmail.com'],
    description=("ADD DESCRIPTION"),
    install_requires=[
        'google-api-python-client>=1.8.4'
        'youtube-transcript-api>=0.3.1']
)
