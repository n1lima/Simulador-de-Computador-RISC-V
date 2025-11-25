from cpu.registers import Registers
from cpu.decoder import Decoder
from cpu.executor import Executor

class CPU:
    def __init__(self, memory):
        self.pc = 0
        self.regs = Registers()
        self.memory = memory
        self.decoder = Decoder()
        self.executor = Executor(self.regs, self.memory)

    def step(self):
        instr = self.memory.load_word(self.pc)

        print(f"PC = {self.pc:08X} | Instr = {instr:08X}")

        decoded = self.decoder.decode(instr)
        self.executor.execute(decoded)

        self.pc += 4
