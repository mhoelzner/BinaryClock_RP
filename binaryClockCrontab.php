<?php

ini_set('display_errors', 1);

ini_set('display_startup_errors', 1);

error_reporting(E_ALL);

system('cd /var/www/html && sudo python binaryClockCrontab.py > /dev/null &');

echo 'done';

 ?>
