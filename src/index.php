<?php
    if (isset($_GET["graph"])) {
        $url = "http://localhost:8080/" . $_GET['graph'];
        $fp = fopen($url, 'rb');
        header("Content-Type: image/png");
        fpassthru($fp);
        exit;
    } else {
        $url = "http://localhost:8080";
        $data = file_get_contents($url);
        echo $data;
    }
?>
