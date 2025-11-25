from bus.bus import Bus

bus = Bus()

# Carrega instrução ADDI x1, x0, 5 no endereço 0
bus.memory.store_word(0x0000, 0x00500093)

bus.run(3)
