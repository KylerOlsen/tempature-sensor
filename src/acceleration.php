<?php
    if (isset($_GET["files"])) {
        $url = "http://localhost:8080/acceleration?files=true";
        $fp = fopen($url, 'rb');
        header("Content-Type: application/json");
        fpassthru($fp);
        exit;
    } else if (isset($_GET["data"])) {
        $url = "http://localhost:8080/acceleration?data=" . $_GET['data'];
        $fp = fopen($url, 'rb');
        header("Content-Type: application/json");
        fpassthru($fp);
        exit;
    } else {
        $url = "http://localhost:8080/acceleration";
        $data = file_get_contents($url);
        echo $data;
    }
?>
