<?php
session_start();
error_reporting(E_ERROR | E_PARSE);
date_default_timezone_set('Europe/Berlin');
header('Content-type: text/html; charset=utf-8');


#########################################################################
#	Kontaktformular.com         					                                #
#	http://www.kontaktformular.com        						                    #
#	All rights by KnotheMedia.de                                    			#
#-----------------------------------------------------------------------#
#	I-Net: http://www.knothemedia.de                            					#
#########################################################################
// Der Copyrighthinweis darf NICHT entfernt werden!


  $script_root = substr(__FILE__, 0,
                        strrpos(__FILE__,
                                DIRECTORY_SEPARATOR)
                       ).DIRECTORY_SEPARATOR;



$remote = getenv("REMOTE_ADDR");

function encrypt($string, $key) {
$result = '';
for($i=0; $i<strlen($string); $i++) {
   $char = substr($string, $i, 1);
   $keychar = substr($key, ($i % strlen($key))-1, 1);
   $char = chr(ord($char)+ord($keychar));
   $result.=$char;
}
return base64_encode($result);
}
$sicherheits_eingabe = encrypt($_POST["sicherheitscode"], "8h384ls94");
$sicherheits_eingabe = str_replace("=", "", $sicherheits_eingabe);



if ($_POST['delete'])
{
unset($_POST);
}

