#!/usr/bin/env python3
import fileinput
import struct
import sys
import subprocess
import re
import os

#
# This script modifies an elf executable file generated by Harry Sarson's patched
# RISC-V assembler.
#
# The first command line argument is interpretted as an elf executable file.
#
# The binary will be "fixed" in place.
#
# Errors and warnings are written to stderr.
#
# ---
#
# The patching of gas and ld for UNFSW and UNFLW transpired to be too hard due to
# a lack of understanding about the way memory addresses are relocated.
#
# Therefore, the binary for uncertain load/stores generated by these tools
# currently has the correct destination register and offset for the uncertainty
# but not for the best guess - which are both set to zero.
#
# For any unfsw and unflw instructions in the binary, this script will copy
# the destination register and offset for the uncertainty into the following
# 32 bits.
#

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_text_start_end(file):
    elf_info = subprocess.Popen(['readelf', file_name, '-hS'], stdout=subprocess.PIPE).stdout.read(-1)
    text_offset_and_size = re.search(
        r"\.text\s*\w*\s*\w*\s*(\w*)\s*(\w*)",
        str(elf_info, 'utf-8')
        , re.MULTILINE
        ).group(1, 2)

    machine_type = re.search(
        r"^\s*Machine:\s*(.+)$",
        str(elf_info, 'utf-8')
        , re.MULTILINE
    ).group(1)

    assert machine_type == "RISC-V", "Expected a RISC-V elf file, found machine: {}".format(machine_type)

    text_offset_bytes = int(text_offset_and_size[0], 16)
    text_size_bytes = int(text_offset_and_size[1], 16)
    assert text_offset_bytes % 4 == 0, "Text size must be a multiple of 4"
    assert text_size_bytes % 4 == 0, "Text size must be a multiple of 4"
    text_offset = text_offset_bytes // 4
    text_size = text_size_bytes // 4
    return (text_offset, text_offset + text_size)


file_name = sys.argv[1]

with open(file_name, mode='rb+') as file:
    try:
        prev_instruction_if_uncertain = None
        words_read = 0
        (text_start, text_end) = get_text_start_end(file_name)
        for chunk in iter((lambda:file.read(4)),b''):
            newChunk = chunk
            if words_read >= text_start and words_read < text_end:
                (int_value,) = struct.unpack('<I', chunk)

                if int_value & 0x3 != 0x3 and int_value != 0:
                    eprint("Possible compressed instruction found (0x{:04X}) at {} bytes into the file\n".format(
                            int_value & 0xFFFF,
                            words_read * 4
                            ) +
                        "    We do not suppport compressed instructions.")

                if prev_instruction_if_uncertain != None:
                    dest_register_mask = 0x000F8000
                    load_offset_mask = 0xFFF00000
                    store_offset_mask = 0xFE000F80
                    dest_register = prev_instruction_if_uncertain & dest_register_mask
                    offset = prev_instruction_if_uncertain & load_offset_mask
                    if int_value & 0x7F == 0x7:
                        assert not (int_value & dest_register_mask), "Expected destination register to be zeroed out."
                        assert not (int_value & load_offset_mask), "Expected offset to be zeroed out."
                        corrected_value = int_value | dest_register | offset
                        # eprint("load ", hex(int_value), hex(corrected_value))
                        newChunk = struct.pack('<I', corrected_value)
                    elif int_value & 0x7F == 0x27:
                        assert not (int_value & dest_register_mask), "Expected destination register to be zeroed out."
                        assert not (int_value & store_offset_mask), "Expected offset to be zeroed out."
                        corrected_value = int_value | dest_register | (offset & 0xFE000000) | ((offset & 0x01F00000) >> 13)
                        # eprint("store", hex(int_value), hex(corrected_value))
                        newChunk = struct.pack('<I', corrected_value)

                if int_value & 0x7FFF == 0x70BF:
                    assert prev_instruction_if_uncertain == None, "Uncertain 32 bit sections should never occur back to back."
                    prev_instruction_if_uncertain = int_value
                else:
                    prev_instruction_if_uncertain = None

            file.seek(words_read * 4)
            file.write(newChunk)
            words_read = words_read + 1
    except Exception as e:
        # We do this to make make recompile this file
        os.unlink(file.name)
        raise e
