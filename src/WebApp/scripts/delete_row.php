<?php

$object_id = $_POST['delete_id'];

// Connect to the database
$dbconn = pg_connect("host=pgteach port=5432 dbname=s1764997 user=s1764997 password=password sslmode=disable");

if ($object_id) {
    $sql = "DELETE FROM collected_data WHERE object_id='$object_id' ";
    $result = pg_query($dbconn, $sql);

    pg_close($dbconn);
} else {
    echo "Error occured. No data received at the server.";
}
?>