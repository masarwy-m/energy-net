from energy_net.entities.device import Device


def main():
    print("In main method")
    device = Device(0.3)
    print(device.efficiency)

if __name__ == "__main__":
    main()