<?php

  $path = "./config/clockConfig.cfg";
  $path_default = "./config/clockConfig_default.cfg";

  if (!file_exists($path)) {
      copy($path_default, $path);
  }

  $config = parse_ini_file($path);

  /*
  if ($config['clock_running'] == 0) {

    // if process binaryClock is running
    // but config file says otherwise
    // try to kill the process before executing
    $process_name = "binaryClock";

    $is_running = shell_exec("pgrep -f " . $process_name);
    if (isset($is_running)) {
      shell_exec("sudo kill -9 " . $is_running);
      //echo "process killed";
    }
  }
  */

?>

<!DOCTYPE html>
<html>
<title>Binary Clock</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=0.85, maximum-scale=0.85">
<link rel="stylesheet" href="./style/style.css">
<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet" type="text/css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<link rel="icon" href="./images/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="./images/apple-icon.png">

<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="white" />

<meta name="mobile-web-app-capable" content="yes">

<script>

  var flag_zeigeSekunden = <?php echo $config['show_seconds']; ?>;

  var flag_regenbogenChecked = <?php echo $config['rainbow_color']; ?>;
  var selectedColorID = <?php echo $config['id']; ?>;
  var r = <?php echo $config['r_value']; ?>;
  var g = <?php echo $config['g_value']; ?>;
  var b = <?php echo $config['b_value']; ?>;

  var flag_hintergrundChecked = <?php echo $config['background_color']; ?>;
  var hintergrundValue = <?php echo $config['background_color_value']; ?>;

  var flag_tagesabhaengigChecked = <?php echo $config['brightness_time_sensitiv']; ?>;
  var generalValue = <?php echo $config['brightness_general']; ?>;

  var clock_running = <?php echo $config['clock_running']; ?>;
  var clock_stop = <?php echo $config['clock_stop']; ?>;

  var plugin_number = <?php echo $config['plugin_number']; ?>;

</script>

<script src="./javascript/script.js"></script>

<body class="w3-light-grey" onload="timedRefresh(300000)";>

<div id="overlay" class="fadeMe">
    <div id="textfade">

    </div>
    <button id="btn_plugin_stop" class="w3-button w3-teal w3-round;" style="position:relative;top:55%;width:100%;display:none;">Stoppen</button>
</div>

