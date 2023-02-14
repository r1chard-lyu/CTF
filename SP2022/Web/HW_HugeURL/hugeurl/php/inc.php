<?php

class Page
{
    public $url;
    private $title;
    private $preview;
    function __construct($url)
    {
        $this->url = $url;
        $this->fetch();
    }
    public function fetch()
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        $response = curl_exec($ch);

        if (preg_match("#<title>([\S\s]+)</title>#i", $response, $match)) {
            $this->title = trim($match[1]);
        } else {
            $this->title = $this->url;
        }

        if (preg_match("#<body>([\S\s]+)</body>#i", $response, $match)) {
            $this->preview = substr(strip_tags($match[1]), 0, 128) . "...";
        } else {
            $this->preview = $this->title;
        }
    }
    public function previewCard()
    {
        return "
        <div class=\"preview\">
        <strong>$this->title</strong><br>
        <small>$this->url</small><br>
        $this->preview
        </div>
        ";
    }
}

function redis()
{
    $redis = new Redis();
    $redis->connect('redis', 6379);
    $redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_PHP);
    return $redis;
}

function uuid()
{
    return str_replace(["/", "+"], ["_", "-"], base64_encode(random_bytes(150)));
}
