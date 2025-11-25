class Memory:
    def __init__(self, size=0xA0000):  # RAM + VRAM + reservados
        self.mem = [0] * size

    def load_word(self, addr):
        b0 = self.mem[addr]
        b1 = self.mem[addr + 1]
        b2 = self.mem[addr + 2]
        b3 = self.mem[addr + 3]
        return (b3 << 24) | (b2 << 16) | (b1 << 8) | b0

    def store_word(self, addr, value):
        self.mem[addr]     = value & 0xFF
        self.mem[addr+1]   = (value >> 8) & 0xFF
        self.mem[addr+2]   = (value >> 16) & 0xFF
        self.mem[addr+3]   = (value >> 24) & 0xFF
