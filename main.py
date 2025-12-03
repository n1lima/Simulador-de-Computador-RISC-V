from bus.bus import Bus

bus = Bus()

#ADDI x1, x0, 5 no endereço 0
bus.memory.store_word(0x0000, 0x00500093)

bus.run(3)

# --> teste para parte de lógica de decodificação de instrução <--

d = bus.cpu.decoder.decode(0x00500093)
print(d)
