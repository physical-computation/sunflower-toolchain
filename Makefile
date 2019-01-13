include conf/setup.conf

Z		= $(PATH):$(SUNFLOWERROOT)/tools/bin

#
#	See
#		https://gcc-help.gcc.gnu.narkive.com/9QCu0XlU/gcc-with-cortex-m4-hard-float-link-error-x-uses-vfp-register-arguments-y-does-not
#	for a good coverage of ARM build flags and multilib.
#
cross-arm:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=arm TARGET-ARCH=arm-none-eabi ADDITIONAL_ARCH_FLAGS="--with-cpu=cortex-m4 --with-fpu=fpv4-sp-d16 --with-mode=thumb --with-float=hard" all;\

cross-superH:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=superH TARGET-ARCH=sh-elf ADDITIONAL_ARCH_FLAGS="--disable-multilib" all;\

cross-riscv:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=riscv TARGET-ARCH=riscv32-elf ADDITIONAL_ARCH_FLAGS="--with-arch=rv32ifd" all;\

cross-all:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=superH TARGET-ARCH=sh-elf ADDITIONAL_ARCH_FLAGS="--disable-multilib" all;\
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=riscv TARGET-ARCH=riscv32-elf ADDITIONAL_ARCH_FLAGS="--with-arch=rv32ifd" all;\
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=arm TARGET-ARCH=arm-none-eabi ADDITIONAL_ARCH_FLAGS="--with-cpu=cortex-m4 --with-fpu=fpv4-sp-d16 --with-mode=thumb --with-float=hard" all;\
#	cd $(TOOLS); $(MAKE) PATH=$(Z)\
#	TARGET=msp430 TARGET-ARCH=msp430 all;\

clean:
	cd $(TOOLS); $(MAKE) nuke; \
	for dir in $(SUPPORTED-TARGETS); do ($(DEL) $(SUNFLOWERROOT)/tools/tools-lib/*/*.a); done
