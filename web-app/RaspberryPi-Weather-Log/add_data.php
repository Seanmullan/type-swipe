<?php
    // Connect to MySQL
    include("connect.php");

    // Prepare the SQL statement
      date_default_timezone_set('Europe/Athens');
     $dateS = date('m/d/Y h:i:s', time());
    echo $dateS;
    $SQL = "INSERT INTO yourdatabasename.data (date,temperature,humidity,pressure) VALUES ('$dateS','".$_GET["temp"]."','".$_GET["hum"]."','".$_GET["pr"]."')";     

    // Execute SQL statement
    mysql_query($SQL);

    // Go to the review_data.php (optional)
    header("Location: index.php");
?>