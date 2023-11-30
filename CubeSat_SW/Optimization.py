import subprocess
import time
import Color_schema


def dependencies():
    python_packages = ["smbus2", "Adafruit-INA219"]

    try:
        subprocess.run(["./bash/protocols.sh"], check=True, shell=True, stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}I2C/SPI communication protocols and system dependencies have been activated!{Color_schema.Colors.RESET}") 
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error installing system dependencies: {e}{Color_schema.Colors.RESET}")

    for package in python_packages:
        try:
            subprocess.run(["pip3", "install", "--upgrade", package], check=True, stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}Package {package} installed successfully.{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error installing package {package}: {e}{Color_schema.Colors.RESET}")
    
def disable_wifi():
    try:
        subprocess.check_output(['sudo', 'ifconfig', 'wlan0', 'down'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN} Wi-Fi service is already deactivated!{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'ifconfig', 'wlan0', 'down'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Color_schema.ORANGE} Deactivating Wi-Fi service!{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error trying to disable Wi-Fi service: {e} {Color_schema.Colors.RESET}")
    
def disable_gui():
    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-active', '--quiet', 'lightdm'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}GUI service is already deactivated!{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'stop', 'lightdm'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.ORANGE}Deactivating GUI service!{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error trying to disable GUI service: {e}{Color_schema.Colors.RESET}")
    
def disable_bluetooth():
    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-enabled', '--quiet', 'bluetooth.service'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN} Bluetooth service is already deactivated!{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'disable', 'bluetooth.service'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.ORANGE} Deactivating Bluetooth service!{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED} Error trying to deactivate Bluetooth service: {e}{Color_schema.Colors.RESET}")

    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-enabled', '--quiet', 'hciuart.service'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}HCIUART service is already deactivated!{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'disable', 'hciuart.service'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}Deactivating HCIUART service!{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.GREEN}Error trying to deactivate HCIUART service: {e}{Color_schema.Colors.RESET}")
            
def disable_updates():
    try:
        subprocess.run(["sudo", "systemctl", "is-active", "--quiet", "apt-daily.timer"], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Automatic updates service is already deactivated.{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError:
        print("Deactivating automatic updates service", end='', flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "disable", "apt-daily.timer"], stderr=subprocess.DEVNULL)
            print(".", end='', flush=True)
            subprocess.run(["sudo", "systemctl", "disable", "apt-daily-upgrade.timer"], stderr=subprocess.DEVNULL)
            print(".", end='', flush=True)
            subprocess.run(["sudo", "systemctl", "stop", "apt-daily.service"], stderr=subprocess.DEVNULL)
            print(".", end='', flush=True)
            subprocess.run(["sudo", "systemctl", "stop", "apt-daily-upgrade.service"], stderr=subprocess.DEVNULL)
            print(f"\n{Color_schema.Colors.ORANGE}Automatic updates have been successfully disabled.{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"\n{Color_schema.Colors.RED}Error while disabling automatic updates: {e}{Color_schema.Colors.RESET}")

# def reboot():
#     print(f"{Color_schema.Colors.GREEN} Rebooting OnBoard Computer in 3 seconds!")
#     time.sleep(3)
#     try:
#         subprocess.run(["sudo", "reboot"], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error restarting OnBoard Computer: {e}")       