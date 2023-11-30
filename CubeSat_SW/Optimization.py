import subprocess
import time
import Color_schema


def dependencies():
    python_packages = ["smbus2", "adafruit-circuitpython-ina219"]

    try:
        subprocess.run(['python3', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['pip3', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'i2c-tools'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}System dependencies are already installed!{Color_schema.Colors.RESET}")
        print("\n")
        return True
    
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True, stderr=subprocess.DEVNULL)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'python3', 'python3-pip', 'i2c-tools'], check=True, stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}System dependencies - Installed{Color_schema.Colors.RESET}")
            print("\n")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error installing system dependencies: {e.returncode}{Color_schema.Colors.RESET}")
            print("\n")
            return False

    try:
        subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_i2c', '0'], check=True, stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}I2C is already activated!{Color_schema.Colors.RESET}")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_i2c', '0'], check=True)
            print(f"{Color_schema.Colors.GREEN}I2C - Activated{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error activating I2C: {e.returncode}{Color_schema.Colors.RESET}")
            return False

    try:
        subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_spi', '0'], check=True, stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}SPI is already activated!{Color_schema.Colors.RESET}")
        print("\n")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_spi', '0'], check=True, stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}SPI - Activated{Color_schema.Colors.RESET}")
            print("\n")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error activating SPI: {e.returncode}{Color_schema.Colors.RESET}")
            print("\n")
            return False

    for package in python_packages:
        try:
            subprocess.run(["pip3", "install", "--upgrade", "-q", package], check=True, stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}Package {package} - Installed{Color_schema.Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error installing package {package}: {e.returncode}{Color_schema.Colors.RESET}")
            return False
    
    print("\n")
    return True

def disable_wifi():
    try:
        subprocess.check_output(['sudo', 'ifconfig', 'wlan0', 'down'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}Wi-Fi service is already deactivated!{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'ifconfig', 'wlan0', 'down'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}WiFi - Deactivated!{Color_schema.Colors.RESET}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error trying to disable Wi-Fi service: {e.returncode} {Color_schema.Colors.RESET}")
            return False

def disable_gui():
    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-active', '--quiet', 'lightdm'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}GUI service is already deactivated!{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'stop', 'lightdm'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN} GUI - Deactivated{Color_schema.Colors.RESET}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error trying to disable GUI service: {e.returncode}{Color_schema.Colors.RESET}")
            return False
    
def disable_bluetooth():
    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-enabled', '--quiet', 'bluetooth.service'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}Bluetooth service is already deactivated!{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'disable', 'bluetooth.service'], stderr=subprocess.DEVNULL)
            print(f"{Color_schema.Colors.GREEN}Bluetooth - Deactivated{Color_schema.Colors.RESET}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error trying to deactivate Bluetooth service: {e.returncode}{Color_schema.Colors.RESET}")
            return False

def disable_updates():
    try:
        subprocess.run(["sudo", "systemctl", "is-active", "--quiet", "apt-daily.timer"], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.ORANGE}Automatic updates service is already deactivated!{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError:
        print("automatic updates service - Deactivated", end='', flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "disable", "apt-daily.timer"], stderr=subprocess.DEVNULL)
            print(".", end='', flush=True)
            subprocess.run(["sudo", "systemctl", "disable", "apt-daily-upgrade.timer"], stderr=subprocess.DEVNULL)
            print(".", end='', flush=True)
            subprocess.run(["sudo", "systemctl", "stop", "apt-daily.service"], stderr=subprocess.DEVNULL)
            print(".", end='', flush=True)
            subprocess.run(["sudo", "systemctl", "stop", "apt-daily-upgrade.service"], stderr=subprocess.DEVNULL)
            print(f"\n{Color_schema.Colors.GREEN}Automatic updates have been successfully disabled!{Color_schema.Colors.RESET}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n{Color_schema.Colors.RED}Error while disabling automatic updates: {e.returncode}{Color_schema.Colors.RESET}")
            return False
print("\n")

def optimization_start():
    try:
        if not dependencies():
            return
        if not disable_wifi():
            return
        if not disable_gui():
            return
        if not disable_bluetooth():
            return
        if not disable_updates()
            return
        print(f"{Color_schema.Colors.GREEN}Operations completed successfully. Rebooting OnBoard Computer in 10 seconds!{Color_schema.Colors.RESET}")
        time.sleep(10)
        subprocess.run(["sudo", "reboot"], check=True)
    except subprocess.CalledProcessError as e:
            print(f"{Color_schema.Colors.RED}Error restarting OnBoard Computer: {e}{Color_schema.Colors.GREEN}")
    except Exception as e:
        print(f"{Color_schema.Colors.RED}Aborted! An error occurred: {e}{Color_schema.Colors.RESET}")
