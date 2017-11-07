window.onload = function () {
    var bObj = document.getElementsByClassName("html-attribute-value");

    for (var i = 0, item; item = bObj[i]; i++) {
        item.onclick = objclick;
    }
    function objclick() {
        alert(this.innerText);
    }
};
