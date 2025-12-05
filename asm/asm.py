#Mini Assembler RISC-V RV32I - GERA INSTRUÇÕES BINARIAS DE 32 BITS

def sign_mask(value, bits):
    if value & (1 << (bits - 1)):
        value |= -1 << bits
    return value & 0xFFFFFFFF

def addi(rd, rs1, imm):
    imm = sign_mask(imm, 12)
    opcode = 0b0010011
    funct3 = 0b000
    inst = (
        (imm & 0xFFF) << 20 |
        (rs1 & 0x1F) << 15 |
        (funct3 & 0x7) << 12 |
        (rd & 0x1F) << 7 |
        opcode
    )
    return inst


def jalr(rd, rs1, imm):
    imm = sign_mask(imm, 12)
    opcode = 0b1100111
    funct3 = 0b000
    inst = (
        (imm & 0xFFF) << 20 |
        (rs1 & 0x1F) << 15 |
        (funct3 & 0x7) << 12 |
        (rd & 0x1F) << 7 |
        opcode
    )
    return inst

def add(rd, rs1, rs2):
    opcode = 0b0110011
    funct3 = 0
    funct7 = 0
    inst = (
        (funct7 << 25) |
        (rs2 << 20) |
        (rs1 << 15) |
        (funct3 << 12) |
        (rd << 7) |
        opcode
    )
    return inst

def jal(rd, imm):
    imm = sign_mask(imm, 21)

    opcode = 0b1101111

    imm20   = (imm >> 20) & 0x1
    imm10_1 = (imm >> 1)  & 0x3FF
    imm11   = (imm >> 11) & 0x1
    imm19_12= (imm >> 12) & 0xFF

    inst = (
        (imm20 << 31) |
        (imm19_12 << 12) |
        (imm11 << 20) |
        (imm10_1 << 21) |
        (rd << 7) |
        opcode
    )
    return inst

def branch(funct3, rs1, rs2, imm):
    imm = sign_mask(imm, 13)
    opcode = 0b1100011

    imm12   = (imm >> 12) & 1
    imm10_5 = (imm >> 5) & 0x3F
    imm4_1  = (imm >> 1) & 0xF
    imm11   = (imm >> 11) & 1

    inst = (
        (imm12   << 31) |
        (imm10_5 << 25) |
        (rs2     << 20) |
        (rs1     << 15) |
        (funct3  << 12) |
        (imm4_1  << 8)  |
        (imm11   << 7)  |
        opcode
    )
    return inst


def beq(rs1, rs2, imm): return branch(0b000, rs1, rs2, imm)
def bne(rs1, rs2, imm): return branch(0b001, rs1, rs2, imm)
def blt(rs1, rs2, imm): return branch(0b100, rs1, rs2, imm)
def bge(rs1, rs2, imm): return branch(0b101, rs1, rs2, imm)

def lw(rd, rs1, imm):
    imm = sign_mask(imm, 12)
    opcode = 0b0000011
    funct3 = 0b010
    inst = (
        (imm & 0xFFF) << 20 |
        (rs1 & 0x1F) << 15 |
        (funct3 & 0x7) << 12 |
        (rd & 0x1F) << 7 |
        opcode
    )
    return inst

def sw(rs2, rs1, imm):
    imm = sign_mask(imm, 12)
    opcode = 0b0100011
    funct3 = 0b010

    imm11_5 = (imm >> 5) & 0x7F
    imm4_0  = (imm & 0x1F)

    inst = (
        (imm11_5 << 25) |
        (rs2 << 20) |   
        (rs1 << 15) |  
        (funct3 << 12) |
        (imm4_0 << 7) |
        opcode
    )
    return inst

def lui(rd, imm20):
    imm = imm20 << 12
    opcode = 0b0110111
    return (imm & 0xFFFFF000) | (rd << 7) | opcode

def auipc(rd, imm20):
    imm = imm20 << 12
    opcode = 0b0010111
    return (imm & 0xFFFFF000) | (rd << 7) | opcode

