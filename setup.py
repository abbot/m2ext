from distutils.core import setup
from distutils.command import build_ext
from distutils.core import Extension

import os, sys
import platform


def load_description():
    try:
        f = open('README.rst', 'r')
        description = f.read()
        f.close()
        return description
    except:
        return ""


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

        self.swig_opts = ['-I%s' % i for i in self.include_dirs + [openssl_include]] + ['-includeall', '-noproxy']
        if self.swig_extra is not None:
            if hasattr(self.swig_extra, 'pop'):
                self.swig_opts.extend(self.swig_extra)
            else:
                self.swig_opts.append(self.swig_extra)

        # This fixes the build on newer RedHat-based distros
        # See https://gitlab.com/m2crypto/m2crypto/-/issues/100 for more info
        if platform.system() == "Linux":
            # For RedHat-based distros, the '-D__{arch}__' option for
            # Swig needs to be normalized, particularly on i386.
            mach = platform.machine().lower()
            if mach in ('i386', 'i486', 'i586', 'i686'):
                arch = '__i386__'
            elif mach in ('ppc64', 'powerpc64', 'ppc64le', 'ppc64el'):
                arch = '__powerpc64__'
            elif mach in ('ppc', 'powerpc'):
                arch = '__powerpc__'
            else:
                arch = '__%s__' % mach
            self.swig_opts.append('-D%s' % arch)
            if mach in ('ppc64le', 'ppc64el'):
                self.swig_opts.append('-D_CALL_ELF=2')
            if mach in ('arm64_be'):
                self.swig_opts.append('-D__AARCH64EB__')

        # Some Linux distributor has added the following line in
        # /usr/include/openssl/opensslconf.h:
        #
        #     #include "openssl-x85_64.h"
        #
        # This is fine with C compilers, because they are smart enough to
        # handle 'local inclusion' correctly.  Swig, on the other hand, is
        # not as smart, and needs to be told where to find this file...
        #
        # Note that this is risky workaround, since it takes away the
        # namespace that OpenSSL uses.  If someone else has similarly
        # named header files in /usr/include, there will be clashes.
        self.swig_opts.append('-I' + os.path.join(openssl_include, 'openssl'))


m2ext = Extension(name="m2ext._m2ext",
                  sources=["swig/m2ext.i"],
                  extra_compile_args=["-DTHREADING"])

setup(
    name='m2ext',
    version='0.1',
    description='M2Crypto Extensions',
    long_description=load_description(),
    author='Lev Shamardin',
    author_email='shamardin@gmail.com',
    license='BSD',
    url='https://github.com/abbot/m2ext',
    ext_modules = [m2ext],
    packages=["m2ext"],
    cmdclass = {'build_ext': OpensslBuilder},
)
