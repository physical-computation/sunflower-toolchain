Installation Instructions
=========================

Step 1
------
Building the gcc cross-compilers depends on `gcc` (you will likely run into issues trying to build the cross-compiler using `clang`), `libmpc`, `mpfr`, and `gmp`, so make sure you have them installed or the cross-compiler build will fail.

Step 2
------
Edit `conf/setup.conf` and set `$SUNFLOWERROOT`, `$HOST`, `TOOLCC`, and `TOOLCXX` appropriately. You will need to set your `$OSTYPE` environment variable in your shell if it is not already set.  Examples include `darwin` for MacOSX, and the eponymous `OpenBSD`, `linux`, and `solaris`. You will also need to set `MACHTYPE`. A common correct value (depends on your host platform) is `i386`.

Step 3
------
+ Add `$SUNFLOWERROOT/tools/bin` to your path (substitute `$SUNFLOWERROOT` as appropriate)

+ To build the cross-compiler, first populate `tools/source` with the appropriate distributions. There is a script in `tools/source` which will automate this for you by downloading the files using wget, and then uncompressing. You can also manually download the above into `tools/source`. You can delete or overwrite the existing empty stub directories.

+ Due to some bugs in the binutils documentation texinfo files, which are caught by newer versions of makeinfo, you must make sure that your version of makeinfo is older than 5.0 (or you can temporarily make makeinfo unexecutable so that the build skips generating the man pages). Next, type 'make cross' (see NOTE below!) from the root of the installation (the directory containing this README file). That will start the process of configuring the aforementioned distributions to build the cross-compiler suite for the simulator.

+ On Mac OS 10.5 and later, `make cross CFLAGS=-Os` will prevent the build of the cross-compiler from generating `.dylib` debugging symbol files, which currently causes many problems with autoconf related tools.

+ If the cross compiler build fails due, e.g., to difference in behavior between the `perl` or `makeinfo` expected by the GCC build versus what is on your system, you might be able to recover by going into `tools/source/gcc-4.2.4/objdir`, running `make install`, then going to `tools/` and completing the cross compilation by running `make gcc-post; make newlib`
