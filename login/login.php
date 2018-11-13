<?php 
session_start();

include 'config.php';
 
$username = ($_POST['username']);
$password = ($_POST['password']);
echo $password;
 
$query = mysqli_query($link, "select * from admin where username='$username' AND password='$password'");
$cek = mysqli_num_rows($query);
//echo $cek;

if($cek > 0){
	$_SESSION['username'] = $username;
	$_SESSION['status'] = "login";
	header("location:admin/index.php");
}else{
	header("location:index.php?pesan=gagal");
}
?>
