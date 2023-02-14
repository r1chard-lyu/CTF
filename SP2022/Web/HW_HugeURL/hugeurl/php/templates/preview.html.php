<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
    <title>HugeURL</title>
    <style>
        .preview {
            background: var(--accent-bg);
            border: 2px solid var(--border);
            border-radius: 5px;
            padding: 1.5rem;
            margin: 2rem 0;
        }

        input,
        button {
            width: 100%;
        }
    </style>
</head>

<body>
    <main>
        <h1>You are about to go to <?= $page->url ?></h1>
        <p>Here is a preview of the page...</p>
        <?= $page->previewCard() ?>
        <a href="<?= $redirect ?>"><button>Redirect ➡️</button></a>

        <hr>
        <p>Preview (this page): <input value="<?= $preview ?>" readonly>
        </p>
        <p>Redirect Directly: <input value="<?= $redirect ?>" readonly>
        </p>
    </main>

</body>

</html>