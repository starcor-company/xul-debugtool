# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
from PyQt5.QtCore import QUrl, QFile, QIODevice
from PyQt5.QtWebChannel import QWebChannel
import sys


from XulDebugTool.model.WebShareObject import WebShareObject

app = QApplication(sys.argv)
win = QWidget()
win.setWindowTitle('test')

layout = QVBoxLayout()
win.setLayout(layout)
view = QWebEngineView()
channel = QWebChannel()
myObj = WebShareObject()
channel.registerObject("bridge", myObj)
view.page().setWebChannel(channel)
qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit(
        'Failed to load qwebchannel.js with error: %s' %
        qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')
script = QWebEngineScript()
script.setSourceCode(qwebchannel_js + '''new QWebChannel( qt.webChannelTransport, function(channel) {
	            window.bridge = channel.objects.bridge;
	            alert('bridge='+bridge+'get bridge value=' + window.bridge.strValue ) ;
	        });''')
script.setInjectionPoint(QWebEngineScript.DocumentCreation)
script.setName('qtwebchannel.js')
script.setWorldId(QWebEngineScript.MainWorld)
view.page().scripts().insert(script)

view.setHtml(''' <html>
    <head>
      <title>A Demo Page</title>
      <meta charset="UTF-8">
      <script language="javascript">
        
	      function onShowMsgBox() {
	        
	        if ( window.bridge) {
	        	//alert('bridge.strValue=' + window.bridge.strValue ) ;
	            //bridge.sayHello('999')
	            var fname = document.getElementById('fname').value;
	            window.bridge.strValue = fname;
	            
	            
	        }
        	
        }
	          
      
      </script>     
    </head>

    <body>
      <form>
        <label for="姓名">user name:</label>
        <input type="text" name="fname" id="fname"></input>
        <br />
        <input type="button" value="传递参数到pyqt" onclick="onShowMsgBox()">
        <input type="reset" value='重置'/>
      </form>
    </body>
  </html>''')

layout.addWidget(view)

win.show()
sys.exit(app.exec_())
