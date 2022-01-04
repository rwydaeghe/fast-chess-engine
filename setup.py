from setuptools import setup, Extension

module = Extension ('primes', sources=['primes.pyx'])

setup(
    name='cythonTest',
    version='1.0',
    author='jetbrains',
    ext_modules=[module]
)