if ($_POST["kf-km"]) {
$empfaenger      = "no-reply@kontaktformular.com";

$email      = $_POST["email"];

   $date = date("d.m.Y | H:i");
   $ip = $_SERVER['REMOTE_ADDR']; 
   $UserAgent = $_SERVER["HTTP_USER_AGENT"];
   $host = getHostByAddr($remote);

$email = stripslashes($email);

 
if (!preg_match("/^[0-9a-zA-ZÄÜÖ_.-]+@[0-9a-z.-]+\.[a-z]{2,6}$/", $email)) {
   $fehler['email'] = "<font color=#cc3333>Geben Sie bitte eine <strong>E-Mail-Adresse</strong> ein.\n<br /></font>";
}

    if (!isset($fehler) || count($fehler) == 0) {
      $error             = false;
      $errorMessage      = '';
      $uploadErrors      = array();
      $uploadedFiles     = array();
      $totalUploadSize   = 0;

      if ($cfg['UPLOAD_ACTIVE'] && in_array($_SERVER['REMOTE_ADDR'], $cfg['BLACKLIST_IP']) === true) {
          $error = true;
          $fehler['upload'] = '<font color=#990000>Sie haben keine Erlaubnis Dateien hochzuladen.<br /></font>';
      }
$dsmsg = "". $_SERVER['HTTP_REFERER'] ."";
      if (!$error) {
          for ($i=0; $i < $cfg['NUM_ATTACHMENT_FIELDS']; $i++) {
              if ($_FILES['f']['error'][$i] == UPLOAD_ERR_NO_FILE) {
                  continue;
              }

              $extension = explode('.', $_FILES['f']['name'][$i]);
              $extension = strtolower($extension[count($extension)-1]);
              $totalUploadSize += $_FILES['f']['size'][$i];

              if ($_FILES['f']['error'][$i] != UPLOAD_ERR_OK) {
                  $uploadErrors[$j]['name'] = $_FILES['f']['name'][$i];
                  switch ($_FILES['f']['error'][$i]) {
                      case UPLOAD_ERR_INI_SIZE :
                          $uploadErrors[$j]['error'] = 'Die Datei ist zu groß (PHP-Ini Direktive).';
                      break;
                      case UPLOAD_ERR_FORM_SIZE :
                          $uploadErrors[$j]['error'] = 'Die Datei ist zu groß (MAX_FILE_SIZE in HTML-Formular).';
                      break;
                      case UPLOAD_ERR_PARTIAL :
						  if ($cfg['UPLOAD_ACTIVE']) {
                          	  $uploadErrors[$j]['error'] = 'Die Datei wurde nur teilweise hochgeladen.';
						  } else {
							  $uploadErrors[$j]['error'] = 'Die Datei wurde nur teilweise versendet.';
					  	  }
                      break;
                      case UPLOAD_ERR_NO_TMP_DIR :
                          $uploadErrors[$j]['error'] = 'Es wurde kein temporärer Ordner gefunden.';
                      break;
                      case UPLOAD_ERR_CANT_WRITE :
                          $uploadErrors[$j]['error'] = 'Fehler beim Speichern der Datei.';
                      break;
                      case UPLOAD_ERR_EXTENSION  :
                          $uploadErrors[$j]['error'] = 'Unbekannter Fehler durch eine Erweiterung.';
                      break;
                      default :
						  if ($cfg['UPLOAD_ACTIVE']) {
                          	  $uploadErrors[$j]['error'] = 'Unbekannter Fehler beim Hochladen.';
						  } else {
							  $uploadErrors[$j]['error'] = 'Unbekannter Fehler beim Versenden des Email-Attachments.';
						  }
                  }

                  $j++;
                  $error = true;
              }
              else if ($totalUploadSize > $cfg['MAX_ATTACHMENT_SIZE']*1024) {
                  $uploadErrors[$j]['name'] = $_FILES['f']['name'][$i];
                  $uploadErrors[$j]['error'] = 'Maximaler Upload erreicht ('.$cfg['MAX_ATTACHMENT_SIZE'].' KB).';
                  $j++;
                  $error = true;
              }
              else if ($_FILES['f']['size'][$i] > $cfg['MAX_FILE_SIZE']*1024) {
                  $uploadErrors[$j]['name'] = $_FILES['f']['name'][$i];
                  $uploadErrors[$j]['error'] = 'Die Datei ist zu groß (max. '.$cfg['MAX_FILE_SIZE'].' KB).';
                  $j++;
                  $error = true;
              }
              else if (!empty($cfg['BLACKLIST_EXT']) && strpos($cfg['BLACKLIST_EXT'], $extension) !== false) {
                  $uploadErrors[$j]['name'] = $_FILES['f']['name'][$i];
                  $uploadErrors[$j]['error'] = 'Die Dateiendung ist nicht erlaubt.';
                  $j++;
                  $error = true;
              }
              else if (preg_match("=^[\\:*?<>|/]+$=", $_FILES['f']['name'][$i])) {
                  $uploadErrors[$j]['name'] = $_FILES['f']['name'][$i];
                  $uploadErrors[$j]['error'] = 'Ungültige Zeichen im Dateinamen (\/:*?<>|).';
                  $j++;
                  $error = true;
              }
              else if ($cfg['UPLOAD_ACTIVE'] && file_exists($cfg['UPLOAD_FOLDER'].'/'.$_FILES['f']['name'][$i])) {
                  $uploadErrors[$j]['name'] = $_FILES['f']['name'][$i];
                  $uploadErrors[$j]['error'] = 'Die Datei existiert bereits.';
                  $j++;
                  $error = true;
              }
              else {
				  if ($cfg['UPLOAD_ACTIVE']) {
                     move_uploaded_file($_FILES['f']['tmp_name'][$i], $cfg['UPLOAD_FOLDER'].'/'.$_FILES['f']['name'][$i]);	
				  }
                  $uploadedFiles[] = $_FILES['f']['name'][$i];
              }
          }
      }

      if ($error) {
          $errorMessage = 'Es sind folgende Fehler beim Versenden des Kontaktformulars aufgetreten:'."\n";
          if (count($uploadErrors) > 0) {
              foreach ($uploadErrors as $err) {
                  $tmp .= '<strong>'.$err['name']."</strong><br/>\n- ".$err['error']."<br/><br/>\n";
              }
              $tmp = "<br/><br/>\n".$tmp;
          }
          $errorMessage .= $tmp.'';
          $fehler['upload'] = $errorMessage;
      }
  }



   if (!isset($fehler))
   {
   $recipient = "xxtestxx43@gmx.de";
   $betreff = "";
   //$mailheaders = "From: \"".stripslashes($_POST["vorname"])." ".stripslashes($_POST["name"])."\" <".$_POST["email"].">\n";
	//$mailheaders .= "Reply-To: <".$_POST["email"].">\n";
	//$mailheaders .= "X-Mailer: PHP/" . phpversion() . "\n";
	$mailheader_betreff = "=?UTF-8?B?".base64_encode($betreff)."?=";
	$mailheaders   = array();
	$mailheaders[] = "MIME-Version: 1.0";
	$mailheaders[] = "Content-type: text/plain; charset=utf-8";
		// ------------------------------------------------------------
		// -------------------- send mail to admin --------------------
		// ------------------------------------------------------------

		// ---- create mail-message for admin
   $mailcontent .= "$dsmsg";
		if(count($uploadedFiles) > 0){
			if($cfg['UPLOAD_ACTIVE']){
				$mailcontent .= 'Es wurden folgende Dateien hochgeladen:'."\n";
				foreach ($uploadedFiles as $filename) {
					$mailcontent .= ' - '.$cfg['DOWNLOAD_URL'].'/'.$cfg['UPLOAD_FOLDER'].'/'.$filename."\n";
				}
			} else {
				$mailcontent .= 'Es wurden folgende Dateien als Attachment angehängt:'."\n";
				foreach ($uploadedFiles as $filename) {
					$mailcontent .= ' - '.$filename."\n";
				}
			}
		}
		if($cfg['DATENSCHUTZ_ERKLAERUNG']) { $mailcontent .= "\n\nDatenschutz: " . $datenschutz . " \n"; }
    
		$mailcontent = strip_tags ($mailcontent);

		// ---- get attachments for admin
		$attachments = array();
		if(!$cfg['UPLOAD_ACTIVE'] && count($uploadedFiles) > 0){
			foreach($uploadedFiles as $tempFilename => $filename) {
				$attachments[$filename] = file_get_contents($tempFilename);
			}
		}

		$success = false;

        // ---- send mail to admin
        {
            $success = sendMyMail($email, $name, $recipient, $betreff, $mailcontent, $attachments);
        }

    	// ------------------------------------------------------------
    	// ------------------- send mail to customer ------------------
    	// ------------------------------------------------------------
    	if(
			$success 
		){

    		// ---- create mail-message for customer
    		
    		
    		$mailcontent  = "Wenn Sie diese E-Mail lesen können, wurde die PHP Funktion mail() erfolgreich auf Ihrem Server getestet. Sie können nun die Datei test.php löschen.\n\n";
   $mailcontent .= "Vervollständigen Sie die Daten in der Datei config.php, um das Kontaktformular (kontakt.php) nutzen zu können. Diese Datei muss mit einem Editor geöffnet werden.\n\nEmpfehlung Windows: https://www.chip.de/downloads/Notepad2-32-Bit_13013323.html\nEmpfehlung MacOS: http://brackets.io\n\n";
$mailcontent .= "Bei Fragen oder Problemen steht Ihnen jederzeit unser Support zur Verfügung.\n\nFAQ Seite: https://www.kontaktformular.com/faq-script-php-kontakt-formular.html\nTutorial Seite: https://www.kontaktformular.com/kontaktformular-erstellen-tutorial.html\n";
    		

    		$mailcontent = strip_tags ($mailcontent);

    		// ---- send mail to customer
            {
                $success = sendMyMail("no-reply@kontaktformular.com", $empfaenger, $email, "Test-Mail", $mailcontent);
            }
		}
		
		// redirect to success-page
		if($success){
    		    echo "<br /><p style='display: flex;justify-content: space-between;align-items: flex-start;margin-left:0px;padding-left:0px;'><span style='font-size:15px;font-family: Arial, sans-serif;'>Das Test-Formular wurde erfolgreich versandt. Sie sollten innerhalb der nächsten Sekunden eine E-Mail erhalten. <br /><br /><a style='font-family: Arial, sans-serif;color:black;text-decoration:underline;' href=http://www.kontaktformular.com/faq-script-php-kontakt-formular.html#keine-mail-erhalten>Keine Mail erhalten? Bitte hier klicken!</a></span></p>";
            }

    		exit;
		}
	}


