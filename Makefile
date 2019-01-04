include conf/setup.conf

Z		= $(PATH):$(SUNFLOWERROOT)/tools/bin

cross-superH:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=superH TARGET-ARCH=sh-elf ADDITIONAL_ARCH_FLAGS="" all;\

cross-riscv:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=riscv TARGET-ARCH=riscv32-elf ADDITIONAL_ARCH_FLAGS="--with-arch=rv32i" all;\

cross-all:
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=superH TARGET-ARCH=sh-elf all;\
	cd $(TOOLS); $(MAKE) PATH=$(Z)\
	TARGET=riscv TARGET-ARCH=riscv32-elf ADDITIONAL_ARCH_FLAGS="--with-arch=rv32i" all;\
#	cd $(TOOLS); $(MAKE) PATH=$(Z)\
#	TARGET=msp430 TARGET-ARCH=msp430 all;\

clean:
	cd $(TOOLS); $(MAKE) nuke; \
	for dir in $(SUPPORTED-TARGETS); do ($(DEL) $(SUNFLOWERROOT)/tools/tools-lib/*/*.a); done
