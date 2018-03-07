// DEFAULTS
var def_flag_zeigeSekunden = 1;

var def_flag_regenbogenChecked = 1;
var def_selectedColorID = 9;
var def_r = 77;
var def_g = 182;
var def_b = 172;

var def_flag_hintergrundChecked = 0;
var def_hintergrundValue = 4;

var def_flag_tagesabhaengigChecked = 1;
var def_generalValue = 255;

var def_clock_running = 0;
var def_clock_stop = 0;

var def_plugin_number = 1;

var timerID = 0;

$(document).ready(function(){

    /* Beim Start auslesen der aktuellen Daten aus der Config Datei */
    /* ************************************************************ */

    if (flag_zeigeSekunden == 1) {
        $('#chb_zeigeSekunden').prop('checked', true);
    }
    else {
        $('#chb_zeigeSekunden').prop('checked', false);
    }

    // setzen ob regenbogen oder solide farbe
    if (flag_regenbogenChecked == 1) {
        // regenbogen farben nutzten
        $('#chb_regenbogen').prop('checked', true);
        $('#foreColor').css('opacity', '0.2');
        $('.foreColorDiv').off('click', showBorder);
        $('#c1').removeClass('selected').siblings().removeClass('selected');
        $('#c1').css({'border-color':'#f1f1f1'}).siblings().css({'border-color':'#f1f1f1'});
    }
    else {
        // keine regenbogen sondern solide farbe auswählen
        $('#chb_regenbogen').prop('checked', false);
        $('#foreColor').css('opacity', '1.0');
        $('.foreColorDiv').on('click', showBorder);
        $('#c' + ("0" + selectedColorID).slice(-2)).addClass('selected');
        $('#c' + ("0" + selectedColorID).slice(-2)).css({'border-color':'#323232'});
    }

    // Hintergrund LEDs an oder aus
    if (flag_hintergrundChecked == 1) {
        // hintergrund LEDs an -> setzten der Helligkeit ermöglichen
        $('#chb_hintergrund').prop('checked', true);
        $('#backgroundLight').css('opacity', '1.0');
        document.getElementById("lightRange").disabled = false;
        $('#lightRange').val(hintergrundValue);
    }
    else {
        // hintergrund LEDs aus -> standartwert seten (LEDs aus)
        $('#chb_hintergrund').prop('checked', false);
        $('#backgroundLight').css('opacity', '0.2');
        document.getElementById("lightRange").disabled = true;
        $('#lightRange').val(4);
    }

    // Tagesabhaenige Helligkeit einstellen
    if (flag_tagesabhaengigChecked == 1) {
        // Tagesabhaenige helligkeit wird automatisch geregelt
        $('#generalLight').hide();

        $('#chb_tagesabhaengig').prop('checked', true);
        $('#generalRange').val(def_generalValue);
    }
    else {
        // Einstellmöglichkeit der Tages und Nachthelligkeit
        $('#generalLight').show();

        $('#chb_tagesabhaengig').prop('checked', false);
        $('#generalRange').val(generalValue);
    }

    // Uhr starten / stoppen
    if (clock_running == 0) {
	      // uhr laeuft nicht - starten button zeigen / btn_stoppen verstecken
	      $('#btn_starten').show()
    	  $('#btn_stoppen').hide();
        $('#konfiguration').hide();

        showJSSplashScreen();

    }
    else {
	      // uhr laeuft - starten button verstecken / btn_stoppen zeigen
    	  $('#btn_starten').hide();
	      $('#btn_stoppen').show();
        $('#konfiguration').show();

        runJSClock();
        timerID = window.setInterval(function(){
          runJSClock();
        }, 1000);

    }

    switch(plugin_number) {
        case 6:
            // Kaminfeuer
            $('#overlay').show();
            $('#textfade').html("Reumantisch");
            $('#btn_plugin_stop').show();
            break;
        case 5:
            // Regenbogen
            $('#overlay').show();
            $('#textfade').html("Regenbogen");
            $('#btn_plugin_stop').show();
            break;
        case 4:
            // Splashscreen
            break;
        case 3:
            // Matrix Effekt
            $('#overlay').show();
            $('#textfade').html("Enter the Matrix.");
            $('#btn_plugin_stop').show();
            break;
        case 2:
            // Text Zeigen
            break;
        default:

    }

    $('#lightRangeValue').html(String(parseInt((hintergrundValue * 100) / 255)) + "%");
    $('#generalRangeValue').html(String(parseInt((generalValue * 100) / 255)) + "%");

    $('#chb_customText').prop('checked', false);
    $('#txt_customText').hide();

    /* Click und Slide Events
    /* ******************************************************************* */

    $(".header").click(function () {


        $header = $(this);
        //getting the next element
        $content = $header.next();
        //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
        $content.slideToggle(500, function () {
            //execute this after slideToggle is done
            //change text of header based on visibility of content div
            $header.text(function () {
                //change text based on condition
                return $content.is(":visible") ? "Erweitert -" : "Erweitert +";
            });
        });

    });

    $("#btn_shutdown").click(function () {

      $('#overlay').show();
      $('#textfade').html("Shutdown");

      if (clock_running == 1) {
          clock_stop = 1;
          saveConfigFile();
      }

      setTimeout(function(){

        $.ajax({
            url: './binaryClockShutdown.php',
            type: "GET",
            data: "restart=0",
            success: function(result) {

                setTimeout(function(){

                  $('#btn_starten').show();
                  $('#btn_stoppen').hide();

                  $('#overlay').hide();
                  $('#konfiguration').hide();
                  clock_stop = 0;
                  clock_running = 0

                  clearInterval(timerID);
                  showJSSplashScreen();

                  window.location = "http://www.google.com";

                }, 10000);

            }
        });

      }, 5000);

    });

    $("#btn_reboot").click(function () {

      $('#overlay').show();
      $('#textfade').html("Reboot");

      if (clock_running == 1) {
          clock_stop = 1;
          saveConfigFile();
      }

      setTimeout(function(){

        $.ajax({
            url: './binaryClockShutdown.php',
            type: "GET",
            data: "restart=1",
            success: function(result) {

                setTimeout(function(){

                  $('#btn_starten').show();
                  $('#btn_stoppen').hide();

                  $('#overlay').hide();
                  $('#konfiguration').hide();
                  clock_stop = 0;
                  clock_running = 0

                  clearInterval(timerID);
                  showJSSplashScreen();

                  timedRefresh(1);

                }, 10000);

            }
        });

      }, 5000);

    });

    $("#btn_crontab").click(function () {

      $('#overlay').show();
      $('#textfade').html("Crontab wird geschrieben.");

      $.ajax({
          url: './binaryClockCrontab.php',
          success: function(result) {

              setTimeout(function(){

                $('#overlay').hide();

              }, 2000);

          }
      });

    });

    $("#btn_iphone").click(function () {

        $('#overlay').show();
        $('#textfade').html("Nach Neustart wird iPhone Hotspot genutzt.");

        $.ajax({
            url: './binaryClockSetWpaSupplicant.php',
            type: "GET",
            data: "iphoneOrHome=1",
            success: function(result) {

                setTimeout(function(){

                  $('#overlay').hide();

                }, 3000);

            }
        });

    });

    $("#btn_homewifi").click(function () {

        $('#overlay').show();
        $('#textfade').html("Nach Neustart wird Heim WLAN genutzt.");

        $.ajax({
            url: './binaryClockSetWpaSupplicant.php',
            type: "GET",
            data: "iphoneOrHome=2",
            success: function(result) {

                setTimeout(function(){

                  $('#overlay').hide();

                }, 3000);

            }
        });

    });

    $('#chb_zeigeSekunden').change(function(){
        if(this.checked){
            flag_zeigeSekunden = 1;
        }
        else {
            flag_zeigeSekunden = 0;
        }
    });

    $('#chb_regenbogen').change(function(){
        if(this.checked){
            // regenbogen farben
            $('#foreColor').css('opacity', '0.2');
            $('.foreColorDiv').off('click', showBorder);
            $('#c1').removeClass('selected').siblings().removeClass('selected');
            $('#c1').css({'border-color':'#f1f1f1'}).siblings().css({'border-color':'#f1f1f1'});

            flag_regenbogenChecked = 1;

        }
        else {
            // keine regenbogen sondern solide farbe auswählen
            $('#foreColor').css('opacity', '1.0');
            $('.foreColorDiv').on('click', showBorder);
            $('#c' + ("0" + selectedColorID).slice(-2)).addClass('selected');
            $('#c' + ("0" + selectedColorID).slice(-2)).css({'border-color':'#323232'});

            flag_regenbogenChecked = 0;

        }
    });

    function showBorder() {
        $(this).css({'border-color':'#323232'}).siblings().css({'border-color':'#f1f1f1'});
        $(this).addClass('selected').siblings().removeClass('selected');

        selectedColorID = parseInt($(this).attr('id').substring(1,3));

        rgb =  $(this).data('rgb').replace(/[^\d,]/g, '').split(',');
        r = rgb[0];
        g = rgb[1];
        b = rgb[2];


    }

    $('#chb_hintergrund').change(function(){
        if(this.checked){

            $('#backgroundLight').css('opacity', '1.0');
            document.getElementById("lightRange").disabled = false;
            $('#lightRange').val(hintergrundValue);

            flag_hintergrundChecked = 1;
        }
        else {

            $('#backgroundLight').css('opacity', '0.2');
            document.getElementById("lightRange").disabled = true;
            $('#lightRange').val(4);

            flag_hintergrundChecked = 0;

        }
    });

    $('#chb_tagesabhaengig').change(function(){
        if(this.checked){

            $('#generalLight').hide();

            $('#chb_tagesabhaengig').prop('checked', true);
            $('#generalRange').val(def_generalValue)

            flag_tagesabhaengigChecked = 1;

        }
        else {

            $('#generalLight').show();

            $('#chb_tagesabhaengig').prop('checked', false);
            $('#generalRange').val(generalValue)

            flag_tagesabhaengigChecked = 0;

        }
    });

    $('#btn_starten').click(function(){

        $('#overlay').show();
        $('#textfade').html("Uhr wird gestartet.");

        $.ajax({
            url: './startClock.php',
            success: function(result) {

                setTimeout(function(){
 		                clock_running = 1;
 		                saveConfigFile();
                    $('#btn_starten').hide();
                    $('#btn_stoppen').show();
                    $('#overlay').hide();
                    $('#konfiguration').show();

                    runJSClock();
                    timerID = window.setInterval(function(){
                      runJSClock();
                    }, 1000);

                }, 6000);

            }
        });
    });

    $('#btn_stoppen').click(function(){

        clock_stop = 1;
        saveConfigFile();

        $('#overlay').show();
        $('#textfade').html("Uhr wird gestoppt.");
        $('#btn_starten').show();
        $('#btn_stoppen').hide();

        setTimeout(function(){

          $('#overlay').hide();
          $('#konfiguration').hide();
          clock_stop = 0;
          clock_running = 0

          clearInterval(timerID);
          showJSSplashScreen();

        }, 3000);

    });

    $('#btn_speichern').click(function(){

        saveConfigFile();

        $('#overlay').show();
        $('#textfade').html("Änderungen werden gespeichert.");

        setTimeout(function(){

          $('#overlay').hide();

        }, 3000);

    });

    function saveConfigFile(){

         $.ajax({
            url: './writeConfigFile.php',
            type: "GET",
		        data: "flag_zeigeSekunden=" + flag_zeigeSekunden +
                  "&flag_regenbogenChecked=" + flag_regenbogenChecked +
                  "&selectedColorID=" + selectedColorID +
                  "&r_value=" + r +
                  "&g_value=" + g +
                  "&b_value=" + b +
                  "&flag_hintergrundChecked=" + flag_hintergrundChecked +
                  "&hintergrundValue=" + hintergrundValue +
                  "&flag_tagesabhaengigChecked=" + flag_tagesabhaengigChecked +
                  "&generalValue=" + generalValue +
		          "&clock_running=" + clock_running +
		          "&clock_stop=" + clock_stop +
                  "&plugin_number=" + plugin_number,
            success: function(result) {
                //alert('Daten wurden geaendert' + result);
            }
          });
     }

     function writeCustomTextFile(){

          $.ajax({
             url: './writeCustomTextFile.php',
             type: "GET",
 		        data: "text=" + $('#txt_customText').val(),
             success: function(result) {
                 //alert('Daten wurden geaendert' + result);
             }
           });
      }

     var timeForFade = 7000;
     // Zeit als Text darstellen
     $('#btn_plugin2').click(function(){

          if ($('#txt_customText').val().length > 0) {
             writeCustomTextFile();
             timeForFade += 11000;
          }

          plugin_number = 2;
          saveConfigFile();

          $('#overlay').show();
          $('#textfade').html("Zeit wird als Text dargestellt.");

          setTimeout(function(){

            $('#overlay').hide();
            plugin_number = 1;
            $('#chb_customText').prop('checked', false);
            $('#txt_customText').val('');
            $('#txt_customText').hide();

          }, timeForFade);

          timeForFade = 7000;

     });

     $('#chb_customText').change(function(){
         $('#txt_customText').val('');
         if(this.checked){
           $('#txt_customText').show();
         }
         else {
           $('#txt_customText').hide();
         }
     });

     // Matrix Effekt
     $('#btn_plugin3').click(function(){

         plugin_number = 3;
         saveConfigFile();

         $('#overlay').show();
         $('#textfade').html("Enter the Matrix.");
         $('#btn_plugin_stop').show();

     });

     // Splashscreen Animation
     $('#btn_plugin4').click(function(){

         plugin_number = 4;
         saveConfigFile();

         $('#overlay').show();
         $('#textfade').html("Splash.");

         setTimeout(function(){

           $('#overlay').hide();
           plugin_number = 1;

         }, 6000);

     });

     // Regenbogen Animation
     $('#btn_plugin5').click(function(){

         plugin_number = 5;
         saveConfigFile();

         $('#overlay').show();
         $('#textfade').html("Regenbogen");
         $('#btn_plugin_stop').show();

     });


     $('#btn_plugin6').click(function(){

         plugin_number = 6;
         saveConfigFile();

         $('#overlay').show();
         $('#textfade').html("Reumantisch!");
         $('#btn_plugin_stop').show();

     });

     $('#btn_plugin_stop').click(function(){

         plugin_number = 1;
         saveConfigFile();
         $('#overlay').hide();
         $('#btn_plugin_stop').hide();

     });


});

