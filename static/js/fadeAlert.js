const fade = (element) => {
    let op = 1;  // initial opacity
    let timer = setInterval(function () {
        if (op < 0.1) {
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 80);
}

window.setTimeout(function () {
    fade(document.getElementById('fadesAway'))
}, 2500);
