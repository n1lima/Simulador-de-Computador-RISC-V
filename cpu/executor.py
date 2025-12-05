class Executor:
    def __init__(self, regs, bus, cpu):
        self.regs = regs
        self.bus = bus
        self.cpu = cpu

    def execute(self, d):
        opcode = d["opcode"]
        t = d["type"]

        if t == "J":  
            if opcode == 0b1101111:
                self.exec_jal(d)
                return

        elif t == "I":  
            if opcode == 0b1100111:
                self.exec_jalr(d)
                return
            elif opcode == 0b0010011:  
                self.exec_op_imm(d)
                return
            elif opcode == 0b0000011: 
                self.exec_load(d)
                return
            
        elif t == "S":
            if opcode == 0b0100011: 
                self.exec_store(d)
                return
            
        elif t == "U":
            if opcode == 0b0110111:  
                self.exec_lui(d)
                return
            elif opcode == 0b0010111: 
                self.exec_auipc(d)
                return

        elif t == "R": 
            if opcode == 0b0110011:  
                self.exec_op(d)
                return

        elif t == "B":  
            if opcode == 0b1100011: 
                self.exec_branch(d)
                return

    # I-TYPE (ADDI, ANDI, ORI, XORI)
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

    #R-TYPE (ADD, SUB, AND, OR, XOR)
    def exec_op(self, d):
        rs1_val = self.regs.read(d["rs1"])
        rs2_val = self.regs.read(d["rs2"])
        funct3 = d["funct3"]
        funct7 = d["funct7"]

        #ADD
        if funct3 == 0b000 and funct7 == 0b0000000:
            result = rs1_val + rs2_val
            self.regs.write(d["rd"], result)
            print(f"ADD x{d['rd']} = x{d['rs1']} + x{d['rs2']} -> {result}")

        #SUB
        elif funct3 == 0b000 and funct7 == 0b0100000:
            result = rs1_val - rs2_val
            self.regs.write(d["rd"], result)
            print(f"SUB x{d['rd']} = x{d['rs1']} - x{d['rs2']} -> {result}")

        #XOR
        elif funct3 == 0b100 and funct7 == 0b0000000:
            result = rs1_val ^ rs2_val
            self.regs.write(d["rd"], result)
            print(f"XOR x{d['rd']} = x{d['rs1']} XOR x{d['rs2']} -> {result}")

        #OR
        elif funct3 == 0b110 and funct7 == 0b0000000:
            result = rs1_val | rs2_val
            self.regs.write(d["rd"], result)
            print(f"OR x{d['rd']} = x{d['rs1']} OR x{d['rs2']} -> {result}")

        #AND
        elif funct3 == 0b111 and funct7 == 0b0000000:
            result = rs1_val & rs2_val
            self.regs.write(d["rd"], result)
            print(f"AND x{d['rd']} = x{d['rs1']} AND x{d['rs2']} -> {result}")


    #B-TYPE (BEQ, BNE, BLT, BGE)
    def exec_branch(self, d):
        rs1_val = self.regs.read(d["rs1"])
        rs2_val = self.regs.read(d["rs2"])
        imm = d["imm"] 
        funct3 = d["funct3"]

        taken = False

        #BEQ
        if funct3 == 0b000:
            taken = (rs1_val == rs2_val)
            cond = "BEQ"

        #BNE
        elif funct3 == 0b001:
            taken = (rs1_val != rs2_val)
            cond = "BNE"

        #BLT (signed)
        elif funct3 == 0b100:
            taken = (rs1_val < rs2_val)
            cond = "BLT"

        #BGE (signed)
        elif funct3 == 0b101:
            taken = (rs1_val >= rs2_val)
            cond = "BGE"

        #Executa o desvio se condição for verdadeira
        if taken:
            self.cpu.pc += imm - 4

            real_pc = self.cpu.pc + 4

            print(f"{cond}: salto tomado -> PC += {imm} (novo PC = {real_pc:08x})")
        else:
            print(f"{cond}: salto NÃO tomado")

    # JAL (Jump And Link)
    def exec_jal(self, d):
        rd  = d["rd"]
        imm = d["imm"]

        ret_addr = self.cpu.pc + 4
        self.regs.write(rd, ret_addr)

        self.cpu.pc += imm - 4

        real_pc = self.cpu.pc + 4
        print(f"JAL x{rd}, {imm} -> PC = {real_pc:08X} (retorno = {ret_addr:08X})")

    # JALR (Jump And Link Register)
    def exec_jalr(self, d):
        rd  = d["rd"]
        rs1 = d["rs1"]
        imm = d["imm"]

        rs1_val = self.regs.read(rs1)

        ret_addr = self.cpu.pc + 4
        self.regs.write(rd, ret_addr)

        target = (rs1_val + imm) & ~1

        self.cpu.pc = target - 4

        real_pc = self.cpu.pc + 4
        print(f"JALR x{rd}, x{rs1}, {imm} -> PC = {real_pc:08X} (retorno = {ret_addr:08X})")
    
    #LOAD (LW)
    def exec_load(self, d):
        rs1_val = self.regs.read(d["rs1"])
        imm = d["imm"]
        addr = rs1_val + imm

        funct3 = d["funct3"]

        if funct3 == 0b010:
            value = self.bus.read(addr)
            self.regs.write(d["rd"], value)
            print(f"LW x{d['rd']} = MEM[{addr:#010x}] -> {value}")

    #STORE(SW)
    def exec_store(self, d):
        base = self.regs.read(d["rs1"])
        src_val = self.regs.read(d["rs2"])
        imm = d["imm"]

        addr = base + imm

        funct3 = d["funct3"]
  
        if funct3 == 0b010:
            self.bus.write(addr, src_val)
            print(f"SW MEM[{addr:#010x}] = x{src_val} (x{d['rs2']})")

    #LUI
    def exec_lui(self, d):
        imm = d["imm"]      
        self.regs.write(d["rd"], imm)
        print(f"LUI x{d['rd']} = {hex(imm)}")

    #AUIPC
    def exec_auipc(self, d):
        imm = d["imm"]               
        result = self.cpu.pc + imm
        self.regs.write(d["rd"], result)
        print(f"AUIPC x{d['rd']} = PC[{self.cpu.pc:08X}] + {hex(imm)} -> {hex(result)}")

