import sys

def read_file(filepath):
    '''
    Opens and reads the file at the given filepath
    '''
    with open(FILEPATH, "r") as f:
        lines = f.readlines()
    lines = [i.strip() for i in lines]
    return lines

def remove_comments(lines: list[str]) -> list[str]:
    '''
    Removes the comments by splitting on //
    '''
    lines = [i.split("//")[0] for i in lines]
    lines = [i for i in lines if i!=""]
    return lines


def get_symbols(lines: list[str]):
    '''
    Gets the symbols from the lines
    '''
    symbols = {"R0": 0, "R1": 1, "R2": 2, "R3": 3,
               "R4": 4, "R5": 5, "R6": 6, "R7": 7,
               "R8": 8, "R9": 9, "R10": 10, "R11": 11,
               "R12": 12, "R13": 13, "R14": 14, "R15": 15,
               "SCREEN": 16384, "KBD": 24576,
               "SP": 0, "LCL": 1, "ARG": 2,
               "THIS": 3, "THAT": 4}
    
    jump_locations = {}
    free_locations = {}
    free = 16
    for i, line in enumerate(lines):
        if line[0]=="(":
            j = 1
            
            while line[j] != ")":
                j += 1
            
            name = line[1:j]
            target = i - len(jump_locations)
            jump_locations[name] = target
            
        elif line[0] == "@" and not line[1:].isdigit():
            name = line[1:]
            if name not in free_locations and name not in symbols:
                free_locations[free] = name
                free += 1
    for _, name in free_locations.items():
        if name in jump_locations.keys():
            symbols[name] = jump_locations[name]
            
    
    occupied = [val for key, val in free_locations.items()if val not in symbols]
    sixteen_and_up = [i for i in range(16, 10000)]
    correct = [(num, name) for name, num in zip(occupied, sixteen_and_up) ]
    for (num, name) in correct:
        if name not in symbols:
            symbols[name] = num

    return symbols


def get_comp(line: str) -> str:
    '''
    Gets the computation bits from the instruction
    '''
    comp_dict = {"0": "101010", "1": "111111", "-1": "111010",
                 "D": "001100", "A": "110000", "M": "110000",
                 "!D": "001101", "!A": "110001", "!M": "110001",
                 "-D": "001111", "-A": "110011", "-M": "110011",
                 "D+1": "011111", "A+1": "110111", "M+1": "110111",
                 "D-1": "001110", "A-1": "110010", "M-1": "110010",
                 "D+A": "000010", "D+M": "000010", "D-A": "010011",
                 "D-M": "010011", "A-D": "000111", "M-D": "000111",
                 "D&A": "000000", "D&M": "000000",
                  "D|A": "010101", "D|M": "010101" }
    if "=" in line:
        line = line.split("=")[1]
    else:
        line = line.split(";")[0]
    comp = ""
    if "M" in line:
        comp += "1"
    else:
        comp += "0"
    comp += comp_dict[line]
    return comp
   
def get_dest(line:str) -> str:
    '''
    Gets the destination bits from the instruction
    '''
    dest_dict = {"M": "001", "D": "010", "MD": "011",
                 "A": "100", "AM": "101",
                 "AD": "110", "AMD": "111"}
    if ";" in line:
        return "000"
    dest = line.split("=")[0]
    return dest_dict[dest]
    
def get_jump(line:str) -> str:
    '''
    Gets the jump bits from the instruction
    '''
    jump_dict = {"": "000", "JGT": "001",
                    "JEQ": "010", "JGE": "011",
                    "JLT": "100", "JNE": "101",
                    "JLE": "110", "JMP": "111"}
    if "=" in line:
        return jump_dict[""]
    jump = line.split(";")[1]
    return jump_dict[jump]

def is_address(line:str) -> bool:
    '''
    Determines if the instruction is an adress instruction adn returns a boolean
    '''
    if line == "":
        return False
    return line[0] == "@"

def convert_int_to_15_bit_address(num:int) -> str:
    '''
    Converts the given integer num to a 15 bit binary number (our address) and returns it as a string
    '''
    to_return = str(bin(num))[2:]
    while len(to_return) < 15:
        to_return = "0" + to_return
    return to_return

def assembler(filepath):
    ''''
    Converts the given xxx.asm file at the filepath given and saves it to a 
    xxx.hack file
    '''
    
    HACK_FILEPATH = filepath[:-3]
    lines = read_file(FILEPATH)
    lines = remove_comments(lines)

    translation= []
    symbols = get_symbols(lines)
    # remove the jump location
    lines = [line for line in lines if line[0] != "("]

    for line in lines:
        
        if line == "" or line[:2]=="//":
            continue
        translated = ""
        if is_address(line):
            translated += "0"
            if line[1:].isdigit():
                num = int(line[1:])
                translated += convert_int_to_15_bit_address(num)
            else:
                name = line[1:]
                num = int(symbols[name])
                translated += convert_int_to_15_bit_address(num)
        else:
            translated += "111"
            translated += get_comp(line)
            translated += get_dest(line)
            translated += get_jump(line)

        translation.append(translated)
        
    # uncomment if you want to see the output per line
    # for i, t in enumerate(translation):
    #    print(i, t)

    with open(f"{HACK_FILEPATH}hack", 'w') as f:
        for line in translation:
            f.write(f"{line}\n")

if __name__ == "__main__":
    
    FILEPATH = sys.argv[1]
    print(FILEPATH)
    assembler(FILEPATH)
    print(f"Converted {FILEPATH} to hack file.")