<!-- Page Container -->
<div id="content" class="w3-content w3-margin-top" style="max-width:1400px;">

  <!-- The Grid -->
  <div class="w3-row-padding">

    <!-- Left Column -->
    <div class="w3-third">

      <div class="w3-white w3-text-grey w3-card">
        <div class="w3-display-container" style="max-width:200px; margin:0 auto; padding-bottom:40px; padding-top:50px;">
          <canvas id="myCanvas" width="200px" height="200px" style="border:1px solid #FF6952; background-color:#323232; display:block; max-width:100%;">
            <img src="./images/clock.png" style="max-width:100%; display:block; padding-top: 50px;" alt="Avatar">
          </canvas>
        </div>
        <div class="w3-container">
          <h2> Binary Clock </h2>
          <p>Eine Binäre Uhr basierend auf einem Raspberry Pi 3+, Adafruits Neopixel Streifen und einer portierten Adafruit Bibliothek von jgarff in python.</p>
          <hr>

            <button id="btn_starten" class="w3-button w3-teal w3-round" style="width:100%;">Uhr Starten</button>
            <button id="btn_stoppen" class="w3-button w3-red w3-round" style="width:100%;">Uhr Stoppen</button>

          <hr>
          <div class="container">
            <div class="header"><span>Erweitert +</span>

            </div>
            <div class="content">

              <button id="btn_shutdown" class="w3-button w3-raspberry w3-round" style="width:100%;">Raspberry Pi herunterfahren</button>
              <button id="btn_reboot" class="w3-button w3-raspberry w3-round" style="width:100%; margin-top:10px;">Raspberry Pi neustarten</button>
	      <button id="btn_reload" class="w3-button w3-raspberry w3-round" style="width:100%; margin-top:10px;" onClick="window.location.reload()">Seite Neu laden </button>
              <button id="btn_iphone" class="w3-button w3-raspberry w3-round" style="width:100%; margin-top:10px;">iPhone Hotspot nutzen</button>
              <button id="btn_homewifi" class="w3-button w3-raspberry w3-round" style="width:100%; margin-top:10px;">WLAN Daheim nutzen</button>

            </div>
          </div>
          <hr>

          <p> Markus Hölzner  |  2017
        </div>
      </div><br>

    <!-- End Left Column -->
    </div>

    <!-- Right Column -->
    <div id="konfiguration" class="w3-twothird">

      <div class="w3-container w3-card w3-white w3-margin-bottom">
        <h2 class="w3-text-grey"><i class="fa fa-suitcase fa-fw w3-margin-right w3-xxlarge w3-text-teal"></i>Konfiguration</h2>
      </div>
      <div class="w3-container w3-card w3-white w3-margin-bottom w3-margin-left">
        <div class="w3-container" style="margin-bottom:20px;">

          <div id="config">

              <h5 class="w3-opacity">Einstellung der Farbe, Hintergrundbeleuchtung und tagesabhäniger Helligkeit der zeitlichen Anzeige</h5>

              <div class="checkBox">
                  <input id="chb_zeigeSekunden" class="w3-check" type="checkbox">
                  <label>Sekunden zeigen</label>
                  <div class="description">
                      Die Anzeige der Zeit ohne Sekunden, nur durch Stunden und Minuten.
                  </div>
              </div>
              <hr>
              <!-- !Regenbogenfarben oder Solide Farbe! -->
              <div class="checkBox">
                  <input id="chb_regenbogen" class="w3-check" type="checkbox">
                  <label>Regenbogenfarben</label>
                  <div class="description">
                      Die LEDs leuchten innerhalb einer Stunde in allen Regenbogenfarben.
                  </div>
              </div>
              <div id="foreColor" class="colorPick">

                <div class="description">
                  Eine einzelne Farbe zur Darstellung der Zeit.
                </div>

                <div class="wrapper">
                  <div id="c01" class="foreColorDiv" style="background-color:#FF0000;" data-hex="FF0000" data-rgb="rgb(255,0,0)">

                  </div>
                  <div id="c02" class="foreColorDiv" style="background-color:#FF6000;" data-hex="FF6000" data-rgb="rgb(255,96,0)">

                  </div>
                  <div id="c03" class="foreColorDiv" style="background-color:#FFFF00;" data-hex="FFFF00" data-rgb="rgb(255,255,0)">

                  </div>
                  <div id="c04" class="foreColorDiv" style="background-color:#80FF00;" data-hex="80FF00" data-rgb="rgb(128,255,0)">

                  </div>
                  <div id="c05" class="foreColorDiv" style="background-color:#00FF00;" data-hex="00FF00" data-rgb="rgb(0,255,0)">

                  </div>
                  <div id="c06" class="foreColorDiv" style="background-color:#00FF80;" data-hex="00FF80" data-rgb="rgb(0,255,128)">

                  </div>
                  <div id="c07" class="foreColorDiv" style="background-color:#00FFFF;" data-hex="00FFFF" data-rgb="rgb(0,255,255)">

                  </div>
                  <div id="c08" class="foreColorDiv" style="background-color:#00B2FF;" data-hex="00B2FF" data-rgb="rgb(0,178,255)">

                  </div>
                  <div id="c09" class="foreColorDiv" style="background-color:#0000FF;" data-hex="0000FF" data-rgb="rgb(0,0,255)">

                  </div>
                  <div id="c10" class="foreColorDiv" style="background-color:#8000FF;" data-hex="8000FF" data-rgb="rgb(128,0,255)">

                  </div>
                  <div id="c11" class="foreColorDiv" style="background-color:#FF00FF;" data-hex="FF00FF" data-rgb="rgb(255,0,255)">

                  </div>
                  <div id="c12" class="foreColorDiv" style="background-color:#FF0080;" data-hex="FF0080" data-rgb="rgb(255,0,128)">

                  </div>
                  <div id="c13" class="foreColorDiv" style="background-color:#FFFFFF;" data-hex="FFFFFF" data-rgb="rgb(255,255,255)">

                  </div>
                </div>
              </div>
              <hr>
              <!-- !Hintergrundbeleuchtung! -->
              <div class="checkBox">
                  <input id="chb_hintergrund" class="w3-check" type="checkbox">
                  <label>Hintergrund LED an</label>
                  <div class="description">
                      LEDs, die nicht zur Darstellung der Zeit aktuellen Zeit genutzt werden, leuchten in einer bestimmten Helligkeit.
                  </div>
              </div>
              <div id="backgroundLight" class="lightPick">
                  <div class="description">
                      Die Helligkeit der Hintergrundbeleuchtung einstellen.
                  </div>
                  <div class="gradBlackWhite">
                      <input type="range" min="1" max="255" value="128" class="slider" id="lightRange" oninput="changeLightValue(this.value, 'lightRangeValue')">
                  </div>
                  <span id="lightRangeValue"></span>
              </div>
              <hr>
              <!-- !Tageszeitabhaengige Helligkeit! -->
              <div class="checkBox">
                  <input id="chb_tagesabhaengig" class="w3-check" type="checkbox">
                  <label>Tagesabhängige Helligkeit</label>
                  <div class="description">
                      Die Helligkeit wird Tagesabhängig geändert.
                  </div>
              </div>
              <div id="generalLight" class="generalLight">
                  <div class="description">
                      Die Helligkeit allgemein einstellen.
                  </div>
                  <div class="gradBlackWhite">
                      <input type="range" min="1" max="255" value="128" class="slider" id="generalRange" oninput="changeLightValue(this.value, 'generalRangeValue')">
                  </div>
                <span id="generalRangeValue"></span>
              </div>
          </div>
          <hr>
          <div id="speicherButton">
              <button id="btn_speichern"class="w3-button w3-teal w3-round" style="width:100%;">Speichern</button>
          </div>
        </div>
      </div>
      <div class="w3-container w3-card w3-white w3-margin-bottom">
        <h2 class="w3-text-grey"><i class="fa fa-suitcase fa-fw w3-margin-right w3-xxlarge w3-text-teal"></i>Plugins</h2>
      </div>
      <div class="w3-container w3-card w3-white w3-margin-bottom w3-margin-left">
        <div class="w3-container" style="margin-bottom:20px;">
          <div class="pluginWrapper">
              <div class="pluginText"><h5 class="w3-opacity">Zeit als Text</h5></div>
              <div class="pluginBtn"><button id="btn_plugin2"class="w3-button w3-teal w3-round" style="width:66%;">Los</button></div>
          </div>
          <div class="description">
              Darstellung der aktuellen Zeit als Text, der von Rechts nach Links über die Anzeige wandert.
          </div>
          <div class="checkBox">
              <input id="chb_customText" class="w3-check" type="checkbox">
              <label>Spezieller Text</label>
              <input id="txt_customText" class="w3-input" type="text" maxlength="26" style="margin-top:10px;">
          </div>
          <hr>
          <div class="pluginWrapper">
              <div class="pluginText"><h5 class="w3-opacity">Startanimation zeigen</h5></div>
              <div class="pluginBtn"><button id="btn_plugin4"class="w3-button w3-teal w3-round" style="width:66%;">Los</button></div>
          </div>
          <div class="description">
              Die Animation, welche beim Start der Binären Uhr gezeigt wird.
          </div>
          <hr>
          <div class="pluginWrapper">
              <div class="pluginText"><h5 class="w3-opacity">Regenbogen über LEDs</h5></div>
              <div class="pluginBtn"><button id="btn_plugin5"class="w3-button w3-teal w3-round" style="width:66%;">Los</button></div>
          </div>
          <div class="description">
              Eine Regenbogenanimation, welche über alle LEDs läuft.
          </div>
          <hr>
          <div class="pluginWrapper">
              <div class="pluginText"><h5 class="w3-opacity">Matrix Effekt</h5></div>
              <div class="pluginBtn"><button id="btn_plugin3"class="w3-button w3-teal w3-round" style="width:66%;">Los</button></div>
          </div>
          <div class="description">
              Matrix Quellcode Animation als fallender grüner Code, um die Aktivität der Virtual-Reality-Umgebung der Matrix darzustellen.
          </div>
          <hr>
          <div class="pluginWrapper">
              <div class="pluginText"><h5 class="w3-opacity">Kamin Feuer</h5></div>
              <div class="pluginBtn"><button id="btn_plugin6"class="w3-button w3-teal w3-round" style="width:66%;">Los</button></div>
          </div>
          <div class="description">
              Simuliert das Brennen eines Kaminfeuers.
          </div>
          <hr>
        </div>
      </div>
    <!-- End Right Column -->
    </div>

  <!-- End Grid -->
  </div>

  <!-- End Page Container -->
</div>

<!--footer class="w3-container w3-teal w3-center w3-margin-top">
</footer-->

</body>
</html>
