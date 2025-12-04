class Executor:
    def __init__(self, regs, memory):
        self.regs = regs
        self.memory = memory

    def execute(self, d):
        opcode = d["opcode"]
        funct3 = d["funct3"]
        funct7 = d["funct7"]

        if d["type"] == "I":  # I-TYPE (ADDI, ANDI, ORI, XORI)
            if opcode == 0b0010011:  # OP-IMM
                self.exec_op_imm(d)

        elif d["type"] == "R":  # R-TYPE (ADD, SUB, AND, OR, XOR)
            if opcode == 0b0110011:  # OP
                self.exec_op(d)

    # ----------------------------------------------
    # I-TYPE (ADDI, ANDI, ORI, XORI)
    # ----------------------------------------------
    def exec_op_imm(self, d):
        rs1_val = self.regs.read(d["rs1"])
        imm = d["imm"]
        funct3 = d["funct3"]

        # ADDI
        if funct3 == 0b000:
            result = rs1_val + imm
            self.regs.write(d["rd"], result)
            print(f"ADDI x{d['rd']} = x{d['rs1']} + {imm} -> {result}")

        # XORI
        elif funct3 == 0b100:
            result = rs1_val ^ imm
            self.regs.write(d["rd"], result)
            print(f"XORI x{d['rd']} = x{d['rs1']} XOR {imm} -> {result}")

        # ORI
        elif funct3 == 0b110:
            result = rs1_val | imm
            self.regs.write(d["rd"], result)
            print(f"ORI x{d['rd']} = x{d['rs1']} OR {imm} -> {result}")

        # ANDI
        elif funct3 == 0b111:
            result = rs1_val & imm
            self.regs.write(d["rd"], result)
            print(f"ANDI x{d['rd']} = x{d['rs1']} AND {imm} -> {result}")

    # ----------------------------------------------
    # R-TYPE (ADD, SUB, AND, OR, XOR)
    # ----------------------------------------------
    def exec_op(self, d):
        rs1_val = self.regs.read(d["rs1"])
        rs2_val = self.regs.read(d["rs2"])
        funct3 = d["funct3"]
        funct7 = d["funct7"]

        # ADD
        if funct3 == 0b000 and funct7 == 0b0000000:
            result = rs1_val + rs2_val
            self.regs.write(d["rd"], result)
            print(f"ADD x{d['rd']} = x{d['rs1']} + x{d['rs2']} -> {result}")

        # SUB
        elif funct3 == 0b000 and funct7 == 0b0100000:
            result = rs1_val - rs2_val
            self.regs.write(d["rd"], result)
            print(f"SUB x{d['rd']} = x{d['rs1']} - x{d['rs2']} -> {result}")

        # XOR
        elif funct3 == 0b100 and funct7 == 0b0000000:
            result = rs1_val ^ rs2_val
            self.regs.write(d["rd"], result)
            print(f"XOR x{d['rd']} = x{d['rs1']} XOR x{d['rs2']} -> {result}")

        # OR
        elif funct3 == 0b110 and funct7 == 0b0000000:
            result = rs1_val | rs2_val
            self.regs.write(d["rd"], result)
            print(f"OR x{d['rd']} = x{d['rs1']} OR x{d['rs2']} -> {result}")

        # AND
        elif funct3 == 0b111 and funct7 == 0b0000000:
            result = rs1_val & rs2_val
            self.regs.write(d["rd"], result)
            print(f"AND x{d['rd']} = x{d['rs1']} AND x{d['rs2']} -> {result}")
