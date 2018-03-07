<?php

ini_set('display_errors', 1);

ini_set('display_startup_errors', 1);

error_reporting(E_ALL);

$restart = $_GET['restart'];

if ($restart == 1) {
  system('cd /var/www/html && sudo python binaryClockShutdown.py 1 > /dev/null &');
}
else {
  system('cd /var/www/html && sudo python binaryClockShutdown.py 0 > /dev/null &');
}

echo 'done';

 ?>
