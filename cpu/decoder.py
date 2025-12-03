from isa.opcodes import OPCODES

class Decoder:

    def decode(self, instr):
        opcode = instr & 0x7F
        funct3 = (instr >> 12) & 0x7
        funct7 = (instr >> 25) & 0x7F

        rs1 = (instr >> 15) & 0x1F
        rs2 = (instr >> 20) & 0x1F
        rd  = (instr >> 7)  & 0x1F

        instr_type = self.get_type(opcode)
        imm = self.get_immediate(instr, instr_type)

        return {
            "raw": instr,
            "opcode": opcode,
            "funct3": funct3,
            "funct7": funct7,
            "rs1": rs1,
            "rs2": rs2,
            "rd": rd,
            "type": instr_type,
            "imm": imm
        }

    def get_type(self, opcode):
        if opcode == OPCODES["OP"]:
            return "R"
        if opcode == OPCODES["OP_IMM"] or opcode == OPCODES["LOAD"] or opcode == OPCODES["JALR"]:
            return "I"
        if opcode == OPCODES["STORE"]:
            return "S"
        if opcode == OPCODES["BRANCH"]:
            return "B"
        if opcode == OPCODES["LUI"] or opcode == OPCODES["AUIPC"]:
            return "U"
        if opcode == OPCODES["JAL"]:
            return "J"
        return "UNKNOWN"

    def get_immediate(self, instr, instr_type):
        if instr_type == "I":
            return ((instr >> 20) & 0xFFF) - ((instr >> 31) * 0x1000)
        if instr_type == "S":
            imm11_5 = (instr >> 25) & 0x7F
            imm4_0  = (instr >> 7) & 0x1F
            return ((imm11_5 << 5) | imm4_0)
        if instr_type == "B":
            imm12   = (instr >> 31) & 0x1
            imm10_5 = (instr >> 25) & 0x3F
            imm4_1  = (instr >> 8) & 0xF
            imm11   = (instr >> 7) & 0x1
            imm = (imm12 << 12) | (imm11 << 11) | (imm10_5 << 5) | (imm4_1 << 1)
            return imm
        if instr_type == "U":
            return instr & 0xFFFFF000
        if instr_type == "J":
            imm20   = (instr >> 31) & 0x1
            imm10_1 = (instr >> 21) & 0x3FF
            imm11   = (instr >> 20) & 0x1
            imm19_12= (instr >> 12) & 0xFF
            imm = (imm20 << 20) | (imm19_12 << 12) | (imm11 << 11) | (imm10_1 << 1)
            return imm
        return 0