// clean post
foreach($_POST as $key => $value){
    $_POST[$key] = htmlentities($value, ENT_QUOTES, "UTF-8");
}
?>
<?php




function sendMyMail($fromMail, $fromName, $toMail, $subject, $content, $attachments=array()){

	$boundary = md5(uniqid(time()));
	$eol = PHP_EOL;

	// header
	$header = "From: =?UTF-8?B?".base64_encode(stripslashes($fromName))."?= <".$fromMail.">".$eol;
	$header .= "Reply-To: <".$fromMail.">".$eol;
	$header .= "MIME-Version: 1.0".$eol;
	if(is_array($attachments) && 0<count($attachments)){
		$header .= "Content-Type: multipart/mixed; boundary=\"".$boundary."\"";
	}
	else{
		$header .= "Content-type: text/plain; charset=utf-8";
	}


	// content with attachments
	if(is_array($attachments) && 0<count($attachments)){

		// content
		$message = "--".$boundary.$eol;
		$message .= "Content-type: text/plain; charset=utf-8".$eol;
		$message .= "Content-Transfer-Encoding: 8bit".$eol.$eol;
		$message .= $content.$eol;

		// attachments
		foreach($attachments as $filename=>$filecontent){
			$filecontent = chunk_split(base64_encode($filecontent));
			$message .= "--".$boundary.$eol;
			$message .= "Content-Type: application/octet-stream; name=\"".$filename."\"".$eol;
			$message .= "Content-Transfer-Encoding: base64".$eol;
			$message .= "Content-Disposition: attachment; filename=\"".$filename."\"".$eol.$eol;
			$message .= $filecontent.$eol;
		}
		$message .= "--".$boundary."--";
	}
	// content without attachments
	else{
		$message = $content;
	}

	// subject
	$subject = "=?UTF-8?B?".base64_encode($subject)."?=";

	// send mail
	return mail($toMail, $subject, $message, $header);
}

