<?php

$iphoneOrHome = $_GET['iphoneOrHome'];

# if iphoneOrHome == 1 set wlan to use iphone hotspot
# if iphoneOrHome == 2 set wlan to use home network
# afer restart

if ($iphoneOrHome == 1) {
    system('cd /boot && sudo cp iphone_wpa_supplicant.conf wpa_supplicant.conf');
}
else {
    system('cd /boot && sudo cp home_wpa_supplicant.conf wpa_supplicant.conf');
}

echo 'done';

?>
