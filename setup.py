from setuptools import setup, find_packages

# Set requirements to be installed
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
install_requires = parse_requirements('requirements.txt')

setup(
    name="atr8ec",
    version="0.1.0",
    description="Example Package for WEEK-06 of DS 5111",
    author="Austin Rivera",
    author_email="atr8ec@virgnia.edu",
    url="https://github.com/austin-t-rivera/atr8ec_DS5111su24_lab_01",
    packages=find_packages(where='src'),
    packages_dir={'': 'src'},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'my-script=atr8ec:text_processor:clean_text',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Darwin',
    ],
    python_requires='>=3.8',
)
