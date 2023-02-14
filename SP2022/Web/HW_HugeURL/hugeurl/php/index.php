<?php

require __DIR__ . '/../vendor/autoload.php';
require __DIR__ . '/inc.php';

$app = new Bullet\App(['template' => [
    'path' => __DIR__ . '/templates/'
]]);

$app->path('/', function ($request) use ($app) {
    return $app->template('index');
});

$app->path('/create', function ($request) use ($app) {
    $app->post(function ($request) use ($app) {
        if (!filter_var($request->url, FILTER_VALIDATE_URL)) {
            die("Invalid URL");
        }

        $uuid = uuid();
        redis()->set($uuid, new Page($request->url));
        return $app->response()->redirect("/p/$uuid");
    });
});

$app->path('/p', function ($request) use ($app) {
    $app->param(
        fn ($slug) => preg_match("#[a-z0-9_-]+#i", $slug) && $slug,
        function ($request, $uuid) use ($app) {
            if ($page = redis()->get($uuid)) {
                return $app->template('preview', [
                    'page' => $page,
                    'preview' => "http://$_SERVER[HTTP_HOST]/p/$uuid",
                    'redirect' => "http://$_SERVER[HTTP_HOST]/r/$uuid"
                ]);
            } else {
                return false;
            }
        }
    );
});

$app->path('/r', function ($request) use ($app) {
    $app->param(
        fn ($slug) => preg_match("#[a-z0-9_-]+#i", $slug) && $slug,
        function ($request, $slug) use ($app) {
            if ($page = redis()->get($slug)) {
                return $app->response()->redirect($page->url);
            } else {
                return false;
            }
        }
    );
});

$app->run(new Bullet\Request())->send();
