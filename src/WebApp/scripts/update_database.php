<?php
//
// On a given AJAX POST request updates the database
//
$object_id = $_POST['object_id'];
$object_type = $_POST['object_type'];

// Connect to the database
$dbconn = pg_connect("host=pgteach port=5432 dbname=s1764997 user=s1764997 password=password sslmode=disable");

if ($object_id) {
    // Update it with collected data
    $result = pg_query($dbconn, "UPDATE collected_data SET object_type='$object_type' WHERE object_id='$object_id';");    
    
    pg_close($dbconn);
    echo "success";
} else {
    echo "failure";
}
?>