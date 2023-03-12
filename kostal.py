from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


# Interface class to a Kostal unit.
class Kostal:
    # Set up a unit using IP and port information as well as Interface description.
    # Try to connect to the Kostal unit specified and leave a connection open for the lifetime of the class.
    # test = True: do not try to connect to a real device
    def __init__(self, inverter_ip, inverter_port, icd, test):
        self.icd = icd
        self.inverter_ip = inverter_ip
        self.inverter_port = inverter_port

        if not test:
            # connection to Kostal unit
            self.client = ModbusTcpClient(self.inverter_ip, port=self.inverter_port)
            if not self.client.connect():
                raise ConnectionRefusedError("Connection to Kostal unit failed")

            # get unit ID
            self.unit_id = self.read_u16("MODBUSUnitID")
        else:
            self.client = None
            self.unit_id = 71

    # Shut down connection to the Kostal unit.
    def __del__(self):
        if self.client is not None:
            self.client.close()

    # Reads a register identified by the given key.
    # The key is the case-sensitive collation of the string in column "Description" of the interface description.
    # Only letters (upper and lower case) and numbers are kept, all other characters are discarded (including spaces).
    def read_register(self, an_key):
        register = self.icd.registers.get(an_key)
        if register is None:
            raise LookupError(f"Invalid key: {an_key}")

        match register.format:
            case "Bool":
                return self.read_bool(register.decaddress)
            case "U16":
                return self.read_u16(register.decaddress)
            case "S16":
                return self.read_s16(register.decaddress)
            case "U32":
                return self.read_u32(register.decaddress)
            case "Float":
                return self.read_float(register.decaddress)
            case "String":
                return self.read_string(register.decaddress, register.n)
            case "_":
                raise RuntimeError(f"Format {register.format} not supported.")

    # Helper functions to read various types.
    # Function to read a bool
    def read_bool(self, adr_dec):
        return self.read_u16(adr_dec)

    # Function to read an uint16
    def read_u16(self, adr_dec):
        r1 = self.client.read_holding_registers(adr_dec, 1, slave=self.unit_id)
        u16_register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_u16_register = u16_register.decode_16bit_uint()
        return result_u16_register

    # Function to read a (signed) int16
    def read_s16(self, adr_dec):
        r1 = self.client.read_holding_registers(adr_dec, 1, slave=self.unit_id)
        s16_register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_s16_register = s16_register.decode_16bit_int()
        return result_s16_register

    # Function to read an uint32
    def read_u32(self, adr_dec):
        r1 = self.client.read_holding_registers(adr_dec, 2, slave=self.unit_id)
        u32_register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_u32_register = u32_register.decode_32bit_uint()
        return result_u32_register

    # Function to read a float
    def read_float(self, adr_dec):
        r1 = self.client.read_holding_registers(adr_dec, 2, slave=self.unit_id)
        float_register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_float_register = round(float_register.decode_32bit_float(), n)
        return result_float_register

    # Function to read an n-register string
    def read_string(self, adr_dec, characters):
        r1 = self.client.read_holding_registers(adr_dec, characters, slave=self.unit_id)
        string_register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_string_register = string_register.decode_string(size=characters)
        return result_string_register
