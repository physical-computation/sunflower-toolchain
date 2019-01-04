Installation Instructions
=========================

Step 1
------
Building the gcc cross-compilers depends on `gcc` (you will likely run into issues trying to build the cross-compiler using `clang`), `libmpc`, `mpfr`, and `gmp`, so make sure you have them installed or the cross-compiler build will fail. On newer versions of macOS, you will need to install gcc (as opposed to using the gcc alias on modern macOS that is just an alias for clang). Because of various design choices made in the implementation of gcc (mixing of C and C++) conventions for source file name extensions, you will need to have a separate `g++` binary that treats its input as either C++ source or C++ object file (you won't be able to get away with calling gcc with `-x c++ -lstdc++ -shared-libgcc`). One version of gcc that fulfills this requirement is `gcc` version 4.9. MacPorts no longer installs separate binaries for gcc versus `g++`, so you will need to use `homebrew` (or some other alternative) to install gcc 4.9 and to set the `TOOLCC` and `TOOLCXX` in appropriately to this gcc-4.9 (more details below). Additionally on macOS Mojave, you need to explicitly install the development headers using
`open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg`

Step 2
------
Edit `conf/setup.conf` and set `$SUNFLOWERROOT`, `TOOLCC`, and `TOOLCXX` appropriately. You will need to set your `$OSTYPE` environment variable in your shell if it is not already set.  Examples include `darwin` for MacOSX, and the eponymous `OpenBSD`, `linux`, and `solaris`. You will also need to set `MACHTYPE`. A common correct value (depends on your host platform) is `i386`.


Step 3
------
+ Add `$SUNFLOWERROOT/tools/bin` to your path (substitute `$SUNFLOWERROOT` as appropriate).

+ To build the cross-compiler, first populate `tools/source` with the appropriate source distributions for gcc, binutils, and newlib. There is a script in `tools/source` which will automate this for you by downloading the files using wget, and then uncompressing. You can also manually download the above into `tools/source`. You can delete or overwrite the existing empty stub directories.

+ Due to some bugs in the `binutils` documentation `texinfo` files, which are caught by newer versions of `makeinfo`, you must make sure that your version of `makeinfo` is older than 5.0 (or you can temporarily make `makeinfo` unexecutable so that the build skips generating the man pages).

+ Next, type `make cross-all` (see NOTE below!) from the root of the installation (the directory containing this README file). That will start the process of configuring the aforementioned distributions to build the cross-compilers for all the supported architectures. See the makefile for the build targets to build just one of the cross-compilers.

+ On Mac OS 10.5 and older versions of macOS, you may need to do `make cross-all CFLAGS=-Os` instead of just `make cross-all` to prevent the build of the cross-compiler from generating `.dylib` debugging symbol files, which currently causes many problems with autoconf related tools.

+ If the cross compiler build fails due, e.g., to difference in behavior between the `perl` or `makeinfo` expected by the GCC build versus what is on your system, you might be able to recover by going into `tools/source/gcc-4.2.4/objdir`, running `make install`, then going to `tools/` and completing the cross compilation by running `make gcc-post; make newlib`.
