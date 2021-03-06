DEST_DICT = {'': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110',
             'AMD': '111'}
COMP_DICT = {'0': '110101010', '1': '110111111', '-1': '110111010', 'D': '110001100', 'A': '110110000',
             '!D': '110001101', '!A': '110110001', '-D': '110001111', '-A': '110110011', 'D+1': '110011111',
             'A+1': '110110111', 'D-1': '110001110', 'A-1': '110110010', 'D+A': '110000010',
             'D-A': '110010011',
             'A-D': '110000111', 'D&A': '110000000', 'D|A': '110010101', 'M': '111110000', '!M': '111110001',
             '-M': '111110011', 'M+1': '111110111', 'M-1': '111110010', 'D+M': '111000010',
             'D-M': '111010011',
             'M-D': '111000111', 'D&M': '111000000', 'D|M': '111010101', 'D<<': '010110000',
             'A<<': '010100000',
             'M<<': '011100000', 'D>>': '010010000', 'A>>': '010000000', 'M>>': '011000000'}
JMP_DICT = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110',
            'JMP': '111'}


class CodeTranslator:
    """
    Represents an object that can translate ASMCode objects into binary HACK machine code.
    """

    def __init__(self, parsed_asm_code):
        """
        Create a translator object that can translate a specific ASMCode object into HACK machine language.
        :param parsed_asm_code: An ASMCode object.
        """
        self.__asm_code = parsed_asm_code

    def translate(self):
        """
        Translate the asm code into HACK machine code.
        :return: A 16-bit byte array representing machine code for HACK.
        """
        lst = []
        for line in self.__asm_code.get_asm_code():
            if line[0] == '@':
                instruction = self.__parse_a_instruction(line)
            else:
                instruction = self.__parse_c_instruction(line)
            lst.append(instruction)
        return lst

    def __parse_a_instruction(self, instruction):
        address = instruction[1:]

        if address.isnumeric():
            address = bin(int(address))[2:]
        else:
            address = self.__asm_code.get_symbol_value(address)
            address = bin(int(address))[2:]
        return address.zfill(16)

    def __parse_c_instruction(self, instruction):
        split_index = instruction.find(';')
        jump = ''
        comp = instruction
        if split_index >= 0:
            comp = instruction[:split_index]
            jump = instruction[split_index + 1:]

        split_index = comp.find('=')
        dest = ""
        if split_index >= 0:
            dest = comp[:split_index]
            comp_cmd = comp[split_index + 1:]
        else:
            comp_cmd = comp

        dest = DEST_DICT[dest]
        comp_cmd = COMP_DICT[comp_cmd]

        jump = JMP_DICT[jump]

        instruction_bits = '1' + comp_cmd + dest + jump

        return instruction_bits
