from crontab import CronTab
import time


def main():

    print("Writing to Crontab")

    my_cron = CronTab(user='www-data')
    job = my_cron.new(command='sudo python /var/www/html/binaryClock.py &')
    job.every_reboot()
    my_cron.write()

    time.sleep(2)
    return


if __name__ == '__main__':
    main()
