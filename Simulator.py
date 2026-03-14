import sys

input_file_name, output_file_binary, output_file_decimal = sys.argv[1], sys.argv[2], sys.argv[3]
register_storage = {"00000":0, "00001":0, "00010":380, "00011":0, "00100":0, "00101":0, "00110":0, "00111":0,
"01000":0, "01001":0, "01010":0, "01011":0, "01100":0, "01101":0, "01110":0, "01111":0,
"10000":0, "10001":0, "10010":0, "10011":0, "10100":0, "10101":0, "10110":0, "10111":0,
"11000":0, "11001":0, "11010":0, "11011":0, "11100":0, "11101":0, "11110":0, "11111":0}
decimal_out, binary_out = open(output_file_decimal, "w"), open(output_file_binary, "w")
program_counter = 0

def compute_twos_complement(binary_string):
    binary_list = list(binary_string)
    for idx in range(len(binary_list)): binary_list[idx] = '1' if binary_list[idx] == '0' else '0'
    return bin(int(''.join(binary_list), 2) + 1)[2:]

def convert_to_hex(num_value): return "0x" + format(num_value, "08X")

def bin_to_int(bin_string):
    if bin_string[0] == '1': return -int(compute_twos_complement(bin_string), 2)
    else: return int(bin_string, 2)

def int_to_bin(num_value, bit_count):
    if num_value >= 0:
        bin_result = bin(num_value)[2:].zfill(bit_count)
        return bin_result
    else:
        bin_result = bin((1 << bit_count) + num_value)[2:].zfill(bit_count)
        return bin_result

r_type_commands = {"00000000000110011":"ADD", "00000001010110011":"SRL", "00000000100110011":"SLT",
"01000000000110011":"SUB", "00000001100110011":"OR", "00000001110110011":"AND"}
i_type_commands = {"0100000011":"LW", "0000010011":"ADDI", "0001100111":"JALR"}
memory_space = {addr: 0 for addr in range(65536, 65664, 4)}
operation_codes = {"0110011":"R", "0000011":"I", "0010011":"I", "1100111":"I", "1100011":"B",
"1101111":"J", "0100011":"S", "0101010":"RVRS", "0000000":"RST", "1111111":"MUL", "1100110":"HALT"}
s_type_commands = {"0000100011":"SW"}
b_type_commands = {"0001100011":"BEQ", "0011100011":"BNE", "1001100011":"BLT"}
j_type_commands = {"1101111":"JAL"}

def handle_r_type(cmd_string):
    cmd_pattern = cmd_string[0:7] + cmd_string[17:20] + cmd_string[25:32]
    cmd_name = r_type_commands.get(cmd_pattern)
    src_reg1, src_reg2, dest_reg = cmd_string[12:17], cmd_string[7:12], cmd_string[20:25]
    if dest_reg == "00000": return
    if cmd_name == "ADD": register_storage[dest_reg] = register_storage[src_reg1] + register_storage[src_reg2]
    elif cmd_name == "SUB": register_storage[dest_reg] = register_storage[src_reg1] - register_storage[src_reg2]
    elif cmd_name == "SRL":
        shift_value = bin_to_int(int_to_bin(register_storage[src_reg2], 32)[27:32])
        register_storage[dest_reg] = register_storage[src_reg1] >> shift_value
    elif cmd_name == "SLT":
        register_storage[dest_reg] = 1 if register_storage[src_reg1] < register_storage[src_reg2] else 0
    elif cmd_name == "OR" or cmd_name == "AND":
        result_bits = ["0"] * 32
        val1_bin, val2_bin = int_to_bin(register_storage[src_reg1], 32), int_to_bin(register_storage[src_reg2], 32)
        for bit_idx in range(32):
            if cmd_name == "OR" and (val1_bin[bit_idx] == "1" or val2_bin[bit_idx] == "1"):
                result_bits[bit_idx] = "1"
            elif cmd_name == "AND" and val1_bin[bit_idx] == "1" and val2_bin[bit_idx] == "1":
                result_bits[bit_idx] = "1"
        register_storage[dest_reg] = bin_to_int("".join(result_bits))

def handle_b_type(cmd_string, pc_val):
    cmd_name = b_type_commands.get(cmd_string[17:20] + cmd_string[25:32])
    reg1_val, reg2_val = register_storage.get(cmd_string[12:17]), register_storage.get(cmd_string[7:12])
    branch_offset_val = bin_to_int(cmd_string[0] + cmd_string[24] + cmd_string[1:7] + cmd_string[20:24]) * 2
    if (cmd_name == "BEQ" and reg1_val == reg2_val) or \
       (cmd_name == "BNE" and reg1_val != reg2_val) or \
       (cmd_name == "BLT" and reg1_val < reg2_val):
        return str(pc_val + branch_offset_val)
    return str(pc_val + 4)

def handle_j_type(cmd_string, pc_val):
    jump_offset = cmd_string[0] + cmd_string[12:20] + cmd_string[11] + cmd_string[1:11] + "0"
    jump_offset_val = bin_to_int(jump_offset)
    dest_reg = cmd_string[20:25]
    if dest_reg != "00000": register_storage[dest_reg] = pc_val + 4
    return pc_val + (jump_offset_val if dest_reg != "00000" else 4)

