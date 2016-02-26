/*
Global:  $ (?), JSON (?), QUnit (?), ajaxSuccessHandler, ajax_selRowIndexToSession (?), ajax_selRowIndexToSession_error_handler (?), ajax_selRowIndexToSession_success_handler (?), ajax_settings (?), ajax_startRowIndexFromSession (?), ajax_startRowIndexFromSession_error_handler (?), ajax_startRowIndexFromSession_success_handler (?), browtab_ajax_document_ready_handler (?), csrf_token (?), dialog, dialogMessage, dialog_box_form_close, expect (?), folderEmptyMessage, getSelElementArr, onChange_handler (?), rowsNumber (?), set_browtab_ajax_listeners (?), sinon (?), stub, transferCanceled (?), transferFailed (?), window (?), xhrErrorAlert (?), xhrErrorHandler (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test
function getSelElementArr(){    // function declared in another file
    return {};
}
//=============================================================================
QUnit.module( "browtab_ajax document ready", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var $tbody;
    var $selRowIndex;
    var selRowIndex_selector;
    var target_selector;
    var saved_csrf_token;
    hooks.beforeEach( function( assert ) {
        stub = {};
        target_selector       = "#td_qwerty";
        selRowIndex_selector  = "#selRowIndex";
        $selRowIndex          = $( selRowIndex_selector );
        set_browtab_ajax_listeners(); 
        saved_csrf_token      = $( "#csrfmiddlewaretoken" ).val();
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        $( "#csrfmiddlewaretoken" ).val( saved_csrf_token );
        csrf_token = saved_csrf_token;
    } );
    QUnit.test( 'browtab_ajax_document_ready_handler', function ( assert ) {
        expect( 8 );
        $( "#csrfmiddlewaretoken" ).val( 'qwerty' );
        stub.create_qs_TR_arr = sinon.stub( window, "create_qs_TR_arr" );
        stub.ajax_startRowIndexFromSession = sinon.stub( window, "ajax_startRowIndexFromSession" );
        stub.set_browtab_ajax_listeners = sinon.stub( window, "set_browtab_ajax_listeners" );
        var res = browtab_ajax_document_ready_handler( );
        assert.ok( stub.create_qs_TR_arr.calledOnce, 'create_qs_TR_arr should be called once' );
        assert.ok( stub.create_qs_TR_arr.calledWith( ), 'create_qs_TR_arr should be called with arg' );
        assert.ok( stub.ajax_startRowIndexFromSession.calledOnce, 'ajax_startRowIndexFromSession should be called once' );
        assert.ok( stub.ajax_startRowIndexFromSession.calledWith(),'ajax_startRowIndexFromSession should be called with arg');
        assert.ok( stub.set_browtab_ajax_listeners.calledOnce, 'set_browtab_ajax_listeners should be called once' );
        assert.ok( stub.set_browtab_ajax_listeners.calledWith( ), 'set_browtab_ajax_listeners should be called with arg' );
        assert.equal( csrf_token, 'qwerty', 'browtab_ajax_document_ready_handler should set value to global var' );
        assert.equal( res, undefined, 'browtab_ajax_document_ready_handler should return undefined' );
    });
    QUnit.test( 'set_browtab_ajax_listeners', function ( assert ) {
        // Attension! in this test stub is name for sinon.spy, not sinon.stub
        expect( 5 );

        stub.off = sinon.spy( $selRowIndex, "off" );
        stub.on  = sinon.spy( $selRowIndex, "on" );

        var res = set_browtab_ajax_listeners( $selRowIndex );

        assert.ok( stub.off.calledOnce, 'off should be called once' );
        assert.ok( stub.on.calledOnce, 'on should be called once' );
        assert.ok( stub.off.getCall( 0 ).calledWith( "change" ), '0 off should be called with arg' );
        assert.ok( stub.on.getCall( 0 ).calledWith( "change", onChange_handler ), '0 on should be called with arg' );
        assert.equal( res, undefined, 'set_browtab_ajax_listeners should return undefined' );
    });
    QUnit.test( 'onChange_handler', function ( assert ) {
        expect( 3 );
        stub.ajax_selRowIndexToSession = sinon.stub( window, "ajax_selRowIndexToSession" );
        var res = onChange_handler( );
        assert.ok( stub.ajax_selRowIndexToSession.calledOnce, 'ajax_selRowIndexToSession should be called once' );
        assert.ok( stub.ajax_selRowIndexToSession.calledWith(  ), 'ajax_selRowIndexToSession should be called with arg' );
        assert.equal( res, false, 'onChange_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "change",... STUB ajax_selRowIndexToSession', function ( assert ) {
        expect( 1 );
        stub.ajax_selRowIndexToSession = sinon.stub( window, "ajax_selRowIndexToSession" );
        $('#selRowIndex').trigger( 'change' );  // actibation of data exchange with session
//        $( selRowIndex_selector ).trigger( 'change' );
        assert.ok( stub.ajax_selRowIndexToSession.calledOnce, 'ajax_selRowIndexToSession should be called once' );
    });
} );
//=============================================================================
function dialogMessage( a,b,c,d ){  // function declared in another file
}
function dialog( a ){               // function declared in another file
}
function dialog_box_form_close() {  // function declared in another file
}
QUnit.module( "browtab_ajax dialogs & alert", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var xhr = {};
    hooks.beforeEach( function( assert ) {
        stub = {};
        xhr.status      ='s'; 
        xhr.statusText  ='t';
        xhr.responseText='r';
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'xhrErrorAlert', function ( assert ) {
        expect( 3 );
        var ss = '';
        var arg = 'xhrErrorAlert: ' + ss +
                '\n xhr.status='        + xhr.status + 
                '\n xhr.statusText='    + xhr.statusText + 
                '\n xhr.responseText='  + xhr.responseText;
        
        stub.alert = sinon.stub( window, "alert" );
        var res = xhrErrorAlert( xhr, ss );
        assert.ok( stub.alert.calledOnce, 'alert should be called once' );
        assert.ok( stub.alert.calledWith( arg ), 'alert should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorAlert should return undefined' );
    });
    QUnit.test( 'xhrErrorAlert ss', function ( assert ) {
        expect( 3 );
        var ss = 'qwerty';
        var arg = 'xhrErrorAlert: ' + ss +
                '\n xhr.status='        + xhr.status + 
                '\n xhr.statusText='    + xhr.statusText + 
                '\n xhr.responseText='  + xhr.responseText;
        
        stub.alert = sinon.stub( window, "alert" );
        var res = xhrErrorAlert( xhr, ss );
        assert.ok( stub.alert.calledOnce, 'alert should be called once' );
        assert.ok( stub.alert.calledWith( arg ), 'alert should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorAlert should return undefined' );
    });
    QUnit.test( 'xhrErrorHandler 200', function ( assert ) {
        expect( 5 );
        xhr.status      = 200; 
       
        stub.xhrErrorAlert          = sinon.stub( window, "xhrErrorAlert" );
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = xhrErrorHandler( xhr );

        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWith( xhr, 'xhrErrorHandler' ), 'xhrErrorAlert should be called with arg' );
        assert.notOk( stub.dialogMessage.called, 'dialogMessage should not be called' );
        assert.notOk( stub.dialog_box_form_close.called, 'dialog_box_form_close should not be called' );
        assert.equal( res, undefined, 'xhrErrorHandler should return undefined' );
    });
    QUnit.test( 'xhrErrorHandler 401', function ( assert ) {
        expect( 6 );
        xhr.status      = 401; 
       
        stub.xhrErrorAlert          = sinon.stub( window, "xhrErrorAlert" );
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = xhrErrorHandler( xhr );

        assert.notOk( stub.xhrErrorAlert.called, 'xhrErrorAlert should not be called' );
        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWith( "Ви не маєте доступу до цієї операції!",
                      "Error", "Помилка доступу", 3000 ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWith(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorHandler should return undefined' );
    });
    QUnit.test( 'xhrErrorHandler 403', function ( assert ) {
        expect( 6 );
        xhr.status      = 403; 
       
        stub.xhrErrorAlert          = sinon.stub( window, "xhrErrorAlert" );
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = xhrErrorHandler( xhr );

        assert.notOk( stub.xhrErrorAlert.called, 'xhrErrorAlert should not be called' );
        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWith( "Ви не маєте доступу до цієї операції!",
                      "Error", "Помилка доступу", 3000 ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWith(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorHandler should return undefined' );
    });
    QUnit.test( 'transferFailed', function ( assert ) {
        expect( 5 );
        var evt = "";

        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = transferFailed( evt );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWith( "An error occurred while transferring the file. Probably file too long", 
                        "Error", "UPLOAD ERROR", 3000 ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWith(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'transferFailed should return undefined' );
    });
    QUnit.test( 'transferCanceled', function ( assert ) {
        expect( 5 );
        var evt = "";

        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = transferCanceled( evt );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWith( "The transfer has been canceled by the user.", "", 
                                            "UPLOAD CANCELED", 2000 ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWith(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'transferCanceled should return undefined' );
    });
} );
//=============================================================================
function folderEmptyMessage( f_name ) {    // This function declared in another js file.
}
QUnit.module( "browtab_ajax session handlers", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var xhr;
    var sr;
    var json;
    hooks.beforeEach( function( assert ) {
        stub = {};
        xhr = 'qwerty';
        sr = {};
        sr.selRowIndex  = 55;
        sr.model        = 'folder';
        sr.id           = 77;
        json = {};
        json.server_response = sr;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'ajax_selRowIndexToSession_error_handler', function ( assert ) {
        expect( 3 );
        stub.xhrErrorAlert = sinon.stub( window, "xhrErrorAlert" );
        var res = ajax_selRowIndexToSession_error_handler( xhr );
        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWith( xhr, 'ajax_selRowIndexToSession' ), 
                                                                'xhrErrorAlert should be called with arg' );
        assert.equal( res, undefined, 'ajax_selRowIndexToSession_error_handler should return undefined' );
    });
    QUnit.test( 'ajax_startRowIndexFromSession_error_handler', function ( assert ) {
        expect( 5 );
        stub.xhrErrorAlert = sinon.stub( window, "xhrErrorAlert" );
        stub.setStartRow = sinon.stub( window, "setStartRow" );
        var res = ajax_startRowIndexFromSession_error_handler( xhr );
        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWith( xhr, 'ajax_startRowIndexFromSession' ), 
                                                                'xhrErrorAlert should be called with arg' );
        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWith( ), 'setStartRow should be called with arg' );
        assert.equal( res, undefined, 'ajax_startRowIndexFromSession_error_handler should return undefined' );
    });
    QUnit.test( 'ajax_startRowIndexFromSession_success_handler', function ( assert ) {
        expect( 7 );
        rowsNumber = 100;

        stub.setStartRow = sinon.stub( window, "setStartRow" );
        stub.folderEmptyMessage = sinon.stub( window, "folderEmptyMessage" );

        var res = ajax_startRowIndexFromSession_success_handler( json );

        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWith( ), 'setStartRow should be called with arg' );
        assert.notOk( stub.folderEmptyMessage.called, 'folderEmptyMessage should not be called' );

        assert.equal( $( "#selRowIndex" ).val(), sr.selRowIndex, 'function set value to html' );
        assert.equal( $( "#selElementModel" ).val(), sr.model, 'function set value to html' );
        assert.equal( $( "#selElementID" ).val(), sr.id, 'function set value to html' );

        assert.equal( res, undefined, 'ajax_startRowIndexFromSession_success_handler should return undefined' );
    });
    QUnit.test( 'ajax_startRowIndexFromSession_success_handler empty folder', function ( assert ) {
        expect( 8 );
        rowsNumber = 0;
        var f_name = $( "#thisfolder span" ).text();    // parent folder name

        stub.setStartRow = sinon.stub( window, "setStartRow" );
        stub.folderEmptyMessage = sinon.stub( window, "folderEmptyMessage" );

        var res = ajax_startRowIndexFromSession_success_handler( json );

        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWith( ), 'setStartRow should be called with arg' );
        assert.ok( stub.folderEmptyMessage.calledOnce, 'folderEmptyMessage should be called once' );
        assert.ok( stub.folderEmptyMessage.calledWith( f_name ), 'folderEmptyMessage should be called with arg' );

        assert.equal( $( "#selRowIndex" ).val(), sr.selRowIndex, 'function set value to html' );
        assert.equal( $( "#selElementModel" ).val(), sr.model, 'function set value to html' );
        assert.equal( $( "#selElementID" ).val(), sr.id, 'function set value to html' );

        assert.equal( res, undefined, 'ajax_startRowIndexFromSession_success_handler should return undefined' );
    });
} );
//=============================================================================
function ajaxSuccessHandler(){  // function declared in another file
}
QUnit.module( "browtab_ajax ajax", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var requests = sinon.requests;
    var done;
    hooks.beforeEach( function( assert ) {
        stub = {};
        csrf_token = $( "#csrfmiddlewaretoken" ).val();
        this.xhr = sinon.useFakeXMLHttpRequest();
        requests = [];
        this.xhr.onCreate = function ( request ) {
            requests.push( request );
        };
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        this.xhr.restore();
    } );
    QUnit.test( 'ajax_selRowIndexToSession', function ( assert ) {
        expect( 16 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-selrowindex-to-session";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attension! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_selRowIndexToSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_selRowIndexToSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_selRowIndexToSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWith( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWith( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWith( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_selRowIndexToSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_selRowIndexToSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.ok( stub.success.calledWith( JSON.parse( response_body ) ), 'success should be called with arg' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_selRowIndexToSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_selRowIndexToSession error', function ( assert ) {
        expect( 16 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-selrowindex-to-session";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attension! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_selRowIndexToSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_selRowIndexToSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_selRowIndexToSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWith( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWith( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWith( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_selRowIndexToSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_selRowIndexToSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called once' );
        assert.ok( stub.error.calledOnce, 'error should not be called' );
        assert.ok( stub.error.calledWith( ), 'error should be called with arg' );

        assert.equal( res, false, 'ajax_selRowIndexToSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_startRowIndexFromSession', function ( assert ) {
        expect( 16 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-startrowindex-from-session";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attension! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_startRowIndexFromSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_startRowIndexFromSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_startRowIndexFromSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWith( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWith( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWith( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_startRowIndexFromSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_startRowIndexFromSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.ok( stub.success.calledWith( JSON.parse( response_body ) ), 'success should be called with arg' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_startRowIndexFromSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_startRowIndexFromSession error', function ( assert ) {
        expect( 16 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-startrowindex-from-session";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attension! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_startRowIndexFromSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_startRowIndexFromSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_startRowIndexFromSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWith( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWith( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWith( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_startRowIndexFromSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_startRowIndexFromSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called once' );
        assert.ok( stub.error.calledOnce, 'error should not be called' );
        assert.ok( stub.error.calledWith( ), 'error should be called with arg' );

        assert.equal( res, false, 'ajax_startRowIndexFromSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
} );
//=============================================================================
