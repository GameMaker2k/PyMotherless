<?php
@ob_start();
if(!isset($_GET['act'])) { $_GET['act'] = "url"; }
if($_GET['act']=="download") { $_GET['act'] = "get"; }
if($_GET['act']=="view") { $_GET['act'] = "get"; }
if($_GET['act']=="geturl") { $_GET['act'] = "url"; }
if($_GET['act']=="viewurl") { $_GET['act'] = "url"; }
if($_GET['act']=="redir") { $_GET['act'] = "goto"; }
if($_GET['act']=="redirect") { $_GET['act'] = "goto"; }
if($_GET['act']=="location") { $_GET['act'] = "goto"; }
if($_GET['act']=="gourl") { $_GET['act'] = "goto"; }
if($_GET['act']=="gotourl") { $_GET['act'] = "goto"; }
if($_GET['act']=="url") {
	if(isset($_GET['fmt'])) { $_GET['fmt'] = 18; }
	header("Content-type: text/plain; charset=utf-8");
	exec("/usr/bin/youtube-dl --get-url --format ".$_GET['fmt']." https://www.youtube.com/watch?v=".$_GET['v'], $get_value); 
	$get_value = implode($get_value); 
	$get_value = trim($get_value);
	echo $get_value; }
if($_GET['act']=="goto") {
	if(isset($_GET['fmt'])) { $_GET['fmt'] = 18; }
	header("Content-type: text/plain; charset=utf-8");
	exec("/usr/bin/youtube-dl --get-url --format ".$_GET['fmt']." https://www.youtube.com/watch?v=".$_GET['v'], $get_value); 
	$get_value = implode($get_value); 
	$get_value = trim($get_value);
	header("Location: ".$get_value);
	echo $get_value; }
if($_GET['act']=="get") { 
	exec("/usr/bin/youtube-dl --dump-user-agent", $get_ua_value);
	$get_ua_value = implode($get_ua_value); 
	$get_ua_value = trim($get_ua_value);
	$default_opts = array(
	  'http'=>array(
	    'method'=>"GET",
	    'header'=>"User-Agent: ".$get_ua_value."\r\n".
	              "Referer: https://www.youtube.com/watch?fmt=".$_GET['fmt']."v=".$_GET['v']."\r\n"
	  )
	);
	$default = stream_context_set_default($default_opts);
	if(isset($_GET['fmt'])) { $_GET['fmt'] = 18; }
	exec("/usr/bin/youtube-dl --get-filename -f ".$_GET['fmt']." https://www.youtube.com/watch?v=".$_GET['v'], $get_fname); 
	$get_fname = implode($get_fname); 
	$get_fname = trim($get_fname);
	header('Content-Disposition: attachment; filename="'.$get_fname.'"');
	exec("/usr/bin/youtube-dl --get-url --format ".$_GET['fmt']." https://www.youtube.com/watch?v=".$_GET['v'], $get_value); 
	$get_value = implode($get_value); 
	$get_value = trim($get_value);
	$getvidheaders = get_headers($get_value, 1);
	header("Content-Type: ".$getvidheaders['Content-Type']);
	echo file_get_contents($get_value); }
?>
