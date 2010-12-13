from distutils.core import setup
from distutils.command import build_ext
from distutils.core import Extension

import os, sys

class OpensslBuilder(build_ext.build_ext):
    """
    Specialization of build_ext to enable swig_opts to inherit any
    include_dirs settings made at the command line or in a setup.cfg
    file
    """

    user_options = build_ext.build_ext.user_options + [
        ('openssl=', 'o', 'Prefix for openssl installation location'),
        ('swig-extra=', None, 'Extra swig options')]
    
    def initialize_options(self):
        build_ext.build_ext.initialize_options(self)
        self.swig_extra = None
        if os.name == 'nt':
            self.libraries = ['ssleay32', 'libeay32']
            self.openssl = 'c:\\pkg'
        else:
            self.libraries = ['ssl', 'crypto']
            self.openssl = '/usr'

    def finalize_options(self):
        build_ext.build_ext.finalize_options(self)

        openssl_include = os.path.join(self.openssl, 'include')
        openssl_lib = os.path.join(self.openssl, 'lib')

        self.swig_opts = ['-I%s' % i for i in self.include_dirs + [openssl_include]] + ['-includeall', '-noproxy']
        if self.swig_extra is not None:
            if hasattr(self.swig_extra, 'pop'):
                self.swig_opts.extend(self.swig_extra)
            else:
                self.swig_opts.append(self.swig_extra)

        self.include_dirs.append(openssl_include)
        self.library_dirs.append(openssl_lib)

m2ext = Extension(name="m2ext._m2ext",
                  sources=["swig/m2ext.i"],
                  extra_compile_args=["-DTHREADING"])

setup(
    name='m2ext',
    version='0.1',
    description='M2Crypto Extensions',
    author='Lev Shamardin',
    author_email='shamardin@gmail.com',
    license='BSD',
    url='https://github.com/abbot/m2ext',
    ext_modules = [m2ext],
    packages=["m2ext"],
    cmdclass = {'build_ext': OpensslBuilder},
)
