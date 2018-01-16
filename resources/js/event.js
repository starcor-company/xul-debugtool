var windowLoaded = false;
var transportAvailable = false;

new QWebChannel(qt.webChannelTransport, function (channel) {
    window.bridge = channel.objects.bridge // https://doc.qt.io/qt-5/qtwebchannel-javascript.html
    transportAvailable = true
    __main()
});

window.onload = function () {
    windowLoaded = true
    __main()
};

function __main() {
    if (!windowLoaded || !transportAvailable) {
        return;
    }

    try {
        onEnvironmentReady(); // 加代码在这个方法里面加,这个方法里可以安全地打日志,出错也会有报错弹窗
    } catch (e){
        window.alert(e+"  ")
    }
}

function onEnvironmentReady() {
    renderNodes();
}

function renderNodes(){
    var bObj = document.getElementsByClassName("html-attribute");
    for (var i = 0, item; item = bObj[i]; i++) {
        if (isIdNode(item)) {
            renderIdNode(item)
        }
        if (isImgNode(item)) {
            renderImgNode(item);
        }
    }
}

function isIdNode(item) {
    return item.children[0].innerText === "id"
}

function isImgNode(item) {
    var attrValue = item.children[1].innerText;
    return attrValue.startsWith("img.")
        && (attrValue.length === 5 || attrValue.length === 6)
}

function renderIdNode(item) {
    item.onclick = idClick;
    item.style.textDecoration = "underline";
    item.style.cursor = "pointer";
}

function renderImgNode(item) {
    var valueElement = getValueElement(item);

    valueElement.onclick = imgClick;
    valueElement.style.textDecoration = "underline";
    valueElement.style.cursor = "pointer";
}

function getValueElement(item) {
    var e1 = item.parentElement.parentElement.getElementsByClassName("text")[0]
    var e2 = item.parentElement.parentElement.parentElement.getElementsByClassName("text")[0]

    if (typeof  e1 == 'undefined') { //换行的情况下会出现
        return e2
    }
    return e1
}


function imgClick() {
    var event = {
        "action":"showImg",
        "Id":"",
        "data":this.innerText
    }
    window.bridge.strValue = JSON.stringify(event)
}

function idClick() {
    var event = {
        "action" : "updateProp",
        "Id" : this.children[1].innerText,
        "xml" : document.getElementById("webkit-xml-viewer-source-xml").innerHTML
    }
    window.bridge.strValue = JSON.stringify();
}

function log(msg) {
    event = {
        "action":"doLog",
        "Id":"---",
        "data":msg
    }
    window.bridge.strValue = JSON.stringify(event);
}