?>
<!DOCTYPE html>
<html lang="de-DE">
	<head>
		<meta charset="utf-8">
		<meta name="language" content="de"/>
		<meta name="description" content="kontaktformular.com"/>
		<meta name="revisit" content="After 7 days"/>
		<meta name="robots" content="INDEX,FOLLOW"/>
		<title>kontaktformular.com</title>

		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" />
	<!-- Stylesheet -->



<link href='https://fonts.googleapis.com/css?family=Heebo:700' rel='stylesheet' type='text/css'>


<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>














<style type="text/css">
/* import fontawesome */

@import '../fontawesome/css/fontawesome.min.css';
@import '../fontawesome/css/regular.min.css';
@import '../fontawesome/css/solid.min.css';



/* common styles */

* {
				box-sizing: border-box;
}

body {
				margin: 0;
				background-color: #FFFFFF;
				padding-top: 5px;
				padding-bottom: 20px;
				display: flex;
align-items: center;
justify-content: center;

}

body,
textarea,
input,
select,
.senden {
				font-family: Arial, sans-serif;
				font-size: 14px;
}

.kontaktformular {
				width: 600px;
				max-width: 100%;
				padding: 1.2rem;	
				padding-left: 0rem;		
				margin-left:0px;
				padding-top: 22px;
				padding-bottom: 1px;
}



/* style common rows/grid */

.kontaktformular .row {
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
				margin-bottom: 1.3rem;
				width: 100%;
}

.kontaktformular .row .col-sm-4 {
				flex-grow:1;
				flex-basis: 0;
				margin: 0 .75rem;
				position: relative;
}
.kontaktformular .row .col-sm-4:first-child {
	margin-left: 0;
}
.kontaktformular .row .col-sm-4:last-child {
	margin-right: 0;
}

.kontaktformular .row .col-sm-8 {
				width: 100%;
				position: relative;
}



/* style common labels */

.kontaktformular .row .control-label {
				position: absolute;
				margin-top: 0.19rem;  height: 91.1%;
				padding: .63rem 1rem .5rem 1rem;
				color: grey;
				opacity: 0.7;
				
				width: 3rem;
				z-index: 2;
}



/* safari: margin-top for control, select & textarea label, padding-top for mailcopy, dataprotection, fileupload, securitycode & securityquestion icon - start */

body.safari .kontaktformular .row .control-label{
     margin-top: 0.27rem; 
}


body.safari .kontaktformular .row .error .control-label{
     margin-top: 0.27rem; 
}


body.safari .kontaktformular .row .select-label{
     margin-top: 0.27rem; 
}


body.safari .kontaktformular .row .error .select-label{
     margin-top: 0.27rem; 
}


body.safari .kontaktformular .row .textarea-label{
     margin-top: 0.20rem; 
}


body.safari .kontaktformular .row .error .textarea-label{
     margin-top: 0.20rem; 
}


body.safari .kontaktformular .row #mailcopy-icon{
     padding-top: 5px; 
}


body.safari .kontaktformular .row #dataprotection-icon{
     padding-top: 4px; 
}


body.safari .kontaktformular .row #fileupload-icon{
     padding-top: 4px; 
}


body.safari .kontaktformular .row #securitycode-icon{
     margin-top: -5px; 
}


body.safari .kontaktformular .row #securityquestion-icon{
     margin-top: -5px; 
}




/* safari: margin-top for control, select & textarea label, padding-top for mailcopy, dataprotection, fileupload, securitycode & securityquestion icon - end */


