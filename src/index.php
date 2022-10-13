<?php
    if (isset($_GET["graph"])) {
        $url = "http://localhost:8080/" . $_GET['graph'];

        $fp = fopen($url, 'rb');

        // send the right headers
        header("Content-Type: image/png");
        //header("Content-Length: " . filesize($url));

        // dump the picture and stop the script
        fpassthru($fp);
        exit;

        // $img = file_get_contents($url);
        // //echo $img;
        // //echo gettype($img);

        // // send the right headers
        // header("Content-Type: image/png");
        // //header("Content-Length: " . mb_strlen(serialize((array)$img), '8bit'));
        // header("Content-Length: " . strlen($img));
        
        // // dump the picture and stop the script
        // fpassthru($img);
        // exit;
    } else {
        $url = "http://localhost:8080";
        $data = file_get_contents($url);
        echo $data;
    }
?>
