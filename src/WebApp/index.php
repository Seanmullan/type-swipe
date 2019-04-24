<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
    <meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' name='viewport'/>
    <meta name="viewport" content="width=device-width"/>

    <!-- Fonts -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=Grand+Hotel' rel='stylesheet' type='text/css'>
    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <!-- AdminLTE -->
    <!-- Bootstrap 3.3.7 -->
    <link rel="stylesheet" href="AdminLTE/bower_components/bootstrap/dist/css/bootstrap.min.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="AdminLTE/bower_components/font-awesome/css/font-awesome.min.css">
    <!-- Ionicons -->
    <link rel="stylesheet" href="AdminLTE/bower_components/Ionicons/css/ionicons.min.css">
    <!-- DataTables -->
    <link rel="stylesheet" href="AdminLTE/bower_components/datatables.net-bs/css/dataTables.bootstrap.min.css">
    <!-- Theme style -->
    <link rel="stylesheet" href="AdminLTE/dist/css/AdminLTE.min.css">
    <!-- AdminLTE Skins. Choose a skin from the css/skins
        folder instead of downloading all of them to reduce the load. -->
    <link rel="stylesheet" href="AdminLTE/dist/css/skins/_all-skins.min.css">
    <!-- bootstrap slider -->
    <link rel="stylesheet" href="AdminLTE/plugins/bootstrap-slider/slider.css">
    
    <!-- My css document -->
    <link rel="stylesheet" href="css/style.css">
    
    <title>Type Swipe</title>
</head>

