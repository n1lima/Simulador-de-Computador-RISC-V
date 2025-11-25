from memory.memory import Memory
from cpu.cpu import CPU

class Bus:
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)

    def run(self, steps=10):
        for _ in range(steps):
            self.cpu.step()