def handle_s_type(cmd_string):
    src_reg2, src_reg1 = cmd_string[7:12], cmd_string[12:17]
    store_offset_val = bin_to_int(cmd_string[0:7] + cmd_string[20:25])
    target_addr = register_storage.get(src_reg1) + store_offset_val
    memory_space[target_addr] = register_storage.get(src_reg2)

def handle_i_type(cmd_string, pc_val):
    cmd_name = i_type_commands.get(cmd_string[17:20] + cmd_string[25:32])
    src_reg, dest_reg, imm_value = cmd_string[12:17], cmd_string[20:25], cmd_string[0:12]
    imm_int = bin_to_int(imm_value)
    
    if cmd_name == "ADDI" and dest_reg != "00000":
        register_storage[dest_reg] = imm_int + register_storage.get(src_reg)
    elif cmd_name == "LW" and dest_reg != "00000":
        mem_address = register_storage.get(src_reg) + imm_int
        if mem_address not in memory_space: memory_space[mem_address] = 0
        register_storage[dest_reg] = memory_space.get(mem_address)
    elif cmd_name == "JALR":
        if dest_reg != "00000": register_storage[dest_reg] = pc_val + 4
        return register_storage.get(src_reg) + imm_int

def output_register_state():
    for val in register_storage.values():
        bin_repr, decimal_repr = " 0b" + int_to_bin(val, 32), " " + str(val)
        binary_out.write(bin_repr)
        decimal_out.write(decimal_repr)
    decimal_out.write(" \n")
    binary_out.write(" \n")

instructions = []
with open(input_file_name, "r") as source_file:
    instructions = [line.strip() for line in source_file.readlines() if line.strip()]

instr_index = 0
while instr_index < len(instructions):
    op_code = instructions[instr_index][25:32]
    instr_category = operation_codes[op_code]
    
    if instr_category == "R":
        handle_r_type(instructions[instr_index])
        instr_index += 1
        program_counter = instr_index * 4
        decimal_out.write(str(program_counter))
        binary_out.write("0b" + int_to_bin(program_counter, 32))
        output_register_state()
    
    elif instr_category == "B":
        if instructions[instr_index] == "00000000000000000000000001100011":
            program_counter = instr_index * 4
            decimal_out.write(str(program_counter))
            binary_out.write("0b" + int_to_bin(program_counter, 32))
            output_register_state()
            break
        
        branch_result = int(handle_b_type(instructions[instr_index], program_counter))
        program_counter = branch_result
        decimal_out.write(str(program_counter))
        binary_out.write("0b" + int_to_bin(program_counter, 32))
        instr_index = int(program_counter / 4)
        output_register_state()
    
    elif instr_category == "S":
        handle_s_type(instructions[instr_index])
        instr_index += 1
        program_counter = instr_index * 4
        binary_out.write("0b" + int_to_bin(program_counter, 32))
        decimal_out.write(str(program_counter))
        output_register_state()
    
    elif instr_category == "I":
        if op_code == "1100111":
            program_counter = handle_i_type(instructions[instr_index], program_counter)
            instr_index = int(program_counter // 4)
            binary_out.write("0b" + int_to_bin(program_counter, 32))
            decimal_out.write(str(program_counter))
            output_register_state()
        else:
            handle_i_type(instructions[instr_index], program_counter)
            instr_index += 1
            program_counter = instr_index * 4
            binary_out.write("0b" + int_to_bin(program_counter, 32))
            decimal_out.write(str(program_counter))
            output_register_state()
    
    elif instr_category == "MUL":
        register_storage[instructions[instr_index][20:25]] = register_storage.get(instructions[instr_index][12:17]) * register_storage.get(instructions[instr_index][7:12])
        instr_index += 1
        program_counter = instr_index * 4
        decimal_out.write(str(program_counter))
        binary_out.write("0b" + int_to_bin(program_counter, 32))
        output_register_state()
    
    elif instr_category == "HALT":
        binary_out.write("0b" + int_to_bin(program_counter, 32))
        decimal_out.write(str(program_counter))
        output_register_state()
        break
    
    elif instr_category == "J":
        program_counter = handle_j_type(instructions[instr_index], program_counter)
        instr_index = program_counter // 4
        binary_out.write("0b" + int_to_bin(program_counter, 32))
        decimal_out.write(str(program_counter))
        output_register_state()
    
    else:
        instr_index += 1
        program_counter = instr_index * 4
        break

for addr in sorted(memory_space.keys()):
    hex_addr = convert_to_hex(addr)
    formatted_bin = hex_addr + ":0b" + int_to_bin(memory_space[addr], 32)
    formatted_decimal = hex_addr + ":" + str(memory_space[addr])
    
    if addr == 65660:
        decimal_out.write(formatted_decimal)
        binary_out.write(formatted_bin)
        break
    else:
        binary_out.write(formatted_bin + "\n")
        decimal_out.write(formatted_decimal + "\n")

for i in decimal_out.readlines():
    print(i)
for i in binary_out.readlines():
    print(i)

binary_out.close()
decimal_out.close()