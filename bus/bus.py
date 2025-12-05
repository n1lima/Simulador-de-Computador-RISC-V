from memory.memory import Memory
from cpu.cpu import CPU

class Bus:
    def __init__(self):
        #Contador de instruções para E/S Programada (VRAM)
        self.instruction_count = 0
        self.INSTRUCTIONS_PER_VRAM_UPDATE = 10 
    
        #MAPEAMENTO OFICIAL
        self.RAM_START  = 0x00000
        self.RAM_END    = 0x7FFFF  #512 KB

        self.VRAM_START = 0x80000
        self.VRAM_END   = 0x8FFFF  #64 KB

        self.RES_START  = 0x90000
        self.RES_END    = 0x9FBFF  #reservado

        self.IO_START   = 0x9FC00
        self.IO_END     = 0x9FFFF  #periféricos (nao utilizado)

        # Cada região recebe uma Memory separada
        self.ram = Memory(self.RAM_END - self.RAM_START + 1)
        self.vram = Memory(self.VRAM_END - self.VRAM_START + 1)
        self.res = Memory(self.RES_END - self.RES_START + 1) 
        self.io = Memory(self.IO_END - self.IO_START + 1)

        #BARRAMENTO LÓGICO 
        self.address_bus = 0       
        self.data_bus = 0         
        self.control_bus = {       
            "mem_read": False,
            "mem_write": False
        }
  
        #inicializa a CPU ligada ao bus
        self.cpu = CPU(self)

    #BUS MAIN LOOP: Adiciona a verificação da VRAM
    def run(self, steps=10):
        print(f"--- INICIANDO SIMULAÇÃO ({steps} passos) ---")
        for i in range(steps):
            print(f"\n[{i+1}/{steps}] Executando instrução no PC: {hex(self.cpu.pc)}")
            self.cpu.step()
            self.instruction_count += 1
            
           #Verifica se deve exibir a VRAM
            self.check_vram_display()

        print("--- SIMULAÇÃO FINALIZADA ---")

    # EXIBE A VRAM A CADA N INSTRUÇÕES
    def check_vram_display(self):
        if self.instruction_count % self.INSTRUCTIONS_PER_VRAM_UPDATE == 0:
            vram_output = ""

            for offset in range(self.VRAM_END - self.VRAM_START + 1):
                byte = self.vram.mem[offset] & 0xFF

                if 32 <= byte <= 126:  #printable ASCII
                    vram_output += chr(byte)
                else:
                    vram_output += ' '  

            print("\n================ VRAM DISPLAY ================")
            print(vram_output.strip())
            print("==============================================")
    
   
    #LEITURA DE MEMÓRIA (LW)
    def read(self, address):

        self.address_bus = address
        self.control_bus["mem_read"] = True
        self.control_bus["mem_write"] = False
        data = 0 

        if self.RAM_START <= address <= self.RAM_END:
            data = self.ram.load_word(address - self.RAM_START)

        elif self.VRAM_START <= address <= self.VRAM_END:
            data = self.vram.load_word(address - self.VRAM_START)

        elif self.IO_START <= address <= self.IO_END:
            print(f"[BUS] Leitura de Periférico: {hex(address)}")
            data = self.io.load_word(address - self.IO_START)

        else:
            print(f"[BUS] Endereço inválido READ: {hex(address)}")
            
        self.control_bus["mem_read"] = False
        self.data_bus = data
        return data

    #ESCRITA DE MEMÓRIA (SW)
    def write(self, address, data):

        self.address_bus = address
        self.data_bus = data
        self.control_bus["mem_write"] = True
        self.control_bus["mem_read"] = False

        if self.RAM_START <= address <= self.RAM_END:
            self.ram.store_word(address - self.RAM_START, data)

        elif self.VRAM_START <= address <= self.VRAM_END:
            #VRAM usa armazenamento byte a byte
            self.vram.store_byte(address - self.VRAM_START, data & 0xFF)
            print(f"[BUS] VRAM BYTE em {hex(address)} = '{chr(data & 0xFF)}'") 

        elif self.IO_START <= address <= self.IO_END:
            print(f"[BUS] Escrita em Periférico: {hex(address)}, Valor: {data}")
            self.io.store_word(address - self.IO_START, data)

        else:
            print(f"[BUS] Endereço inválido WRITE: {hex(address)}")

        self.control_bus["mem_write"] = False