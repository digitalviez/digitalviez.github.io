<?php

$empfaenger = "digitalviez@gmx.de";  // Bitte tragen Sie hier Ihre E-Mail Adresse ein. (zwischen den Anführungszeichen)

$ihrname = "Digital Viez";  // Bitte tragen Sie hier Ihren Namen ein. (zwischen den Anführungszeichen) Dieser erscheint als Absender in der Danke Mail.

$cfg['DATENSCHUTZ_ERKLAERUNG'] = 0;  //  0 = Ohne Datenschutzerklärung    1 = Mit Datenschutzerklärung

$datenschutzerklaerung = "datenschutz.php";  //  Pfad zur Datenschutzerklärung. "datenschutz.php" kann durch einen Link/URL ersetzt werden. (muss mit "http://www." anfangen!)
    
$danke = "danke.php";  // Pfad zur Danke Seite. "danke.php" kann durch einen Link/URL ersetzt werden. (muss mit "http://www." anfangen!) Die entsprechende Danke Seite kann mit dem nachfolgenden Script auch außerhalb des iFrame angezeigt werden: http://www.kontaktformular.com/faq-script-php-kontakt-formular.html#Danke-Seite-außerhalb-vom-IFrame-anzeigen


    

// Spamschutz - Einstellungen // (siehe: https://www.kontaktformular.com/kontaktformular-spamschutz-captcha-badword-filter-zeitsperre-honeypot.html)

$cfg['Sicherheitscode'] = 0;  //  0 = Ohne Sicherheitscode   1 = Mit Sicherheitscode

$cfg['Sicherheitsfrage'] = 0;  //  0 = Ohne Sicherheitsfrage   1 = Mit Sicherheitsfrage

$cfg['Honeypot'] = 0;  //  0 = Ohne Honeypot   1 = Mit Honeypot 
	
$cfg['Zeitsperre'] = 0;  //  Mindest-Anzahl der Sekunden zwischen Anzeigen und Senden des Formulars  	0 = Ohne Zeitsperre
	
$cfg['Klick-Check'] = 0;  //  0 = Ohne Klick-Check   1 = Mit Klick-Check

$cfg['Links'] = 100;  //  Anzahl der maximal erlaubten Links (0 = keine Links erlaubt)
	
$cfg['Badwordfilter'] = 'sex%, pussy%, porn%, %.ru, %.ru/%';  //  Begriffe für den Bad Word Filter   0 oder leer = Ohne Bad Word Filter

// Funktionsweise des Bad Word Filters:
// badword = matcht, wenn das Bad Word als ganzes Wort enthalten ist   
// badword% = matcht, wenn das Bad Word enthalten ist UND wenn ein Wort mit dem Bad Word beginnt   
// %badword = matcht, wenn das Bad Word enthalten ist UND wenn ein Wort mit dem Bad Word endet   
// %badword% = matcht, wenn das Bad Word enthalten ist UND wenn ein Wort das Bad Word enthält
	
$cfg['Badwordfields'] = 'name, email, nachricht';  //   Die Namen der Felder, die bei dem Bad Word Filter geprüft werden sollen - Groß- und Kleinschreibung beachten!
	



// Weitere Einstellungen //

$cfg['Kopie_senden'] = 1;    // 0 = keine Kopie senden   1 = Kopie nur bei Zustimmung senden   2 = immer eine Kopie senden (ungefragt)

$cfg['HTML5_FEHLERMELDUNGEN'] = 1;  //  0 = Ohne HTML5 Fehlermeldungen    1 = Mit HTML5 Fehlermeldungen




// Die SMTP Funktion kann im nachfolgenden Abschnitt aktiviert werden. Wichtig: Auf Ihrem Server muss mind. PHP 7.2 oder höher installiert sein. Die aktuelle PHP Version können Sie prüfen, indem Sie die Datei phpinfo.php im Browser aufrufen. //

$smtp = array();

$smtp['enabled'] = 0; // Soll das Kontaktformular E-Mails über einen SMTP Server versenden? Ja = 1, Nein = 0

$smtp['host'] = 'smtp.example.de'; // Der Host, unter welchem der SMTP Server erreichbar ist. (bspw. smtp.gmail.com)
   
$smtp['user'] = 'name'; // Der Benutzername, mit welchem Sie sich bei Ihrem SMTP Server authentifizieren. (kann u.U. die oben genannte E-Mail Adresse sein!)

$smtp['password'] = 'password'; // Das Passwort, mit welchem Sie sich bei Ihrem SMTP Server authentifizieren.

$smtp['encryption'] = 'tls'; // Die Art der Verschlüsselung, die bei der Verbindung mit Ihrem SMTP Server verwendet wird: '', 'ssl' oder 'tls'

$smtp['port'] = 587; // Der TCP Port, unter welchem Ihr SMTP Server erreichbar ist.

$smtp['debug'] = 0; // Das Debuglevel (0 - 4)
    
    
    
    
// Einstellungen für Upload-Funktion

$cfg['NUM_ATTACHMENT_FIELDS'] = 0;	// Anzahl der Upload-Felder

$cfg['UPLOAD_ACTIVE'] = 1;		// 1 = Dateianhang wird via Mail gesendet (Standard) 2 = Dateianhang wird in ein Verzeichnis hochgeladen. (ergänzen Sie die unten stehenden Angaben)

$cfg['WHITELIST_EXT'] = 'pdf|png|jpg';	// Erlaubte Dateiendungen - Beispiel: pdf|png|jpg

$cfg['MAX_FILE_SIZE'] = 1024;		// Maximale Größe von einer Datei in KB. (diese Option ist abhängig von den PHP und Server Einstellungen)

$cfg['MAX_ATTACHMENT_SIZE'] = 2048;	// Maximale Größe von mehreren Dateien in KB. (bei mehr als 1 Uploadfeld)

$cfg['BLACKLIST_IP'] = array('12.345.67.89');	// Gesperrte IPs - Beispiel: array('192.168.1.2', '192.168.2.4');


// Vervollständigen Sie die nachfolgenden Angaben, sofern der Dateianhang in ein Verzeichnis hochgeladen werden soll

$cfg['UPLOAD_FOLDER'] = 'upload';	// Das Verzeichnis "upload" muss erstellt werden. Dieses benötigt Schreibrechte. (chmod 777)

$cfg['DOWNLOAD_URL'] = 'https://www.ihre-website.de/kontaktformular';	// URL zum Kontaktformular (ohne / am Ende!)
	
    
    
        
// Maximale Zeichenlänge der Felder definieren //

$zeichenlaenge_firma = "50";  // Maximale Zeichen - Feld "Firma" (zwischen den Anführungszeichen)

$zeichenlaenge_vorname = "50"; // Maximale Zeichen - Feld "Vorname" (zwischen den Anführungszeichen)

$zeichenlaenge_name = "50"; // Maximale Zeichen - Feld "Nachname" (zwischen den Anführungszeichen)

$zeichenlaenge_email = "50"; // Maximale Zeichen - Feld "E-Mail" (zwischen den Anführungszeichen)

$zeichenlaenge_telefon = "50"; // Maximale Zeichen - Feld "Telefon" (zwischen den Anführungszeichen)

$zeichenlaenge_betreff = "50"; // Maximale Zeichen - Feld "Betreff" (zwischen den Anführungszeichen)

?> 