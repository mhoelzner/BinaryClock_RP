<?php

    $flag_zeigeSekunden = $_GET["flag_zeigeSekunden"];
    $flag_regenbogenChecked = $_GET["flag_regenbogenChecked"];
    $selectedColorID = $_GET["selectedColorID"];
    $r_value = $_GET["r_value"];
    $g_value = $_GET["g_value"];
    $b_value = $_GET["b_value"];
    $flag_hintergrundChecked = $_GET["flag_hintergrundChecked"];
    $hintergrundValue = $_GET["hintergrundValue"];
    $flag_tagesabhaengigChecked = $_GET["flag_tagesabhaengigChecked"];
    $generalValue = $_GET["generalValue"];
    $clock_running = $_GET["clock_running"];
    $clock_stop = $_GET["clock_stop"];
    $plugin_number = $_GET["plugin_number"];

    $myfile = fopen("./config/clockConfig.cfg", "w") or die("Unable to open file!");

    $txt = "[binaryclock_general]\n";
    fwrite($myfile, $txt);
    $txt = "show_seconds = " . $flag_zeigeSekunden . "\n";
    fwrite($myfile, $txt);
    $txt = " \n";
    fwrite($myfile, $txt);
    $txt = "[binaryclock_color]\n";
    fwrite($myfile, $txt);
    $txt = "rainbow_color = " . $flag_regenbogenChecked . "\n";
    fwrite($myfile, $txt);
    $txt = "id = " . $selectedColorID . "\n";
    fwrite($myfile, $txt);
    $txt = "r_value = " . $r_value . "\n";
    fwrite($myfile, $txt);
    $txt = "g_value = " . $g_value . "\n";
    fwrite($myfile, $txt);
    $txt = "b_value = " . $b_value . "\n";
    fwrite($myfile, $txt);
    $txt = " \n";
    fwrite($myfile, $txt);
    $txt = "[binaryclock_background]\n";
    fwrite($myfile, $txt);
    $txt = "background_color = " . $flag_hintergrundChecked . "\n";
    fwrite($myfile, $txt);
    $txt = "background_color_value = " . $hintergrundValue . "\n";
    fwrite($myfile, $txt);
    $txt = " \n";
    fwrite($myfile, $txt);
    $txt = "[binaryclock_sensitiv]\n";
    fwrite($myfile, $txt);
    $txt = "brightness_time_sensitiv = " . $flag_tagesabhaengigChecked . "\n";
    fwrite($myfile, $txt);
    $txt = "brightness_general = " . $generalValue . "\n";
    fwrite($myfile, $txt);
    $txt = " \n";
    fwrite($myfile, $txt);
    $txt = "[binaryclock_startstop]\n";
    fwrite($myfile, $txt);
    $txt = "clock_running = " . $clock_running . "\n";
    fwrite($myfile, $txt);
    $txt = "clock_stop = " . $clock_stop . "\n";
    fwrite($myfile, $txt);
    $txt = " \n";
    fwrite($myfile, $txt);
    $txt = "[binaryclock_plugins]\n";
    fwrite($myfile, $txt);
    $txt = "plugin_number = " . $plugin_number . "\n";
    fwrite($myfile, $txt);

    fclose($myfile);

 ?>