<body>
    <?php
        $db_connection = pg_connect ("host=pgteach dbname=s1764997 user=s1764997 password=password sslmode=disable");
    ?>
    <ul id="hidden_list">
        <?php
            $result = pg_query($db_connection,"SELECT * FROM collected_data ORDER BY object_id DESC");
            while ($row = pg_fetch_row($result)) {
        ?>
            <li data-obj_id="<?php echo $row[0] ?>" data-obj_type="<?php echo $row[3] ?>"
            data-obj_classification="<?php echo $row[1] ?>" data-used_for_training="<?php echo $row[5] ?>"
            <?php if($row[5] == 0) { ?> data-delete_button="true"  <?php } ?> 
            data-bin_type="<?php echo $row[2] ?>" data-object_weight="<?php echo $row[6] ?>" data-time_to_swipe="<?php echo $row[7] ?>"
            style="display:none;" ></li>
        <?php 
            } 
        ?>
    </ul>
    <ul id="update_list"></ul>
    
    <article class="row">
        <section class="col-sm-12 content">
            <header class="main-header">
                <h1>
                    <span class="main-header__headline">Type Swipe</span>
                    <small class="main-header__small-headline"></small>
                </h1>
            </header>
            
            <article class="row">
                <section class="col-sm-6 section zero-padding">
                    <div class="box box-solid box-limited-width">
                        <div class="box-header">
                            <span class="box-title">
                                Motors control
                                <span id="message_connected" name="connect_state" data-value="Connect">Connection failure</span>
                            </span>
                            <form id="control_form" method="POST" action="http://jigglypuff" >
                                <input type="submit" class="btn btn-lg btn-success" name="state" value="Start" id="control_button">
                            </form>
                        </div>
                    </div>
                </section>
                <section id="classification_accuracies"></section>
            </article>

            <article id="inner_row" class="row">
                <section class="col-sm-6 content">
                    <div class="box box-primary left">
                        <div class="box-header box-with-right-margin">
                            <span class="box-title">System Error Breakdown</span>
                        </div>
                        <div class="box-body">
                            <span>Errors displayed below account altogether for 8% of measurements that were taken.</span>
                            <div class="nav-tabs-custom">
                                <canvas id="pieChart_breakdown"></canvas>
                            </div>
                            <div>
                                <span id="obj_too_big_badge"></span><span id="obj_too_big_text"></span>
                                <span id="obj_too_heavy_badge"></span><span id="obj_too_heavy_text"></span>
                                <span id="sorting_arm_badge"></span><span id="sorting_arm_text"></span>
                            </div>
                            <div>
                                <span id="cannot_roll_badge"></span><span id="cannot_roll_text"></span>
                                <span id="mistakenly_detected_badge"></span><span id="mistakenly_detected_text"></span>
                                <span id="i2c_badge"></span><span id="i2c_text"></span>
                            </div>
                        </div>
                    </div>
                </section>
                <section class="col-sm-6 content">
                    <div class="box box-primary">
                        <div class="box-header">
                            <span class="box-title">Quantitative analysis</span>
                        </div>
                        <div class="box-body">
                            <table class="table table-hover table-bordered table-with-top-margin">
                                <tbody>
                                    <tr>
                                        <td>Number of objects classified:</td>
                                        <td id="total_objects_classified"></td>
                                    </tr>
                                    <tr>
                                        <td>Maximal weight on conveyor belt:</td>
                                        <td>1 kg</td>
                                    </tr>
                                    <tr>
                                        <td>Battery life: </td>
                                        <td>12 h</td>
                                    </tr>
                                    <tr>
                                        <td>System start up time:</td>
                                        <td>30s</td>
                                    </tr>
                                    <tr>
                                        <td>Average time to get an object to a bin:</td>
                                        <td>4.7s</td>
                                    </tr>
                                </tbody>
                            </table>
                            
                        </div>
                    </div>
                    <div class="box box-solid box-limited-width">
                        <div class="box-header with-border">
                            <h3 class="box-title">Team Members</h3>
                        </div>
                        <div class="box-body no-padding">
                        <ul class="users-list clearfix">
                            <li>
                                <img src="team_images/seanm_img.jpeg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Sean Mullan</a>
                                <span class="users-list-date">Software Team</span>
                            </li>
                            <li>
                                <img src="team_images/sophia_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Sophia Singh</a>
                                <span class="users-list-date">Software Team</span>
                            </li>
                            <li>
                                <img src="team_images/xuran_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Xuran Li</a>
                                <span class="users-list-date">Machine Learning & Vision</span>
                            </li>
                            <li>
                                <img src="team_images/alison_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Alison Li</a>
                                <span class="users-list-date">Vision</span>
                            </li>
                            <li>
                                <img src="team_images/przemek_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Przemek Malon</a>
                                <span class="users-list-date">Construction & Web App Team</span>
                            </li>
                            <li>
                                <img src="team_images/james_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">James Hanratty</a>
                                <span class="users-list-date">Construction Team</span>
                            </li>
                            <li>
                                <img src="team_images/matus_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Matus Drgon</a>
                                <span class="users-list-date">Web App Team</span>
                            </li>
                            <li>
                                <img src="team_images/seans_img.jpg" alt="User Image" class="user-image-height">
                                <a class="users-list-name" href="#">Sean Stirling</a>
                                <span class="users-list-date">Software Team</span>
                            </li>
                        </ul>
                        </div>
                        
                    </div>
                </section>
            </article>

            <div class="box box-solid">
                <div class="box-body">
                    <div class="row zero-side-margins">
                        <form id="update_object" method="POST" action="http://groups.inf.ed.ac.uk/teaching/sdp5/scripts/update_database.php">
                            <div class="col-xs-3">
                                <input id="update_object_id" type="text" name="object_id" class="form-control" placeholder="Object ID">
                            </div>
                            <div class="col-xs-5">
                                <input id="update_object_type" name="object_type" type="text" class="form-control" placeholder="Object type">
                            </div>
                            <div class="col-xs-4">
                                <button type="submit" class="btn btn-primary btn-margin-left"> Submit change </button>
                                <a href="quantitative_data.csv" class="btn btn-primary btn-margin-left" download="Quantitative Analysis">Download quantitative data</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <div class="box box-primary">
                <div class="box-header">
                    <span class="box-title">Collected Data</span>
                </div>
                <div class="box-body">
                    <table class="table table-hover" id="data_table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Object type</th>
                                <th>Classification</th>
                                <th>Weight reading</th>
                                <th>&nbsp;</th>
                                <th>&nbsp;</th>
                            </tr>   
                        </thead>
                        <tbody></tbody>
                    </table>        
                </div>
            </div>
        </section>
    </article>
    
</body>

