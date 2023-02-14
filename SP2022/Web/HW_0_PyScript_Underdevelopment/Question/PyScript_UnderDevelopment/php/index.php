<?php
	if(!isset($_FILES["file"]))
		highlight_file(__file__) && die();
	
	$node = @`node {$_FILES["file"]["tmp_name"]} 2>&1`;
	$python = @`python3 {$_FILES["file"]["tmp_name"]} 2>&1`;
	if($node  === $python)
		echo 'Here is your Flag: '.$flag;
	else
		echo 'Fail :(';
?>


