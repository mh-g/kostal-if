import re


# Contains the information for a single register.
# "values" is an optional dictionary of possible return values.
class Register:
    # Split up the input line and put it into a well-defined class structure.
    def __init__(self, line):
        parts = re.split("\s", line)
        self.hex_address = parts[0]
        self.dec_address = parts[1]
        number_of_parts = len(parts)
        self.freetext = " ".join(parts[2:number_of_parts - 6])
        regex = re.compile('[^a-zA-Z0-9]')
        self.index = regex.sub('', "".join(parts[2:number_of_parts - 6]))
        self.unit = parts[number_of_parts - 6]
        self.format = parts[number_of_parts - 5]
        self.n = parts[number_of_parts - 4]
        self.access = parts[number_of_parts - 3]
        self.code = parts[number_of_parts - 2]
        self.values = {}

    # Add footnote lines, often giving result types. Must be manually interleaved into the original ASCII input file.
    def add_value(self, line):
        if (line[0] >= '0') and (line[0] <= '9'):
            index, value = re.split(" ", line, 1)
            self.values[index] = value

    def __str__(self):
        return "addr:" + self.hex_address + "(" + self.dec_address + ")" \
            + " unit=" + self.unit \
            + " format=" + self.format \
            + " bytes=" + self.n \
            + " access=" + self.access \
            + " code=" + self.code \
            + " desc=" + self.freetext \
            + " values=" + ";".join (self.values)


# Contains the information of the complete MODBUS register table.
# Reads table from section 3.2 of BA_KOSTAL_Interface_description_MODBUS_TCP_SunSpec_Hybrid.pdf, rev. 2.0, 2021-06-16,
# after it has been copied into plain ASCII and stripped of its header.
# Footnotes may be included after the referenced line by prepending four whitespace at the beginning of the line.
# https://www.kostal-solar-electric.com/de-de/download/download/-/media/document-library-folder---kse/2020/12/15/13/38/ba_kostal-interface-description-modbus-tcp_sunspec_hybrid.pdf
class ICD:
    r = None

    def __init__(self, filename):
        self.registers = {}
        with open(filename) as f:
            for line in f:
                self.parseline(line)

    def parseline(self, line):
        if line[1] == ' ':
            self.r.add_value(line[4:])
        else:
            self.r = Register(line)
            self.registers[self.r.index] = self.r

    def get_register(self, key):
        return self.registers[key]