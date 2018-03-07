import os
import time
import sys


def main():

    param_1 = sys.argv[1]
    print(param_1)
    if param_1 == '0':
        print("Restarting")
        os.system('sudo shutdown -h now')
        time.sleep(3)
    elif param_1 == '1':
        print("Shutting Down")
        os.system('sudo shutdown -r now')
        time.sleep(3)

    return


if __name__ == '__main__':
    main()
