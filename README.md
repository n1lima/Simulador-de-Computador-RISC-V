# Simulador de Computador RISC-V (RV32I)

Este projeto é um simulador de arquitetura de computador baseado no conjunto de instruções **RISC-V RV32I Base Integer ISA**, desenvolvido em Python. O simulador segue uma arquitetura modular de ciclo único e implementa os principais componentes de um sistema computacional: **CPU**, **Barramento** e **Memória** (RAM/VRAM).


## Funcionalidades

* **CPU RV32I Completa:** Implementação de um processador de ciclo único com suporte a registradores e execução de instruções.
* **Barramento (Bus):** Implementação de barramentos de endereço, dados e controle para comunicação entre os módulos.
* **Mapeamento de Memória:** O sistema gerencia diferentes regiões de memória (RAM Principal, VRAM, I/O).
* **E/S Programada (VRAM):** O conteúdo da VRAM é periodicamente exibido no terminal, simulando um display de vídeo com caracteres ASCII.
* **Mini-Assembler:** Módulo em Python para montagem de instruções RISC-V de 32 bits, facilitando a criação de programas de teste (`asm.py`).
* **Conjunto de Instruções Implementado:** Suporte para instruções R-Type, I-Type, S-Type, B-Type, U-Type e J-Type.


## Estrutura de Pastas
### Componentes Principais

| Arquivo | Descrição |
| :--- | :--- |
| `cpu/cpu.py` | Responsável pelo ciclo de relógio (step), buscando instruções do barramento, decodificando e as enviando para o executor. |
| `cpu/registers.py` | Implementa o banco de 32 registradores RISC-V (`x0` é fixo em zero). |
| `cpu/decoder.py` | Extrai os campos da instrução (opcode, rd, rs1, rs2, funct3, funct7) e calcula o valor imediato (`imm`), identificando o tipo de instrução (R, I, S, B, U, J). |
| `cpu/executor.py` | Contém as funções para a lógica de execução (ALU) de cada instrução implementada. |
| `bus/bus.py` | Gerencia o acesso e o mapeamento de endereços para as diferentes regiões de memória (RAM, VRAM, I/O). |
| `memory/memory.py` | Implementa uma memória simples, endereçável por byte, com métodos para leitura e escrita de palavras (32 bits) e bytes (8 bits). |
| `asm/asm.py` | Oferece funções para gerar as representações binárias das instruções RV32I, incluindo tratamento de sinal (`sign_mask`). |


## Mapeamento de Memória

O Barramento (`bus.py`) utiliza o seguinte mapeamento de memória, conforme a especificação do projeto[cite: 410]:

| Faixa de Endereço (Hex) | Tamanho | Descrição | Módulo |
| :--- | :--- | :--- | :--- |
| **0x00000** - **0x7FFFF** | 512 KB | RAM Principal (Código, Dados, Pilha)  | `self.ram` |
| **0x80000** - **0x8FFFF** | 64 KB | VRAM (Vídeo RAM)  | `self.vram` |
| **0x90000** - **0x9FBFF** | Reservado | Área Reservada para Expansão  | `self.res` |
| **0x9FC00** - **0x9FFFF** | 1 KB | Periféricos de Hardware (E/S Mapeada)  | `self.io` |


## Como Executar

O simulador é executado através do arquivo principal `main.py`, que carrega um programa de teste na RAM e inicia a simulação.

### Programa de Teste

O `main.py` carrega na memória principal um programa em RISC-V que escreve a mensagem **"Hi"** na VRAM (endereço `0x80000` e `0x80001`):

1.  Carrega o endereço base da VRAM (`0x80000`) no registrador `x1` (utilizando `lui` e `addi`).
2.  Carrega o valor ASCII de **'H'** (`0x48`) em `x2`.
3.  Armazena `x2` no endereço `x1 + 0` (`0x80000`) utilizando `sw`.
4.  Carrega o valor ASCII de **'i'** (`0x69`) em `x2`.
5.  Armazena `x2` no endereço `x1 + 1` (`0x80001`) utilizando `sw`.

### Execução

```bash
python main.py
Exemplo de Saída
A saída da simulação deve demonstrar o ciclo de execução das instruções, o uso dos registradores e, ao final, o conteúdo da VRAM (E/S Programada):

--- INICIANDO SIMULAÇÃO (20 passos) ---

[1/20] Executando instrução no PC: 0x0
PC = 00000000 | Instr = 000800B7
LUI x1 = 0x80000

[2/20] Executando instrução no PC: 0x4
PC = 00000004 | Instr = 00008093
ADDI x1 = x1 + 0 -> 524288

[3/20] Executando instrução no PC: 0x8
PC = 00000008 | Instr = 04800113
ADDI x2 = x0 + 72 -> 72

[4/20] Executando instrução no PC: 0xc
PC = 0000000C | Instr = 0020A023
[BUS] VRAM BYTE em 0x80000 = 'H'
SW MEM[0x00080000] = x72 (x2)

[5/20] Executando instrução no PC: 0x10
PC = 00000010 | Instr = 06900113
ADDI x2 = x0 + 105 -> 105

[6/20] Executando instrução no PC: 0x14
PC = 00000014 | Instr = 0020A0A3
[BUS] VRAM BYTE em 0x80001 = 'i'
SW MEM[0x00080001] = x105 (x2)

[7/20] Executando instrução no PC: 0x18
PC = 00000018 | Instr = 00000000

[8/20] Executando instrução no PC: 0x1c
PC = 0000001C | Instr = 00000000

[9/20] Executando instrução no PC: 0x20
PC = 00000020 | Instr = 00000000

[10/20] Executando instrução no PC: 0x24
PC = 00000024 | Instr = 00000000

================ VRAM DISPLAY ================
Hi
==============================================

[11/20] Executando instrução no PC: 0x28
PC = 00000028 | Instr = 00000000

[12/20] Executando instrução no PC: 0x2c
PC = 0000002C | Instr = 00000000

[13/20] Executando instrução no PC: 0x30
PC = 00000030 | Instr = 00000000

[14/20] Executando instrução no PC: 0x34
PC = 00000034 | Instr = 00000000

[15/20] Executando instrução no PC: 0x38
PC = 00000038 | Instr = 00000000

[16/20] Executando instrução no PC: 0x3c
PC = 0000003C | Instr = 00000000

[17/20] Executando instrução no PC: 0x40
PC = 00000040 | Instr = 00000000

[18/20] Executando instrução no PC: 0x44
PC = 00000044 | Instr = 00000000

[19/20] Executando instrução no PC: 0x48
PC = 00000048 | Instr = 00000000

[20/20] Executando instrução no PC: 0x4c
PC = 0000004C | Instr = 00000000

================ VRAM DISPLAY ================
Hi
==============================================
--- SIMULAÇÃO FINALIZADA ---
