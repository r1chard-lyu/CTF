// ==UserScript==
// @name         test1
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://game.zoolab.org:8443/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=zoolab.org
// @grant        none
// ==/UserScript==

let gameWindow = gameFrame.contentWindow
let gameDocument = gameFrame.contentDocument
let gameElement
window.send = send

function send (msg) {
    const event = new CustomEvent("send", { detail: msg });
    gameElement.dispatchEvent(event);
}

function init () {
    gameElement = gameDocument.querySelector('#game')
}

async function main () {
    init()
    console.log(gameElement)
    for (let i = 0; i < 100; i++) {
    send({
        "type": "attack",
        "data": {
            "facing": [0, 1],
        }
    })}
}

window.setTimeout(main, 500)