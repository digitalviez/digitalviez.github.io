<?php
header('Content-type: text/html; charset=utf-8');
$data = array(
	0 => array("Welche Form hat ein Ball?","rund"),
	1 => array("Wie viele Stunden hat ein Tag?",24),
	2 => array("Wie viele Tage hat eine Woche?",7),
	3 => array("Wie viele Sekunden hat eine Minute?",60),
	4 => array("Was ergibt 5 mal 3?",15),
	5 => array("Was ergibt 9 minus 2?",7),
	6 => array("Was ergibt 12 plus 1?",13),
	7 => array("Was ergibt 50 geteilt durch 10?",5)
);

class AntiSpam{

	public static function getAnswerById($id){
		global $data;
		
		return $data[$id][1];
	}	
	
	public static function getRandomQuestion(){
		global $data;
		
		$rand = rand(0,count($data)-1);
		return array($rand,$data[$rand][0]);
	}
	
}

?>