from kostal import Kostal
from table_parser import ICD

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    table = ICD("registers.txt")
    device = Kostal("192.168.178.90", 1502, 71, table)

    # exemplary cases:
    # 0x02 MODBUSEnable Bool 1
#    print(device.read_register("MODBUSEnable"))
    # 0x04 MODBUSUnitID U16 1
#    print(device.read_register("MODBUSUnitID"))
    # 0x23F InverterGenerationPoweractual S16 1
#    print(device.read_register("InverterGenerationPoweractual"))
    # 0x68 Stateofenergymanager U32 2
#    print(device.read_register("Stateofenergymanager"))
    # 0x62 TemperatureofcontrollerPCB Float 2
#    print(device.read_register("TemperatureofcontrollerPCB"))
    # 0x06 Inverterarticlenumber String 8
#    print(device.read_register("Inverterarticlenumber"))
    # 0x217 InverterManufacturer String 16
#    print(device.read_register("InverterManufacturer"))
    # 0x180 Inverternetworkname String 32
#    print(device.read_register("Inverternetworkname"))

    # questionable cases:
    # 0x24, 0x36, 0x38: U16 but N=2
    # 0xC2, 0xCA, 0xD0: Float but discrete values

# loop over all
    for key, value in table.registers.items():
        print (f'{key}: {device.read_register(key)}')
