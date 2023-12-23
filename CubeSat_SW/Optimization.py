import subprocess
import time
import os
import Color_schema

def handle_errors(print_messages=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except subprocess.CalledProcessError as e:
                return False
        return wrapper
    return decorator

@handle_errors(print_messages=False)
def DEPENDECIES():
    
    system_dependencies = ["python3", "python3-pip", "i2c-tools"]

    os.system('clear')
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL )
        subprocess.run(['sudo', 'apt-get', 'install', '-y'] + system_dependencies, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL )
        print(f"{Color_schema.Colors.GREEN}System Dependencies - Installed{Color_schema.Colors.RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error installing system dependencies: {e.returncode}{Color_schema.Colors.RESET}\n")
        return False
    
@handle_errors(print_messages=False)
def COMM_PROTOCOLS():
    try:
        subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_i2c', '0'], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_spi', '0'], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}COMMUNICATION PROTOCOLS - Enabled{Color_schema.Colors.RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error activating Communication Protocols: {e.returncode}{Color_schema.Colors.RESET}\n")
        return False
    
@handle_errors(print_messages=False)
def PACKAGES():
    try:
        subprocess.run(["sudo", "apt", "install", "-y", "python3-smbus2"], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Packages - Installed{Color_schema.Colors.RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error installing packages: {e.returncode}{Color_schema.Colors.RESET}\n")
        return False

@handle_errors(print_messages=False)
def DISABLE_WIFI():
    try:
        subprocess.check_call(['sudo', 'ip', 'link', 'set', 'wlan0', 'down'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Wi-Fi Service - Deactivated!{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error trying to disable Wi-Fi service: {e.returncode}{Color_schema.Colors.RESET}")
        return False

@handle_errors(print_messages=False)
def DISABLE_GUI():
    try:
        subprocess.run(['sudo', 'systemctl', 'isolate', 'multi-user.target', '&&', 'sudo', 'chvt', '1'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}GUI Service - Deactivated{Color_schema.Colors.RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error trying to disable GUI service: {e.returncode} - {e.stderr.decode().strip()}{Color_schema.Colors.RESET}\n")
        return False

@handle_errors(print_messages=False)
def DISABLE_BLUETOOTH():
    try:
        subprocess.check_call(['sudo', 'systemctl', 'disable', 'bluetooth.service'], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Bluetooth Service - Deactivated{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error trying to disable Bluetooth service: {e.returncode} - {e.stderr.decode().strip()}{Color_schema.Colors.RESET}")
        return False
    
@handle_errors(print_messages=False)
def DISABLE_UPDATES():
    try:
        subprocess.run(["sudo", "systemctl", "disable", "apt-daily.timer"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "systemctl", "disable", "apt-daily-upgrade.timer"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "systemctl", "stop", "apt-daily.service"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "systemctl", "stop", "apt-daily-upgrade.service"], stderr=subprocess.DEVNULL)
        print(f"{Color_schema.Colors.GREEN}Automatic Updates Service - Deactivated{Color_schema.Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Color_schema.Colors.RED}Error while disabling automatic updates: {e.returncode} - {e.stderr.decode().strip()}{Color_schema.Colors.RESET}")
        return False
        
def optimization_start():
    if all([
        DEPENDECIES(),
        COMM_PROTOCOLS(),
        PACKAGES(),
        DISABLE_WIFI(),
        DISABLE_UPDATES(),
        DISABLE_BLUETOOTH(),
        DISABLE_GUI(),
    ]):
        print(f"{Color_schema.Colors.GREEN}All system configuration have been applied!{Color_schema.Colors.RESET}")
        print(f"{Color_schema.Colors.RED}OnBoard Computer will restart in 10 seconds!{Color_schema.Colors.RESET}")
        time.sleep(10)
        subprocess.run(['sudo', 'reboot'], check=True)
    else:
        print(f"{Color_schema.Colors.RED}Error trying to reboot OnBoard Computer!{Color_schema.Colors.RESET}")
        
