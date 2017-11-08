window.onload = function () {
    alert("onload");
    var bObj = document.getElementsByClassName("html-attribute-value");

    for (var i = 0, item; item = bObj[i]; i++) {
        item.onclick = objclick;
    }
    function objclick() {
        alert(this.innerText);
        onShowMsgBox(this.innerText)
    }
};

function onShowMsgBox(text) {
    if (window.bridge) {
        window.bridge.strValue = text;
    }
}