#mailcopy-icon{
     padding-top: 9px; 
}


#dataprotection-icon{
     padding-top: 9px; 
}


#fileupload-icon{
     padding-top: 7px; 
}


#securitycode-icon{
     padding-top: 0px; 
}


#securityquestion-icon{
     padding-top: 0px; 
}






/* Regulare icons - padding left for safari and other browsers */

body.safari #caret-down-icon{
     padding-left: 3.5px;  
     padding-top: 1.5px;
}

body.safari #briefcase-icon{
     padding-left: 1.5px; 
}

body.safari #user-icon{
     padding-left: 2.0px; 
}

body.safari #user-icon-position-2{
     padding-left: 2.0px;   
     padding-top: 2px; 
}

body.safari #email-icon{
     padding-left: 1.0px; 
}

body.safari #email-icon-position-2{
     padding-left: 1.0px;  
     padding-top: 2px; 
}

body.safari #phone-icon{
     padding-left: 0.5px; 
}

body.safari #phone-icon-position-2{
     padding-left: 0.5px; 
     padding-top: 2px; 
}

body.safari #home-icon{
     padding-left: 0.5px; 
}

body.safari #home-icon-position-2{
     padding-left: 0.5px; 
     padding-top: 2px; 
}

body.safari #subject-icon{
     padding-left: 1.5px; 
}

body.safari #message-icon{
     padding-left: 0.5px; 
}

#caret-down-icon{
     padding-left: 3px;
     padding-top: 1.5px; 
}

#briefcase-icon{
     padding-left: 1px; 
}

#user-icon{
     padding-left: 1.5px; 
}

#user-icon-position-2{
     padding-left: 1.5px;    
}

#email-icon{
     padding-left: 0.5px; 
}

#email-icon-position-2{
     padding-left: 0.5px; 
}

#phone-icon{
     padding-left: 0px; 
}

#phone-icon-position-2{
     padding-left: 0px; 
}

#home-icon{
     padding-left: 0px; 
}

#home-icon-position-2{
     padding-left: 0px; 
}

#subject-icon{
     padding-left: 1.0px; 
}

#message-icon{
     padding-left: 0px; 
}






/* style common fields */
.kontaktformular .row input,
.kontaktformular .row textarea {
				-webkit-appearance: none;
				-moz-appearance: none;
				appearance: none;
}
.kontaktformular .row .field {
				display: block;	
				font-size: 14px;
				width: 100%;
				padding: .74rem .8rem .45rem 3.8rem;
				color: #555;
			  
			  border: 1px solid #CCC;
				border-radius: .25rem;
				
				
				
				      
  -moz-border-radius: .25rem;
  -webkit-border-radius: .25rem;
  border-top: 1px solid #BDBDBD;
  border-left: 1px solid #BDBDBD;
  border-right: 1px solid #BDBDBD;
  border-bottom: 1px solid #BDBDBD; 
        box-shadow: 0 0 1px rgba(0,0,0, .4);
				      
				      
				      
				transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
				-webkit-appearance: none;
				-moz-appearance: none;
				appearance: none;
}

.kontaktformular .row .field:focus,
.kontaktformular .row input[type="checkbox"]:focus {
				border-color: #66afe9 !important;
				outline: 0 !important;
				box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 0.5rem rgba(102, 175, 233, 0.6) !important;
}



/* style active / inactive label */

.kontaktformular .row .not-empty-field .control-label i{
	color: #424242;
}


body.safari .kontaktformular .row .not-empty-field .control-label i{
	color: #424242 !important;
}


.kontaktformular .row .active-field .control-label i{
	color: #424242;
}


body.safari .kontaktformular .row .active-field .control-label i{
	color: #424242 !important;
}



/* style textarea */

.kontaktformular .row .textarea-label{
				 margin-top:0.25rem;
				height: 97.1%;
				padding: 0.6rem 1rem 5.1rem 1rem;  									
}



.kontaktformular .row textarea {
				 height: 1.7rem;
				
}


/* style selectbox */

.kontaktformular .row .select-label{
				height: 90.9%;
				padding: .63rem 1rem .5rem 1rem;
		
}



/* style input, select and textarea with border-right.png - start */

#border-right {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}

#border-right3 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right4 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right5 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right6 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right7 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right8 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right9 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right10 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right11 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right12 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}
#border-right13 {
					background-image: url('../img/border-right.png');
				background-position: 2.85rem center;
				-webkit-text-size-adjust:none; 
				background-repeat: no-repeat;
				
}

