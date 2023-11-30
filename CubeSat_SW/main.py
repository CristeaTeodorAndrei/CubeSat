import Optimization

def main():
    Optimization.dependencies()
    Optimization.disable_bluetooth()
    Optimization.disable_gui()
    Optimization.disable_updates()
    Optimization.disable_wifi()
    Optimization.reboot()


if __name__=="__main__":
    main()

    # while True:
    #     Does nothing for the moment