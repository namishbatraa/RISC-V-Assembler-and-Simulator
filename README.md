# RISC-V Assembler and Simulator

This project implements a **RISC-V Assembler and Simulator in Python**.  
The assembler converts RISC-V assembly instructions into **32-bit binary machine code**, and the simulator executes the generated instructions while tracking **register states, memory, and program counter updates**.

---

## Overview

The project is divided into two main components:

1. **Assembler**
   - Parses RISC-V assembly instructions.
   - Converts them into 32-bit binary machine instructions.
   - Performs syntax and operand validation.

2. **Simulator**
   - Executes the generated binary instructions.
   - Simulates register operations, memory access, and control flow.
   - Outputs register states and memory contents.

---

## Features

### Assembler
- Converts RISC-V assembly code to binary machine code
- Supports multiple instruction formats
- Handles labels and branching
- Validates registers and immediate values
- Reports syntax and semantic errors

### Simulator
- Simulates execution of machine instructions
- Maintains a register file with 32 registers
- Tracks the program counter (PC)
- Simulates memory operations
- Outputs register values in both **binary and decimal formats**

---

## Supported Instruction Formats

### R-Type
- ADD  
- SUB  
- SRL  
- SLT  
- OR  
- AND  

### I-Type
- ADDI  
- LW  
- JALR  

### S-Type
- SW  

### B-Type
- BEQ  
- BNE  
- BLT  

### J-Type
- JAL  

---

## Project Structure

```
RISC-V-Assembler-Simulator
│
├── Assembler.py        # Converts assembly instructions to binary
├── Simulator.py        # Executes binary instructions
├── data.json           # Instruction formats, opcodes, register mappings
├── input.txt           # Assembly program input
├── output.txt          # Generated machine code
```

---

## How to Run

### 1. Run the Assembler

Convert assembly instructions to binary machine code.

```
python Assembler.py input.txt output.txt
```

Example:

```
python Assembler.py program.asm output.txt
```

This generates the binary instructions in **output.txt**.

---

### 2. Run the Simulator

Execute the generated binary instructions.

```
python Simulator.py output.txt binary_output.txt decimal_output.txt
```

Outputs:

- **binary_output.txt** → Register values in binary
- **decimal_output.txt** → Register values in decimal

---

## Example Assembly Program

```
addi x1, x0, 5
addi x2, x0, 10
add x3, x1, x2
```

Workflow:

1. Assemble the program
```
python Assembler.py input.txt output.txt
```

2. Run the simulator
```
python Simulator.py output.txt binary.txt decimal.txt
```

3. View register states and memory updates.

---

## Error Handling

The assembler detects and reports errors such as:

- Invalid register names
- Incorrect number of operands
- Invalid immediate values
- Immediate values outside valid range
- Undefined labels

---

## Technologies Used

- Python
- RISC-V Instruction Set Architecture
- Binary encoding and decoding
- Computer Architecture concepts

---

## Learning Objectives

This project demonstrates:

- Implementation of a **RISC-V assembler**
- Simulation of **CPU instruction execution**
- Understanding of **instruction formats and encoding**
- Handling **control flow, registers, and memory**

---

## Author

Namish Batra
