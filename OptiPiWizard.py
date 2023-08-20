import subprocess

def disable_wifi():
    subprocess.run(["sudo", "ifconfig", "wlan0", "down"])

def disable_gui():
    subprocess.run(["sudo", "systemctl", "set-default", "multi-user.target"])
    subprocess.run(["sudo", "systemctl", "disable", "lightdm.service"])

def disable_bluetooth():
    subprocess.run(["sudo", "systemctl", "disable", "bluetooth.service"])
    subprocess.run(["sudo", "systemctl", "disable", "hciuart.service"])

def disable_updates():
    subprocess.run(["sudo", "systemctl", "disable", "apt-daily.timer"])
    subprocess.run(["sudo", "systemctl", "disable", "apt-daily-upgrade.timer"])
    subprocess.run(["sudo", "systemctl", "stop", "apt-daily.service"])
    subprocess.run(["sudo", "systemctl", "stop", "apt-daily-upgrade.service"])