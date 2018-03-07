Anleitung nachdem SD Karte mit aktuellem Raspbian bestückt worden ist.
**********************************************************************

Raspian Konfigurieren
    
    sudo raspi-config
    -> Nutzerpasswort ändern
    -> Hostnamen ändern
        -> binaryclock.local
    -> expand file system
    -> locale setzten
    -> anschalten von SSH
    -> anschalten von I2C


Apache und PHP installieren

    sudo apt-get update
    sudo apt-get install apache2 php


Rechtevergabe und Owner von /var/www/html ändern

    cd /var/www
    sudo chown www-data:www-data html/
    sudo chmod 755 html/


Python Bibliothek für die Nutzung der Neopixel installieren

    sudo apt-get install build-essential python-dev git scons swig
    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x/
    scons
    cd python
    sudo python setup.py install


Python Bibliothek für die Anzeige von Texten installieren

    sudo apt-get install python-pip ttf-freefont
    sudo pip install freetype-py


Python Bibliothek zur Änderungverfolgung von Dateien installieren

    sudo pip install watchdog


Python Bibliothek zum Schreiben von Crontab installieren

    sudo pip install python-crontab


Python Bibliothek zur Nutzung der RTC (pcf8523)

    sudo apt-get install -y python-smbus
    sudo apt-get install -y i2c-tools
    
    Änderungen an der /boot/config.txt vornehmen
    
        sudo nano /boot/config.txt
        -> dtoverlay=i2c-rtc,pcf8523
        
    Prüfen ob es geklappt hat mit
    
        sudo i2cdetect -y 1
        
    Neustarten
    
    Jetzt die fake-hwclock ausschalten
    
        sudo apt-get -y remove fake-hwclock
        sudo update-rc.d -f fake-hwclock remove
        sudo nano /lib/udev/hwclock-set
        -> ersten if Anweisung auskommentieren
        
    Neustarten
    
    Schreiben der aktuellen Zeit des Pi auf die RTC
    
        sudo hwclock -w
        
    Pruefen aller Systemzeiten
    
        timedatectl status


Aufnahme der Nutzer pi und www-data in die sudoers

    sudo nano /etc/sudoers
    -> www-data ALL=(ALL) NOPASSWD: ALL
    -> pi ALL=(ALL) NOPASSWD: ALL
    sudo adduser pi sudo
    sudo adduser www-data sudo


Alle Relevanten Dateien in das /var/www/html Verzeichnis kopieren
anschließend nocheinmal die Berechtigungen setzten

    scp -r /Pfad/Wo/BinaryClockDateien/liegen/* pi@binaryclock.local:var/www/html
    sudo chmod -R 755 html/
    sudo chown -R www-data:www-data html/
