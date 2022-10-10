from setuptools import setup

setup(
    name='scPrisma_torch',
    version='1.0',
    packages=['scPrisma_torch'],
    url='',
    license='',
    author='jonathankarin',
    author_email='jonathan.karin@mail.huji.ac.il',
    description='scPrisma: inference, filtering and enhancement of periodic signals in single-cell data using spectral template matching ',
    python_requires='>=3',
    install_requires=[
        'numpy', 'scanpy', 'numba', 'pandas', 'scikit-learn', 'scipy', 'seaborn','matplotlib','sklearn','torch']

)
