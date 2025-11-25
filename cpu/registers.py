class Registers:
    def __init__(self):
        # 32 registradores de 32 bits
        self.reg = [0] * 32

    def read(self, idx):
        return self.reg[idx]

    def write(self, idx, value):
        if idx != 0:  # x0 sempre 0
            self.reg[idx] = value & 0xFFFFFFFF
