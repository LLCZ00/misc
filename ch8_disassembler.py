#!/usr/bin/python3

"""
Chip-8 Disassembler
- Disassemble
- Dump bytes/offsets
"""
import sys
import os


class Instruction_Disassemble:
    """2-byte instructions, the first nibble (4 bits)
    being the actual opcode, followed by various operands
    (values, registers, memory locations, etc.)
    """
    def __init__(self, instruction, verbose=True):
        self.instruction = instruction
        self._opcode = (self.instruction >> 12) & 0xF
        self._nib2 = (self.instruction >> 8) & 0xF
        self._nib3 = (self.instruction >> 4) & 0xF
        self._nib4 = self.instruction & 0xF
        self._last2 = self.instruction & 0xFF
        self._last3 = self.instruction & 0xFFF
        self.comment = ""
        self.verbose = verbose

    def __repr__(self):
      return str(self)

    def __str__(self):
        result = self.translate()
        if self.verbose and self.comment:
            result += f" ; {self.comment}"
        return result

    def translate(self):
        instr_str = f"Unknown opcode: {hex(self.instruction)}"
        if self._opcode == 0:
            if self.instruction == 0x00E0:
                instr_str = "CLS"
            elif self.instruction == 0x00EE:
                instr_str = "RET"
            elif self.instruction == 0x0:
                instr_str = ""
            else:
                instr_str = f"Call {hex(self._last3)} ; (Deprecated)"

        elif self._opcode == 1:
            instr_str = f"JP {hex(self._last3)}"

        elif self._opcode == 2:
            instr_str = f"Call {hex(self._last3)}"

        elif self._opcode == 3:
            instr_str = f"SE V{hex(self._nib2)[2:]}, {hex(self._last2)}"
            self.comment = "Skip next instruction if Vx == byte"

        elif self._opcode == 4:
            instr_str = f"SNE V{hex(self._nib2)[2:]}, {hex(self._last2)}"
            self.comment = "Skip next instruction if Vx != byte"

        elif self._opcode == 5:
            instr_str = f"SE V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            self.comment = "Skip next instruction if Vx == Vy"

        elif self._opcode == 6:
            instr_str = f"LD V{hex(self._nib2)[2:]}, {hex(self._last2)}"
            self.comment = "Vx = byte"

        elif self._opcode == 7:
            instr_str = f"ADD V{hex(self._nib2)[2:]}, {hex(self._last2)}"
            self._opcode = "Vx += byte (Carry flag not changed)"

        elif self._opcode == 8:
            if self._nib4 == 0:
                instr_str = f"LD V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
                self.comment = "Vx = Vy"
            elif self._nib4 == 1:
                instr_str = f"OR V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 2:
                instr_str = f"AND V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 3:
                instr_str = f"XOR V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 4:
                instr_str = f"ADD V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 5:
                instr_str = f"SUB V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 6:
                instr_str = f"SHR V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 7:
                instr_str = f"SUBN V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            elif self._nib4 == 0xE:
                instr_str = f"SHL V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"

        elif self._opcode == 9:
            instr_str = f"SNE V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}"
            self.comment = "Skip next instruction if Vx != Vy"

        elif self._opcode == 0xA:
            instr_str = f"LD I, {hex(self._last3)}"
            self.comment = "Set I to addr"

        elif self._opcode == 0xB:
            instr_str = f"JP V0, {hex(self._last3)}"
            self.comment = "Jump to addr + V0"

        elif self._opcode == 0xC:
            instr_str = f"RND V{hex(self._nib2)[2:]}, {hex(self._last2)}"
            self.comment = "Vx = rand() % byte"

        elif self._opcode == 0xD:
            instr_str = f"DRW V{hex(self._nib2)[2:]}, V{hex(self._nib3)[2:]}, {hex(self._nib4)}"
            self.comment = "draw(Vx, Vy, N)"

        elif self._opcode == 0xE:
            if self._last2 == 0x9E:
                instr_str = f"SKP V{hex(self._nib2)[2:]}"
                self.comment = "Skips next instruction if the key stored in VX is pressed"
            elif self._last2 == 0xA1:
                instr_str = f"SKNP V{hex(self._nib2)[2:]}"
                self.comment = "Skips next instruction if the key stored in VX is not pressed"

        elif self._opcode == 0xF:
            if self._last2 == 0x07:
                instr_str = f"LD V{hex(self._nib2)[2:]}, DT"
                self.comment = "Vx = get_delay()"
            elif self._last2 == 0x0A:
                instr_str = f"LD V{hex(self._nib2)[2:]}, K"
                self.comment = "Vx = get_key()"
            elif self._last2 == 0x15:
                instr_str = f"LD DT, V{hex(self._nib2)[2:]}"
                self.comment = "delay_timer(Vx)"
            elif self._last2 == 0x18:
                instr_str = f"LD ST, V{hex(self._nib2)[2:]}"
                self.comment = "sound_timer(Vx)"
            elif self._last2 == 0x1E:
                instr_str = f"ADD I, V{hex(self._nib2)[2:]}"
                self.comment = "I += Vx"
            elif self._last2 == 0x29:
                instr_str = f"LD F, V{hex(self._nib2)[2:]}"
                self.comment = "Sets I to the location of the sprite for the character in Vx"
            elif self._last2 == 0x33:
                instr_str = f"LD B, V{hex(self._nib2)[2:]}"
                self.comment = "Store binary-coded decimal"
            elif self._last2 == 0x55:
                instr_str = f"LD [I], V{hex(self._nib2)[2:]}"
                self.comment = "reg_dump(Vx, &I)"
            elif self._last2 == 0x65:
                instr_str = f"LD V{hex(self._nib2)[2:]}, [I]"
                self.comment = "reg_load(Vx, &I)"

        return instr_str 


class ROMFile:
    byte_format = hex
    def __init__(self, path):
        self.rom_path = path

    def rawbytes(self):
        """Generator yielding each 2-byte instruction and
        its offset from ROM file 
        """
        with open(self.rom_path , 'rb') as rom:
            for instruction in iter(lambda: rom.read(2), b""):
                yield instruction, (rom.tell() - 2)

    def assemble(self):
        pass


    def dump(self, disass=True, verbose=True):
        """Print 'offset: instruction' for given Chip-8 ROM file

        :param disass: Translate opcodes from bytes to instructions if True, otherwise just print the hex
        :type disass: bool
        :param verbose: Prints comments alongside comments, if True
        :type verbose: bool
        """
        for byte_instruction, offset in self.rawbytes():
            if disass:
                byte_instruction = Instruction_Disassemble(int.from_bytes(byte_instruction, "big"), verbose=verbose)
            else:
                byte_instruction = self.byte_format(int.from_bytes(byte_instruction, "big"))

            print(f"{self.byte_format(offset)}: {byte_instruction}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{__file__} FILEPATH")
        sys.exit(1)

    rom_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(rom_path):
        print(f"ROM file not found '{rom_path}'")
        sys.exit(1)

    c8d = ROMFile(rom_path)
    c8d.dump(verbose=False)
    

