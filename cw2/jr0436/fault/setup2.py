from distutils.core import setup, Extension

setup(name = "Fault",
      version = "1.0",
      ext_modules = [Extension('stage2', ['stage2.c'],
      	extra_compile_args=['-std=gnu99'],
      	extra_link_args=['-lcrypto'])])
