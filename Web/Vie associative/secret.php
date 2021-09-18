<?php

if(isset($_REQUEST['secret']) && !empty($_REQUEST['secret'])){

	$con = new mysqli('mysql_database','hackademint','hs5gTyxdTp5gUAqQ', 'secrets_database');
	if ($con->connect_errno) {
	    printf("Échec de la connexion : %s\n", $con->connect_error);
	    die();
	}
	$latest_id_query = 'SELECT id FROM secrets ORDER BY id DESC LIMIT 1';
	$res_id = $con->query($latest_id_query);	
	
	$id = (int)$res_id->fetch_row()[0];	

	$query = 'INSERT INTO secrets (id, secret) VALUES ';
	$parts = array();

	foreach($_REQUEST['secret'] AS $index=>$value){
		if(!empty($value)){
			$parts[]=" (". strval(1+$id) ." + {$index}, '".$con->real_escape_string($value)."')";
			
		}
	}

	$query .= implode(", ", $parts);
	$res_secret = $con->query($query);
	echo 'Thanks for telling me your secret(s) !';

	mysqli_close($con);
} else {

	header('Location: /');
	die();


}

?>
