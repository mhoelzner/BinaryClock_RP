<?php

    $text = $_GET["text"];

    $myfile = fopen("./other/customText.txt", "w") or die("Unable to open file!");

    fwrite($myfile, $text);

    fclose($myfile);

 ?>
