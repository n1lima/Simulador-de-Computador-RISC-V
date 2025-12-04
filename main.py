from bus.bus import Bus

bus = Bus()

bus.memory.store_word(0x0000, 0x00F00093)

bus.memory.store_word(0x0004, 0x0050F113)

bus.memory.store_word(0x0008, 0x0020C1B3)

# Executa 3 instruções
bus.run(3)

# Verificando resultados nos registradores
print("x1 =", bus.cpu.regs.read(1)) 
print("x2 =", bus.cpu.regs.read(2)) 
print("x3 =", bus.cpu.regs.read(3)) 