/* style input, select and textarea with border-right.png - end */




/* style rows with complex contents  */

.kontaktformular .captcha-row,
.kontaktformular .question-row,
.kontaktformular .checkbox-row,
.kontaktformular .upload-row {
				display: block;
				font-size: 14px;
				width: 100%;
				color: #555555;
				border: 1px solid #BDBDBD;
				border-radius: 4px;
				transition: border-color ease-in-out .15s;
				padding-right: 1rem;
				box-shadow: 0 0 1px rgba(0,0,0, .4);
}
.kontaktformular .captcha-row .control-label,
.kontaktformular .question-row .control-label,
.kontaktformular .upload-row .control-label,
.kontaktformular .checkbox-row .control-label{
				height: 100%;
				margin-top: 0; 
}
.kontaktformular .captcha-row > div,
.kontaktformular .question-row > div,
.kontaktformular .checkbox-row > div{
				padding-bottom: .15rem;
}
.kontaktformular .captcha-row div div,
.kontaktformular .question-row div div{
				width: 100%;
				padding: .75rem 0 .75rem 60px;
}



/* style upload-fields  */

.kontaktformular .row input[type="file"] {
				width: calc(100% - 60px);
				height: 30px;
				margin: .2rem 0 .2rem 60px;
}
.kontaktformular .row .control-label + input[type="file"] {
				margin-top: .75rem;
}
.kontaktformular .row input[type="file"]:last-child {
				margin-bottom: .25rem;
}



/* style security-fields  */

.kontaktformular .captcha-row .field,
.kontaktformular .question-row .field{
				width: calc(100% - 60px);
				margin: .2rem 0 .2rem 60px;
				padding-left: .8rem;
}
.kontaktformular .row#answer .control-label {
				align-self: flex-start;
}



/* style checkbox-row  */

.kontaktformular .checkbox-row .checkbox-inline{
				display: block;
				padding: .7rem 0 .31rem 60px;
}

.kontaktformular .checkbox-row .checkbox-inline a:hover,
.kontaktformular .checkbox-row .checkbox-inline a:focus {
				color: #0025e2;
				text-decoration: underline;
}

.kontaktformular .checkbox-row .checkbox-inline a,
.kontaktformular .checkbox-row .checkbox-inline span {
				color: #0020c1;
				text-decoration: none;
				line-height: 24px;
				padding-left: 10px;
				
}
.kontaktformular .checkbox-row .checkbox-inline span{
				color: inherit;
}
.kontaktformular .row input[type="checkbox"] {
				height: 22px;
				width: 22px;
				border: 1px solid #CCC;
				border-radius: .25rem;
				transition: border-color ease-in-out .15s;	
				display: block;
				float: left;
				-webkit-appearance: none;
				-moz-appearance: none;
				appearance: none;
				cursor: pointer;
				margin-left: 0;
				
				
				
				
				  -moz-border-radius: .25rem;
  -webkit-border-radius: .25rem;
  border-top: 1px solid #BDBDBD;
  border-left: 1px solid #BDBDBD;
  border-right: 1px solid #BDBDBD;
  border-bottom: 1px solid #BDBDBD; 
        box-shadow: 0 0 1px rgba(0,0,0, .4);
				
				
}
.kontaktformular .row input:checked {
				background: url(../img/check-solid.svg) no-repeat center center;
				background-size: 75%;
}



/* style submit-button  */






.kontaktformular .row .senden {
				width: 100%;
				font-size: 16px;
				font-weight: bold;
				height: 2.5rem;
				margin-top: 15px;
				padding: .5rem .75rem;
				color: white;
				background-color: #337ab7;
				border: 1px solid transparent;
				border-color: #2e6da4;
				border-radius: 4px;
}

.kontaktformular .row .senden:hover {
				background-color: #286090;
				border-color: #204d74;
				cursor: pointer;
}





/* style select-box for placeholders */

.kontaktformular .row select {
                background-color: #fff;                
}

.kontaktformular .row ::placeholder{
				color: grey;
				opacity: 0.7;
				}
				
				
