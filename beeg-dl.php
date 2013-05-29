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
$default_opts = array(
  'http'=>array(
    'method'=>"GET",
    'header'=>"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0\r\n".
              "Referer: http://beeg.com/".$_GET['v']."\r\n"
  )
);
$default = stream_context_set_default($default_opts);
if($_GET['act']=="url") {
	header("Content-type: text/plain; charset=utf-8");
	$get_value = file_get_contents("http://beeg.com/".$_GET['v']);
	$preg_grep_1 = preg_quote("'file': '");
	$preg_grep_2 = preg_quote("',");
	preg_match("/".$preg_grep_1."(.*)".$preg_grep_2."/", $get_value, $get_value_matches);
	$get_value = $get_value_matches[1]."?start=0";
	$get_value = trim($get_value);
	echo $get_value; }
if($_GET['act']=="goto") {
	header("Content-type: text/plain; charset=utf-8");
	$get_value = file_get_contents("http://beeg.com/".$_GET['v']);
	$preg_grep_1 = preg_quote("'file': '");
	$preg_grep_2 = preg_quote("',");
	preg_match("/".$preg_grep_1."(.*)".$preg_grep_2."/", $get_value, $get_value_matches);
	$get_value = $get_value_matches[1]."?start=0";
	$get_value = trim($get_value);
	header("Location: ".$get_value);
	echo $get_value; }
if($_GET['act']=="get") { 
	$get_value = file_get_contents("http://beeg.com/".$_GET['v']);
	$preg_grep_1 = preg_quote("'file': '");
	$preg_grep_2 = preg_quote("',");
	preg_match("/".$preg_grep_1."(.*)".$preg_grep_2."/", $get_value, $get_value_matches);
	$get_value = $get_value_matches[1]."?start=0";
	$get_value = trim($get_value);
	$getvidheaders = get_headers($get_value, 1);
	header("Content-Type: ".$getvidheaders['Content-Type']);
	echo file_get_contents($get_value); }
?>
