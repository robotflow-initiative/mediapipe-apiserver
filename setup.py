from setuptools import find_packages, setup

setup(
    name='mediapipe_apiserver',
    version='0.1.0',
    url='https://github.com/robotflow-initiative/mediapipe_apiserver',
    author='davidliyutong',
    author_email='david.liyutong@outlook.com',
    description='MediaPipe API Server',
    packages=find_packages(),    
    install_requires=[line.strip() for line in open('requirements.txt')],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
