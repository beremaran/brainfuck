import sys

BRAINFUCK_INSTRUCTIONS = {
    '<', '>', '+', '-', '.', ',', '[', ']'
}

if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding='utf8') as f:
        instructions = f.read()
        
    instruction_pointer = 0
    instructions = ''.join([x for x in instructions if x in BRAINFUCK_INSTRUCTIONS])
    
    data_pointer = 0
    data_buffer = [0] * 16777216
    
    loop_indices = {}
    loop_stack = []
    for i, instruction in enumerate(instructions):
        if instruction not in {'[', ']'}:
            continue
        
        if instruction == '[':
            loop_stack.append(i)
        if instruction == ']':
            if len(loop_stack) == 0:
                raise IndexError(f'no matching loop end at: {i}')
            loop_indices[loop_stack.pop()] = i
            
    for loop_start, loop_end in loop_indices.copy().items():
        loop_indices[loop_end] = loop_start
            
    loop_stack.clear()
    
    try:
        while instruction_pointer < len(instructions):        
            instruction = instructions[instruction_pointer]
            
            jump_to = None
            match instruction:
                case '>':
                    data_pointer += 1
                case '<':
                    data_pointer -= 1
                case '+':
                    data_buffer[data_pointer] += 1
                case '-':
                    data_buffer[data_pointer] -= 1
                case '.':
                    print(chr(data_buffer[data_pointer]), sep='', end='')
                case ',':
                    new_char = sys.stdin.read(1)
                    if len(new_char) == 0:
                        exit(0)
                        
                    data_buffer[data_pointer] = ord(new_char)
                case '[':
                    loop_stack.append(instruction_pointer)
                    if data_buffer[data_pointer] == 0:
                        jump_to = loop_indices[loop_stack.pop()] + 1
                case ']':
                    if data_buffer[data_pointer] != 0:
                        jump_to = loop_indices[instruction_pointer] + 1
                    else:
                        loop_stack.pop()
                        
            if jump_to:
                instruction_pointer = jump_to
            else:
                instruction_pointer += 1
    except (IndexError, KeyError, TypeError) as e:
        print(f'data_pointer: {data_pointer} data: {data_buffer[data_pointer]}')
        print(f'instruction_pointer: {instruction_pointer} instruction: {instructions[instruction_pointer]}')
        raise e from e
        