<!-- Bootstrap scripts -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<!-- AdminLTE -->
<!-- jQuery 3 -->
<script src="AdminLTE/bower_components/jquery/dist/jquery.min.js"></script>
<!-- Bootstrap 3.3.7 -->
<script src="AdminLTE/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
<!-- DataTables -->
<script src="AdminLTE/bower_components/datatables.net/js/jquery.dataTables.js"></script>
<script src="AdminLTE/bower_components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
<!-- SlimScroll -->
<script src="AdminLTE/bower_components/jquery-slimscroll/jquery.slimscroll.min.js"></script>
<!-- FastClick -->
<script src="AdminLTE/bower_components/fastclick/lib/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="AdminLTE/dist/js/adminlte.min.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="AdminLTE/dist/js/demo.js"></script>
<!-- ChartJS -->
<script src="AdminLTE/bower_components/chart.js/Chart.js"></script>
<!-- Bootstrap slider -->
<script src="AdminLTE/plugins/bootstrap-slider/bootstrap-slider.js"></script>
<!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script> -->


<script type="text/javascript">
    var obj_ids = new Map(),               
        not_trained_objects = new Map(),
        highest_id = 0

    //
    // Works with HTML and displays classification accuracies and number of classified objects in each category
    //
    function display_classification_accuracies(glass_acc, metal_acc, plastic_acc, glass_count, metal_count, plastic_count) {
        let metal_cont = $("<div></div>").addClass('col-lg-4 col-xs-6'),
            metal_box = $("<div></div>").addClass('small-box bg-green'),
            metal_inner = $("<div></div>").addClass('inner'),
            metal_headline = $("<h3></h3>").html(metal_acc),
            metal_text = $("<p></p>").html('Metal classification accuracy<br/>' + metal_count + ' classified objects'),
            metal_percentage = $("<sup>%</sup>").css('font-size','20px')
        metal_cont.append(metal_box.append(metal_inner.append(metal_headline.append(metal_percentage)).append(metal_text)))

        let glass_cont = $("<div></div>").addClass('col-lg-4 col-xs-6'),
            glass_box = $("<div></div>").addClass('small-box').css('background-color','#3c8dbc').css('color','white'),
            glass_inner = $("<div></div>").addClass('inner'),
            glass_headline = $("<h3></h3>").html(glass_acc),
            glass_text = $("<p></p>").html('Glass classification accuracy<br/>' + glass_count + ' classified objects'),
            glass_percentage = $("<sup>%</sup>").css('font-size','20px')
        glass_cont.append(glass_box.append(glass_inner.append(glass_headline.append(glass_percentage)).append(glass_text)))

        let plastic_cont = $("<div></div>").addClass('col-lg-4 col-xs-6'),
            plastic_box = $("<div></div>").addClass('small-box').css('background-color','#f39c12').css('color','white'),
            plastic_inner = $("<div></div>").addClass('inner'),
            plastic_headline = $("<h3></h3>").html(plastic_acc),
            plastic_text = $("<p></p>").html('Plastic classification accuracy<br/>' + plastic_count + ' classified objects'),
            plastic_percentage = $("<sup>%</sup>").css('font-size','20px')
        plastic_cont.append(plastic_box.append(plastic_inner.append(plastic_headline.append(plastic_percentage)).append(plastic_text)))

        $("#classification_accuracies").append(metal_cont).append(glass_cont).append(plastic_cont)
    }

    //
    // Handle displaying modals and closing them
    //
    function display_modals() {
        var modals = new Map(),
            images = new Map(),
            buttons = new Map(),
            modalImages = new Map(),
            captions = new Map(),
            closeModal = new Map(),
            deleteButtons = new Map()

        for (let i of obj_ids.values() ) {
            // Get the modal
            modals.set( i, $('#modal_' + i)[0] )

            // Get the image and insert it inside the modal
            images.set( i, $('#image_' + i)[0] )
            buttons.set( i, $('#display_' + i)[0] )
            deleteButtons.set(i, $("#delete_" + i)[0] )
            modalImages.set( i, $('#img_' + i)[0] )
            captions.set( i, $('#caption_' + i)[0] )

            if (buttons.get(i) != null) {
                buttons.get(i).onclick = function() {
                    modals.get(i).style.display = "block"
                    modalImages.get(i).src = images.get(i).src;
                    captions.get(i).innerHTML = images.get(i).alt
                }
            }
            
            if (deleteButtons.get(i) != null) {
                deleteButtons.get(i).onclick = function() {
                    $.ajax({
                        type: "POST",
                        url: "http://groups.inf.ed.ac.uk/teaching/sdp5/scripts/delete_row.php",
                        data: { delete_id: i }
                    }).done(function( msg ) {
                        $("#" + i).css('display','none')
                    }); 
                }
            }

            // Get the <span> element that closes the modal
            closeModal.set( i, $('#close_' + i)[0] )

            // When the user clicks on <span> (x), close the modal
            if (closeModal.get(i) != null) {
                closeModal.get(i).onclick = function() {
                    modals.get(i).style.display = "none";
                }
            } 
        }
    }

    // 
    // Periodically called function to find out if the conveyor belt is currently running or not
    // Based on the result from the Pi, the button to start/stop the belt is rendered appropriately
    //
    function send_startstop_request() {
        var data = {};
        $.ajax({
            url: "http://jigglypuff",
            type: "POST",
            data: JSON.stringify( data ),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                let value = response.data
                if (value == 1) {
                    $('#control_button').css('background-color','#dd4b39')
                    $('#control_button').val("Stop")
                    $('#control_form').val("Stop")
                } else if (value == 0) {
                    $('#control_button').css('background-color','#008d4c')
                    $('#control_button').val("Start")
                    $('#control_form').val("Start")
                }
                setTimeout(function(){
                    send_startstop_request();
                }, 5000);
            }
        });
    }

    //
    // Sends HTTP request to Raspberry Pi. If answer received, Pi is ready to start the conveyor belt when triggered from the website
    // Message is sent periodically to keep the state updated
    //
    function sendMessage(){
        var data = {};
            data.connect_state = $('#message_connected').data('value')
        $.ajax({
            url: "http://jigglypuff",
            type: "POST",
            data: JSON.stringify( data ),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                $('#message_connected').css('color', '#008d4c').html('Connected to Raspberry Pi')
            },
            error: function(response){
                $('#message_connected').css('color', '#d73925').html('Connection failure')
            }
        });

        setTimeout(function(){
            sendMessage();
        }, 5000);
    }

    //
    // Renders data table on the website and gathers data for computing classification accuracies
    //
    function display_table() {
        // Objects sorted in decreasing order based on their ID (so that new objects are at the top of the table)
        // => highest id is ID of object in the first row of the table
        highest_id = $('#hidden_list li:first').data('obj_id')

        renderTable("hidden_list")
    }

    //
    // Updates table with newly gathered data without page reload
    //
    function update_table() {
        if (highest_id == null || highest_id == undefined) highest_id = 100000
        $.ajax({
            url: "http://groups.inf.ed.ac.uk/teaching/sdp5/scripts/download_data.php", 
            type: "POST",
            data: { highest_id: highest_id },
            success: function(result){
                if (result != "") {
                    $("#update_list").html(result);
                    
                    // Objects sorted in decreasing order based on their ID (so that new objects are at the top of the table)
                    // => highest id is ID of object in the first row of the table
                    highest_id = $('#update_list li:first').data('obj_id')
                    
                    renderTable("update_list")
                }
            }
        });
        
        setTimeout(function(){
            update_table();
        }, 5000);
    }

    // 
    // Loops through a list based on given id, renders the table, calculates classification accuracies 
    // and calls functions to render them
    //
    function renderTable(list_id) {
        var classified_plastic_count = 0,
            classified_metal_count = 0,
            classified_glass_count= 0,
            glass_count = 0,
            plastic_count = 0,
            metal_count = 0,
            classified_plastics_corr = 0,
            classified_glass_corr = 0,
            classified_metal_corr = 0,
            ind = 0
        
        obj_ids = new Map()
        not_trained_objects = new Map()

        $('#' + list_id + ' li').each(function(){
            var li = $(this),
                obj_id = li.data('obj_id'),
                obj_classification = li.data('obj_classification'),
                obj_type = li.data('obj_type'),
                bin_type = li.data('bin_type'),
                obj_weight = li.data('object_weight')

            obj_ids.set(ind, obj_id)
            ind++

            if ( li.data("used_for_training") == 0 ) not_trained_objects.set(obj_id, li.data("obj_classification") )

            switch( obj_classification ) {
                case "plastic":
                    classified_plastic_count++
                    break
                case "glass":
                    classified_glass_count++
                    break
                case "metal":
                    classified_metal_count++
                    break
            }

            switch( obj_type ) {
                case "plastic":
                    plastic_count++
                    if ( obj_classification == "plastic" ) classified_plastics_corr++
                    break
                case "glass":
                    glass_count++
                    if ( obj_classification == "glass" ) classified_glass_corr++
                    break
                case "metal":
                    metal_count++
                    if ( obj_classification == "metal" ) classified_metal_corr++
                    break
            }
            
            let tr = $("<tr></tr>").attr('id', obj_id),
                td_id = $("<td>" + obj_id +"</td>"),
                td_type = $("<td>" + obj_type + "</td>").attr('id','obj_type_'+obj_id),
                td_classification = $("<td>" + obj_classification + "</td>"),
                td_image = $("<td style='width:50px'></td>"),
                td_delete = $("<td style='width:50px'></td>").attr('id','td_delete_'+obj_id),
                td_weight = $("<td>" + obj_weight + "</td>")
                
            // Handle displaying modals and closing them
            let img_btn = $("<button>Display</button>").attr('id','display_'+obj_id).addClass('btn btn-default btn-xs'),
                img_src = $("<img>").attr('src','objects_images/image_' + obj_id + '.png').attr('id','image_'+obj_id)
                    .addClass('myImg').css('display','none'),
                outer_div = $("<div></div>").attr('id','modal_'+obj_id).addClass('modal'),
                cancel = $("<span>&times;</span>").attr('id','close_'+obj_id).addClass('close').css('font-size','70px'),
                img_modal = $("<img>").attr('id','img_'+obj_id).addClass('modal-content'),
                inner_div = $("<div></div>").attr('id','caption_'+obj_id).addClass('caption')
            
            if (img_src.attr('src') != null) {
                outer_div.append(cancel).append(img_modal).append(inner_div)
                td_image.append(img_btn).append(img_src).append(outer_div)
            }

            if (li.data('delete_button') == true) {
                var delete_button = $("<button>Delete</button>").attr('id','delete_'+obj_id).addClass('btn btn-danger btn-xs')
                td_delete.append(delete_button)
            }

            tr.append(td_id).append(td_id).append(td_type).append(td_classification)
            .append(td_weight).append(td_image).append(td_delete)
            $('#data_table tbody').append(tr)
        })

        display_modals()

        // Compute classification accuracies
        let glass_acc = Math.round(100*classified_glass_corr/glass_count),
            plastic_acc = Math.round(100*classified_plastics_corr/plastic_count),
            metal_acc = Math.round(100*classified_metal_corr/metal_count)

        display_classification_accuracies(glass_acc, metal_acc, plastic_acc, glass_count, metal_count, plastic_count)
        $("#total_objects_classified").text(glass_count+plastic_count+metal_count)
    }

    //
    // Render HTML and display legend for the pie chart 
    //
    function displayPieChartLegend(errors_percentage) {
        $('#obj_too_big_badge').addClass('badge').css('background-color','#d2d6de').html(errors_percentage[5]+'%')
        $('#obj_too_heavy_badge').addClass('badge').css('background-color','#3c8dbc').html(errors_percentage[4]+'%')
        $('#sorting_arm_badge').addClass('badge').css('background-color','#00c0ef').html(errors_percentage[3]+'%')
        $('#cannot_roll_badge').addClass('badge').css('background-color','#f39c12').html(errors_percentage[2]+'%')
        $('#i2c_badge').addClass('badge').css('background-color','#00a65a').html(errors_percentage[1]+'%')
        $('#mistakenly_detected_badge').addClass('badge').css('background-color','#f56954').html(errors_percentage[0]+'%')
        
        $('#obj_too_big_text').css('padding-left','2px').css('padding-right','10px').css('font-weight','500').html('Object too big')
        $('#obj_too_heavy_text').css('padding-left','2px').css('padding-right','10px').css('font-weight','500').html('Object too heavy')
        $('#sorting_arm_text').css('padding-left','2px').css('padding-right','10px').css('font-weight','500').html('Sorting arm stuck')
        $('#cannot_roll_text').css('padding-left','2px').css('padding-right','10px').css('font-weight','500').html('Cannot roll into bin')
        $('#mistakenly_detected_text').css('padding-left','2px').css('padding-right','10px').css('font-weight','500').html('Mistakenly detected object')
        $('#i2c_text').css('padding-left','2px').css('padding-right','10px').css('font-weight','500').html('Sorting arm i2c error')
    }

    //
    // Renders pie chart on the website
    //
    function renderPieChart() {
        // Get context with jQuery - using jQuery's .get() method.
        var data_1 = 15.4,
            data_2 = 7.7,
            data_3 = 30.8,
            data_4 = 30.8,
            data_5 = 7.7,
            data_6 = 7.7,

            data_1_val = 2,
            data_2_val = 1,
            data_3_val = 4,
            data_4_val = 4,
            data_5_val = 1,
            data_6_val = 1

        var pieChartCanvas = $('#pieChart_breakdown').get(0).getContext('2d')
        var pieChart       = new Chart(pieChartCanvas)
        var PieData        = [
        {
            value    : data_1_val,
            color    : '#f56954',
            highlight: '#f56954',
            label    : 'Mistakenly detected object'
        },
        {
            value    : data_2_val,
            color    : '#00a65a',
            highlight: '#00a65a',
            label    : 'Sorting arm i2c error'
        },
        {
            value    : data_3_val,
            color    : '#f39c12',
            highlight: '#f39c12',
            label    : 'Cannot roll into bin'
        },
        {
            value    : data_4_val,
            color    : '#00c0ef',
            highlight: '#00c0ef',
            label    : 'Sorting arm stuck'
        },
        {
            value    : data_5_val,
            color    : '#3c8dbc',
            highlight: '#3c8dbc',
            label    : 'Object too heavy'
        },
        {
            value    : data_6_val,
            color    : '#d2d6de',
            highlight: '#d2d6de',
            label    : 'Object too big'
        }
        ]
        var pieOptions     = {
        //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke    : true,
        //String - The colour of each segment stroke
        segmentStrokeColor   : '#fff',
        //Number - The width of each segment stroke
        segmentStrokeWidth   : 2,
        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout: 50, // This is 0 for Pie charts
        //Number - Amount of animation steps
        animationSteps       : 100,
        //String - Animation easing effect
        animationEasing      : 'easeOutBounce',
        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate        : true,
        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale         : false,
        //Boolean - whether to make the chart responsive to window resizing
        responsive           : true,
        // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
        maintainAspectRatio  : true,
        //String - A legend template
        legendTemplate       : '<ul class="<%=name.toLowerCase()%>-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'
        }
        //Create pie or douhnut chart    })

        // You can switch between pie and douhnut using the method below.
        pieChart.Doughnut(PieData, pieOptions)

        let data_arr = [data_1, data_2, data_3, data_4, data_5, data_6]
        displayPieChartLegend(data_arr)
    }

    $(function() {
        $(document).on('submit', '#control_form', function(e) {
            let data = {};
            data.state = $("#control_button").val();
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'),
                data: JSON.stringify( data ),
                contentType: "application/json; charset=utf-8",
                success: function(response) {
                    let value = response.data
                    if (value == 1) {
                        $('#control_button').css('background-color','#dd4b39')
                        $('#control_button').val("Stop")
                        $('#control_form').val("Stop")
                    } else if (value == 0) {
                        $('#control_button').css('background-color','#008d4c')
                        $('#control_button').val("Start")
                        $('#control_form').val("Start")
                    }
                }
            });
            e.preventDefault(); 
        });
        
        // Keep button updated to know if conveyor belt is running
        send_startstop_request()
        
        // Keep website updated to know if connection between Pi and website is functional
        sendMessage();

        //
        // Update website with user's input about object classification when form submitted
        //
        $(document).on('submit', '#update_object', function(e) {
            var obj_id = $("#update_object_id").val(),
                obj_type = $("#update_object_type").val()

            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'),
                data: $(this).serialize(),
                success: function(html) {
                    $("#obj_type_" + obj_id).html(obj_type)
                }
            });
            e.preventDefault();
        });
            
        // Display the data table
        display_table()

        //
        // Retrain model on button click
        //
        $(document).on('submit', '#retrain_model', function(e) {
            // Create an array of strings of type "obj_<id>_<classification>" for all objects that have not yet been used for classification
            var obj_id_class_arr = []

            // Filter based on which objects have not been used for training yet
            for (let i of not_trained_objects.keys()) {
                obj_id_class_arr.push( "obj_" + i + "_" + not_trained_objects.get(i))
            }

            let obj = {}      
            obj.data = obj_id_class_arr
            $.ajax({
                data: JSON.stringify(obj),
                dataType: 'json',
                url: $(this).attr('action'),
                type: $(this).attr('method')
            })
        })

        // Render the pie chart
        renderPieChart()

        // Call periodically this function to update the table with newly gathered data without page reload
        update_table()

        $('#data_table').DataTable({
            'paging'      : true,
            'lengthChange': false,
            'searching'   : false,
            'ordering'    : false,
            'info'        : true,
            'autoWidth'   : false
        })
    })

</script>


</html>