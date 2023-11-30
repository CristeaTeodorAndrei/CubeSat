import subprocess

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
def install_smbus2():
    try:
        
    subprocess.check_call('')
    
def disable_wifi():
    try:
        subprocess.check_output(['sudo', 'ifconfig', 'wlan0', 'down'])
        print("Wi-Fi is already deactivated!")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'ifconfig', 'wlan0', 'down'])
            print("Deactivating Wi-Fi module!")
        except subprocess.CalledProcessError as e:
            print(f"Error trying to disable Wi-Fi module: {e}")
    
def disable_gui():
    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-active', '--quiet', 'lightdm'])
        print("GUI is already disabled!")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'stop', 'lightdm'])
            print("GUI has been disabled!")
        except subprocess.CalledProcessError as e:
            print(f"Error trying to disable GUI: {e}")

    
def disable_bluetooth():
    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-enabled', '--quiet', 'bluetooth.service'])
        print("Bluetooth is already disabled!")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'disable', 'bluetooth.service'])
            print("Deactivating Bluetooth module!")
        except subprocess.CalledProcessError as e:
            print(f"Error trying to deactivate Bluetooth module: {e}")

    try:
        subprocess.check_output(['sudo', 'systemctl', 'is-enabled', '--quiet', 'hciuart.service'])
        print("HCIUART already deactivated!")
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(['sudo', 'systemctl', 'disable', 'hciuart.service'])
            print("Deactivating HCIUART service!")
        except subprocess.CalledProcessError as e:
            print(f"Error trying to deactivate HCIUART service: {e}")
            
def disable_updates():
    subprocess.run(["sudo", "systemctl", "disable", "apt-daily.timer"])
    subprocess.run(["sudo", "systemctl", "disable", "apt-daily-upgrade.timer"])
    subprocess.run(["sudo", "systemctl", "stop", "apt-daily.service"])
    subprocess.run(["sudo", "systemctl", "stop", "apt-daily-upgrade.service"])
    print("Updates have been disabled!")
