from bus.bus import Bus
from asm.asm import lui, addi, sw

bus = Bus()

#Programa RISC-V escrito diretamente na RAM
#Objetivo: escrever "Hi" na VRAM

# x1 = 0x80000 (base da VRAM)
bus.ram.store_word(0x00000, lui(1, 0x80))     
bus.ram.store_word(0x00004, addi(1, 1, 0))  

# x2 = 'H' 
bus.ram.store_word(0x00008, addi(2, 0, 0x48))
bus.ram.store_word(0x0000C, sw(2, 1, 0)) # VRAM[0]

# x2 = 'i' 
bus.ram.store_word(0x00010, addi(2, 0, 0x69))
bus.ram.store_word(0x00014, sw(2, 1, 1))  # VRAM[1]

#roda programa em 20 instruções
bus.run(20)