.kontaktformular .row select.unselected{
				color: #A6A6A6;
			
	border: 1px solid #CCC;
	border-radius: .25rem;
	-moz-border-radius: .25rem;
  -webkit-border-radius: .25rem;
  border-top: 1px solid #BDBDBD;
  border-left: 1px solid #BDBDBD;
  border-right: 1px solid #BDBDBD;
  border-bottom: 1px solid #BDBDBD; 
    box-shadow: 0 0 1px rgba(0,0,0, .4);
    
				transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;			
}


.kontaktformular .row select.field{
	-moz-appearance: none;
	-webkit-appearance: none;
	appearance: none;
	z-index: 1;
}
.kontaktformular .row select.field option[value=""][disabled] {
				display: none;
}
.kontaktformular .row select.field option {
				color: #555555;
}
.kontaktformular .row select.field option[value=""] {
				color: rgba(0,0,0,0.4);
}



/* style errors */

.kontaktformular .row .error .select-label{
				height: 66%;
				padding: .63rem 1rem .5rem 1rem; 
			color: #db0007;
				border-color: #db0007;    
}





.kontaktformular .row .error .control-label{
				color: #db0007;
				border-color: #db0007;
				margin-top: 0.19rem;
				height: 65.1%;
				padding: .63rem 1rem .5rem 1rem;			
}




.kontaktformular .row .error .textarea-label{
			color: #db0007;
			border-color: #db0007;
      height: 84.6%;		
       margin-top:0.25rem;
       padding: 0.6rem 1rem 5.1rem 1rem;  
}









.kontaktformular .row .error .field,
.kontaktformular .row .error .checkbox-inline input,
.kontaktformular.kontaktformular-validate .row .field:invalid,
.kontaktformular.kontaktformular-validate .row .checkbox-inline input:invalid{	/* style invalid fields only if user wants to send the form (integrated via js) */
				background-color: #ffeaec;
				border-color: #eac0c5;
}
.kontaktformular .row .field:invalid,
.kontaktformular .row .checkbox-inline input:invalid{		/* remove browser-style for invalid fields */
				outline: none;
				box-shadow:none;
}
.kontaktformular .row .field:focus:valid,
.kontaktformular .row .checkbox-inline input:focus:valid{
				background-color: #FFFFFF;
				border-color: #d9e8d5;
				outline: none;
				box-shadow:none;
}
.kontaktformular .row .error ::placeholder{
				color: rgba(219, 0, 7, 0.6);
}

.kontaktformular .row .error select.unselected
{
				color: rgba(219, 0, 7, 0.4);
}

.kontaktformular .row .errormsg{
				color: #db0007;
				font-size: .75rem;
}
.kontaktformular .captcha-row.error_container,
.kontaktformular .question-row.error_container,
.kontaktformular .checkbox-row.error_container{
	margin-bottom: 2.7rem;				
					
}
.kontaktformular .captcha-row .errormsg,
.kontaktformular .question-row .errormsg{
					display: block;
				position: absolute;
				left: 0;
				bottom: -46px;
				height: 40px;
}
.kontaktformular .checkbox-row .errormsg{
				display: block;
				position: absolute;
				left: 0;
				bottom: -46px;
				height: 40px;
}










.kontaktformular .captcha-row.error_container .control-label,
.kontaktformular .question-row.error_container .control-label,
.kontaktformular .upload-row.error_container .control-label,
.kontaktformular .checkbox-row.error_container .control-label{
				height: 100%;
				margin-top: 0; 
}













/* style for mobile */

@media (max-width: 655px) {
				
				.kontaktformular {
								padding: 1px 1rem 1px 1rem;
								/* box-shadow: none; */
								margin-left:15px;
								margin-top:0px;
								margin-right:15px;
								width: auto;
				}
				.kontaktformular .row {
								display: block;
								margin-top: 1rem;
				}
				.kontaktformular .row .col-sm-4{
								flex-grow:0;
								flex-basis: 0;
								margin: 0;
				}
				.kontaktformular .row .col-sm-4,
				.kontaktformular .row .col-sm-8 {
								margin-top: 1.5rem;
				}
				.kontaktformular .captcha-row .col-sm-8,
				.kontaktformular .question-row .col-sm-8,
				.kontaktformular .upload-row .col-sm-8,
				.kontaktformular .checkbox-row .col-sm-8{
								margin-top: 0;
				}
				
				
				
				
				.kontaktformular .row .control-label {
				margin-top: 0.16rem; }
				.kontaktformular .row .error .control-label{
				margin-top: 0.16rem; }
				
				.kontaktformular .row .textarea-label{
				 margin-top:0.21rem; }
        .kontaktformular .row .error .textarea-label{
				 margin-top:0.21rem; }


.kontaktformular .row .senden {
				width: 100%;
				font-size: 16px;
				font-weight: bold;
				height: 2.5rem;
				margin-top: 6px;
				padding: .5rem .75rem;
				color: white;
				background-color: #337ab7;
				border: 1px solid transparent;
				border-color: #2e6da4;
				border-radius: 4px;
}
#mailcopy-icon{
     padding-top: 6px; 
}


