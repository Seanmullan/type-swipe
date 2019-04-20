<?php
    $data = $_POST['highest_id'];
    if ($data) {
        $db_connection = pg_connect ("host=pgteach dbname=s1764997 user=s1764997 password=password sslmode=disable");
        $result = pg_query($db_connection,"SELECT * FROM collected_data WHERE object_id>'$data' ORDER BY object_id DESC");
        $ind = 0;
    
    
        while ($row = pg_fetch_row($result)) {
            ?>
            <li data-obj_id="<?php echo $row[0] ?>" data-obj_type="<?php echo $row[3] ?>"
                data-obj_classification="<?php echo $row[1] ?>" data-used_for_training="<?php echo $row[5] ?>"
                <?php if($row[5] == 0) { ?> data-delete_button="true"  <?php } ?> 
                data-bin_type="<?php echo $row[2] ?>" data-object_weight="<?php echo $row[6] ?>" data-time_to_swipe="<?php echo $row[7] ?>"
                style="display:none;" ></li>
            
            <?php
        }
    } else {
        echo "PHP error";
    }

    
?>
