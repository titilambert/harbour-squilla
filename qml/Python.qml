import QtQuick 2.0
import io.thp.pyotherside 1.2

/*
Python {
    id: py
    property bool ready: false
    Component.onCompleted: {
        addImportPath(Qt.resolvedUrl(".."));
        importModule("heysms", function() {
            py.call("heysms.main", [], function() {
                py.ready = true;
            });
        });
    }
    onError: console.log("Error: " + traceback);
}*/


Python {
    Component.onCompleted: {
        addImportPath(Qt.resolvedUrl(".."));
        console.log('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
        importModule("heysms", function() {
            py.call("heysms.main", [], function() {
                py.ready = true;
            });
        });    
    }
}