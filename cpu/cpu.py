from cpu.registers import Registers
from cpu.decoder import Decoder
from cpu.executor import Executor

class CPU:
    def __init__(self, bus):
        #PC sempre começa em 0 (início do programa)
        self.pc = 0
        self.regs = Registers()
        self.bus = bus  
        self.decoder = Decoder()
        self.executor = Executor(self.regs, self.bus, self)

    def step(self):
        #CPU sempre busca a instrução apontada pelo PC
        instr = self.bus.read(self.pc)

        print(f"PC = {self.pc:08X} | Instr = {instr:08X}")

        #Etapa 2: decodificação
        decoded = self.decoder.decode(instr)

        #Etapa 3: execução
        self.executor.execute(decoded)

        #Avança para a próxima instrução (4 bytes)
        self.pc += 4
