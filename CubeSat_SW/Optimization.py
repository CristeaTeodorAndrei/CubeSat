import subprocess
import time
import os
import Color_schema


def dependencies():
    
    python_packages = ["smbus2", "adafruit-circuitpython-ina219"]
    system_dependencies = ["python3", "python3-pip", "i2c-tools"]

    os.system('clear')
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.run(['sudo', 'apt-get', 'install', '-y'] + system_dependencies, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}System dependencies - Installed{Color_schema.Colors.RESET}")
        print("\n")
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error installing system dependencies: {e.returncode}{Color_schema.Colors.RESET}")
        print("\n")


    try:
        subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_i2c', '0'], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}I2C - Activated{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error activating I2C: {e.returncode}{Color_schema.Colors.RESET}")
    try:
        subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_spi', '0'], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}SPI - Activated{Color_schema.Colors.RESET}")
        print("\n")
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error activating SPI: {e.returncode}{Color_schema.Colors.RESET}")
        print("\n")


    for package in python_packages:
        try:
            subprocess.run(["pip3", "install", "--upgrade", "-q", package], check=True, stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}Package {package} - Installed{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error installing package {package}: {e.returncode}{Color_schema.Colors.RESET}")
    
    print("\n")

def disable_wifi():
    try:
        subprocess.check_call(['sudo', 'ip', 'link', 'set', 'wlan0', 'down'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Wi-Fi Service - Deactivated!{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error trying to disable Wi-Fi service: {e.returncode}{Color_schema.Colors.RESET}")
    
def disable_gui():
    try:
        print(f"{Color_schema.Colors.GREEN}GUI Service - Deactivated{Color_schema.Colors.RESET}")
        print("\n\n")
        print(f"{Color_schema.Colors.GREEN}All system configurations have been updated!{Color_schema.Colors.RESET}")
        print(f"{Color_schema.Colors.RED}OnBoard Computer will restart in 10 seconds!{Color_schema.Colors.RESET}") 
        time.sleep(10)
        subprocess.run(['sudo', 'systemctl', 'isolate', 'multi-user.target', '&&', 'sudo', 'chvt', '1'], stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', 'reboot'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error trying to disable GUI service: {e.returncode} - {e.stderr.decode().strip()}{Color_schema.Colors.RESET}")

def disable_bluetooth():
    try:
        subprocess.check_call(['sudo', 'systemctl', 'disable', 'bluetooth.service'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Bluetooth Service - Deactivated{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error trying to disable Bluetooth service: {e.returncode} - {e.stderr.decode().strip()}{Color_schema.Colors.RESET}")

def disable_updates():
    try:
        subprocess.run(["sudo", "systemctl", "disable", "apt-daily.timer"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "systemctl", "disable", "apt-daily-upgrade.timer"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "systemctl", "stop", "apt-daily.service"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "systemctl", "stop", "apt-daily-upgrade.service"], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Automatic Updates Service - Deactivated{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error while disabling automatic updates: {e.returncode} - {e.stderr.decode().strip()}{Color_schema.Colors.RESET}")

def optimization_start():
    dependencies()
    disable_wifi()
    disable_updates()
    disable_bluetooth()
    disable_gui()