function changeLightValue(val,rangeValue) {

    var percentValue = 100;

    if (rangeValue == 'lightRangeValue'){
      // Hintergrund LED Helligkeit
      hintergrundValue = val
      percentValue = parseInt((val * 100) / 255);
    }
    else if (rangeValue = 'generalRangeValue'){
      generalValue = val
      percentValue = parseInt((val * 100) / 255);
    }

    $('#' + rangeValue).html(String(percentValue) + "%");

}

function bitsOfNumber(n) {

  var a = [];
  if (n > 0) {
      while (true) {
          var x = Math.log(n,2)
          bit = Math.pow(2, Math.floor(Math.log2(n)));
          a.push(bit);
          n -= a[a.length - 1];
          if (n == 0){
              break;
          }
       }
  }
  return a
}

function showJSSplashScreen(){

  var c = document.getElementById("myCanvas");
  var ctx = c.getContext("2d");

  var cb = "#626262";
  var cf = "#FF6952";

  // alle ausmalen


  // hl
  ctx.beginPath();
  ctx.fillStyle = cb;
  ctx.arc(32, 52, 12, 0, 2 * Math.PI);
  ctx.arc(32, 81, 12, 0, 2 * Math.PI);
  ctx.arc(32, 110, 12, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.fillStyle = cf;
  ctx.arc(32, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // hr
  ctx.beginPath();
  ctx.fillStyle = cb;
  ctx.arc(59, 52, 12, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.fillStyle = cf;
  ctx.arc(59, 81, 12, 0, 2 * Math.PI);
  ctx.arc(59, 110, 12, 0, 2 * Math.PI);
  ctx.arc(59, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // ml
  ctx.beginPath();
  ctx.fillStyle = cb;
  ctx.arc(86, 52, 12, 0, 2 * Math.PI);
  ctx.arc(86, 81, 12, 0, 2 * Math.PI);
  ctx.arc(86, 110, 12, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.fillStyle = cf;
  ctx.arc(86, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // mr
  ctx.beginPath();
  ctx.fillStyle = cb;
  ctx.arc(113, 52, 12, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.fillStyle = cf;
  ctx.arc(113, 81, 12, 0, 2 * Math.PI);
  ctx.arc(113, 110, 12, 0, 2 * Math.PI);
  ctx.arc(113, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // ml
  ctx.beginPath();
  ctx.fillStyle = cb;
  ctx.arc(140, 52, 12, 0, 2 * Math.PI);
  ctx.arc(140, 81, 12, 0, 2 * Math.PI);
  ctx.arc(140, 110, 12, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.fillStyle = cf;
  ctx.arc(140, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // sr
  ctx.beginPath();
  ctx.fillStyle = cb;
  ctx.arc(167, 52, 12, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.fillStyle = cf;
  ctx.arc(167, 81, 12, 0, 2 * Math.PI);
  ctx.arc(167, 110, 12, 0, 2 * Math.PI);
  ctx.arc(167, 139, 12, 0, 2 * Math.PI);
  ctx.fill();

}

function runJSClock(){

  var c = document.getElementById("myCanvas");
  var ctx = c.getContext("2d");

  ctx.clearRect(0, 0, c.width, c.height);

  var cb = "#626262";
  var cf = "#FF6952";

  var d = new Date(); // for now
  var h = d.getHours(); // => 9
  var m = d.getMinutes(); // =>  30
  var s = d.getSeconds(); // => 51

  var hl = Math.floor(h/10.0);
  var lst_hl = bitsOfNumber(hl);
  var hr = h - (hl * 10.0);
  var lst_hr = bitsOfNumber(hr);

  var ml = Math.floor(m/10.0);
  var lst_ml = bitsOfNumber(ml);
  var mr = m - (ml * 10.0);
  var lst_mr = bitsOfNumber(mr);

  var sl = Math.floor(s/10.0);
  var lst_sl = bitsOfNumber(sl);
  var sr = s - (sl * 10.0);
  var lst_sr = bitsOfNumber(sr);

  // alle ausmalen

  ctx.beginPath();
  ctx.fillStyle = cb;
  // hl
  ctx.arc(32, 52, 12, 0, 2 * Math.PI);
  ctx.arc(32, 81, 12, 0, 2 * Math.PI);
  ctx.arc(32, 110, 12, 0, 2 * Math.PI);
  ctx.arc(32, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // hr
  ctx.beginPath();
  ctx.arc(59, 52, 12, 0, 2 * Math.PI);
  ctx.arc(59, 81, 12, 0, 2 * Math.PI);
  ctx.arc(59, 110, 12, 0, 2 * Math.PI);
  ctx.arc(59, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // ml
  ctx.beginPath();
  ctx.arc(86, 52, 12, 0, 2 * Math.PI);
  ctx.arc(86, 81, 12, 0, 2 * Math.PI);
  ctx.arc(86, 110, 12, 0, 2 * Math.PI);
  ctx.arc(86, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // mr
  ctx.beginPath();
  ctx.arc(113, 52, 12, 0, 2 * Math.PI);
  ctx.arc(113, 81, 12, 0, 2 * Math.PI);
  ctx.arc(113, 110, 12, 0, 2 * Math.PI);
  ctx.arc(113, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // ml
  ctx.beginPath();
  ctx.arc(140, 52, 12, 0, 2 * Math.PI);
  ctx.arc(140, 81, 12, 0, 2 * Math.PI);
  ctx.arc(140, 110, 12, 0, 2 * Math.PI);
  ctx.arc(140, 139, 12, 0, 2 * Math.PI);
  ctx.fill();
  // sr
  ctx.beginPath();
  ctx.arc(167, 52, 12, 0, 2 * Math.PI);
  ctx.arc(167, 81, 12, 0, 2 * Math.PI);
  ctx.arc(167, 110, 12, 0, 2 * Math.PI);
  ctx.arc(167, 139, 12, 0, 2 * Math.PI);
  ctx.fill();

  // hl
  ctx.beginPath();
  ctx.fillStyle = cf;
  for (var i=0, l=lst_hl.length; i<l; i++) {
    var item = lst_hl[i];
    switch(item) {
    case 8:
        ctx.arc(32, 52, 12, 0, 2 * Math.PI);
        break;
    case 4:
        ctx.arc(32, 81, 12, 0, 2 * Math.PI);
        break;
    case 2:
        ctx.arc(32, 110, 12, 0, 2 * Math.PI);
        break;
    default:
        ctx.arc(32, 139, 12, 0, 2 * Math.PI);
        break;
    }

  }
  ctx.fill();

  // hr
  ctx.beginPath();
  ctx.fillStyle = cf;
  for (var i=0, l=lst_hr.length; i<l; i++) {
    var item = lst_hr[i];
    switch(item) {
    case 8:
        ctx.arc(59, 52, 12, 0, 2 * Math.PI);
        break;
    case 4:
        ctx.arc(59, 81, 12, 0, 2 * Math.PI);
        break;
    case 2:
        ctx.arc(59, 110, 12, 0, 2 * Math.PI);
        break;
    default:
        ctx.arc(59, 139, 12, 0, 2 * Math.PI);
        break;
    }
  }
  ctx.fill();

  // ml
  ctx.beginPath();
  ctx.fillStyle = cf;
  for (var i=0, l=lst_ml.length; i<l; i++) {
    var item = lst_ml[i];
    switch(item) {
    case 8:
        ctx.arc(86, 52, 12, 0, 2 * Math.PI);
        break;
    case 4:
        ctx.arc(86, 81, 12, 0, 2 * Math.PI);
        break;
    case 2:
        ctx.arc(86, 110, 12, 0, 2 * Math.PI);
        break;
    default:
        ctx.arc(86, 139, 12, 0, 2 * Math.PI);
        break;
    }
  }
  ctx.fill();

  // mr
  ctx.beginPath();
  ctx.fillStyle = cf;
  for (var i=0, l=lst_mr.length; i<l; i++) {
    var item = lst_mr[i];
    switch(item) {
    case 8:
        ctx.arc(113, 52, 12, 0, 2 * Math.PI);
        break;
    case 4:
        ctx.arc(113, 81, 12, 0, 2 * Math.PI);
        break;
    case 2:
        ctx.arc(113, 110, 12, 0, 2 * Math.PI);
        break;
    default:
        ctx.arc(113, 139, 12, 0, 2 * Math.PI);
        break;
    }
  }
  ctx.fill();
  // sl
  ctx.beginPath();
  ctx.fillStyle = cf;
  for (var i=0, l=lst_sl.length; i<l; i++) {
    var item = lst_sl[i];
    switch(item) {
    case 8:
        ctx.arc(140, 52, 12, 0, 2 * Math.PI);
        break;
    case 4:
        ctx.arc(140, 81, 12, 0, 2 * Math.PI);
        break;
    case 2:
        ctx.arc(140, 110, 12, 0, 2 * Math.PI);
        break;
    default:
        ctx.arc(140, 139, 12, 0, 2 * Math.PI);
        break;
    }
  }
  ctx.fill();
  // sr
  ctx.beginPath();
  ctx.fillStyle = cf;
  for (var i=0, l=lst_sr.length; i<l; i++) {
    var item = lst_sr[i];
    switch(item) {
    case 8:
        ctx.arc(167, 52, 12, 0, 2 * Math.PI);
        break;
    case 4:
        ctx.arc(167, 81, 12, 0, 2 * Math.PI);
        break;
    case 2:
        ctx.arc(167, 110, 12, 0, 2 * Math.PI);
        break;
    default:
        ctx.arc(167, 139, 12, 0, 2 * Math.PI);
        break;
    }
  }
  ctx.fill();
}

function timedRefresh(timeoutPeriod) {
    setTimeout('location.reload(true);',timeoutPeriod);
}