#dataprotection-icon{
     padding-top: 7px; 
}


#fileupload-icon{
     padding-top: 4px; 
}


#securitycode-icon{
     padding-top: 0px; 
}


#securityquestion-icon{
     padding-top: 0px; 
}



/* safari iOS: margin-top for control & select label, padding-top for mailcopy & dataprotection icon - start */

body.safari .kontaktformular .row .control-label{
     margin-top: 0.19rem; 
}


body.safari .kontaktformular .row .error .control-label{
     margin-top: 0.19rem; 
}


body.safari .kontaktformular .row .select-label{
     margin-top: 0.15rem; 
}


body.safari .kontaktformular .row .error .select-label{
     margin-top: 0.15rem; 
}


body.safari .kontaktformular .row #mailcopy-icon{
     padding-top: 6px; 
}


body.safari .kontaktformular .row #dataprotection-icon{
     padding-top: 5px; 
}


body.safari #phone-icon-position-2{
     padding-left: 0.5px; 
     padding-top: 0px; 
}



body.safari #home-icon-position-2{
     padding-left: 0.5px; 
     padding-top: 0px; 
}


body.safari #user-icon-position-2{
     padding-left: 2.0px;   
     padding-top: 0px; 
}



body.safari #email-icon-position-2{
     padding-left: 1.0px;  
     padding-top: 2px; 
}




/* safari iOS: margin-top for control & select label, padding-top for mailcopy & dataprotection icon - end */




}



/* style copyright */

.copyright {
	 color: #000000;
	 font-size: 13px;
}

</style>

</head>





<body>

	<div>
		<form id="kontaktformular" class="kontaktformular" action="<?php echo $_SERVER['PHP_SELF'];?>" method="post" enctype="multipart/form-data">


<script>
if (navigator.userAgent.search("Safari") >= 0 && navigator.userAgent.search("Chrome") < 0) 
{
   document.getElementsByTagName("BODY")[0].className += " safari";
}
	</script>









		

		 


			<div class="row" id="send">
				<div class="col-sm-8">
					
						<p style="line-height:21px;">Nutzen Sie dieses Formular, um die PHP Funktion mail() auf Ihrem Server zu testen.<br /><br />Tragen Sie Ihre E-Mail Adresse ein und klicken Sie auf <b>Senden</b>. Innerhalb von wenigen Sekunden sollten Sie eine Test-Mail erhalten. Diese Datei kann danach gelöscht werden.</p>
				
					
						</div>
			</div>
				
			
			
			<div class="row">
			 
				
				
					<div class="col-sm-8 <?php if ($fehler["email"] != "") { echo 'error'; } ?> <?php echo (isset($_POST['email']) && ''!=$_POST['email'] ? 'not-empty-field ' : ''); ?>">
					
					<input style="padding-left:20px;" <?php if($cfg['HTML5_FEHLERMELDUNGEN']) { ?> required style="box-shadow: 0 0 1px rgba(0,0,0, .4);" <?php }else{ ?> onchange="checkField(this)" <?php } ?> aria-label="E-Mail" type="<?php if($cfg['HTML5_FEHLERMELDUNGEN']) { echo 'email'; }else{ echo 'text'; } ?>" name="email" class="field" placeholder="E-Mail *" value="<?php echo $_POST[email]; ?>" maxlength="<?php echo $zeichenlaenge_email; ?>" id="border-right2" onclick="setActive(this);" onfocus="setActive(this);" />
					<?php if ($fehler["email"] != "") { echo $fehler["email"]; } ?>
				</div>
				
			</div>
			
					
					<div class="row" id="send">
				<div class="col-sm-8">
			<input type="submit" class="senden" name="kf-km" value="Senden"  />
				
		
				</div>
			</div>
			
		
			
			
			
			
			
			
			
		  
		  
		  
		
					
					
		</form>
	</div>
</body>
</html>
