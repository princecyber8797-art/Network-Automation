import os
import yaml

from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()


def load_inventory():
    with open("inventory/devices.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    inventory = load_inventory()

    username = os.getenv("NETWORK_USERNAME")
    password = os.getenv("NETWORK_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "NETWORK_USERNAME and NETWORK_PASSWORD must be set in .env"
        )

    for device in inventory["devices"]:
        connection_params = {
            "device_type": device["device_type"],
            "host": device["host"],
            "username": username,
            "password": password,
        }

        print(f"\nConnecting to {device['name']} ({device['host']})...")

        try:
            connection = ConnectHandler(**connection_params)

            output = connection.send_command("show version")

            print("=" * 70)
            print(output)
            print("=" * 70)

            connection.disconnect()

            print(f"SUCCESS: {device['name']}")

        except Exception as error:
            print(f"FAILED: {device['name']}")
            print(f"ERROR: {error}")


if __name__ == "__main__":
    main()
