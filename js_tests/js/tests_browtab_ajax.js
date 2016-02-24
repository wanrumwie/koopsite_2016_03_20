/*
Global:  $ (?), JSON (?), QUnit (?), TR_start (?), auxiliary_handler, columnsNumber, create_qs_TR_arr (?), display_qs_TR_arr (?), expect (?), getRowIndexbyID (?), getSelRowIndex (?), getTRbyID (?), getTRbyIndex (?), getTRfromTbodyByIndex (?), get_m_id_n_ByIndex (?), get_qs_TR_arr (?), markSelRow (?), onClick_handler (?), onDblclick_handler (?), onKeyDown (?), onKeydown_handler (?), qs_TR_arr (?), restore_qs_TR_arr (?), rowsNumber (?), selElement (?), selRowFocus (?), selRowIndex (?), selTR (?), selectRow (?), selectStyle (?), setSelRow (?), setStartRow (?), set_browtab_listeners (?), sinon (?), storeSelRowIndex (?), stub, window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test
/*
var qs_obj = { 
                0: {
                    0: {'id': '3', 'model': 'user', 'name': 'george'}, 
                    1: 'george', 
                    2: ''
                    }, 
                1: {
                    0: {'id': '1', 'model': 'user', 'name': 'john'}, 
                    1: 'john', 
                    2: ''
                    },
                2: {
                    0: {'id': '3', 'model': 'folder', 'name': 'fjohn'}, 
                    1: 'fjohn', 
                    2: ''
                    }
                };
var json_string = JSON.stringify( qs_obj ); // array stored in html by server
$( "#json_arr" ).val( json_string );
console.log('json_string=',json_string);
*/
/*
        console.log('$( "#csrfmiddlewaretoken" ).val() =', $( "#csrfmiddlewaretoken" ).val());
var columnsNumber = 2;
function ajaxSuccessHandler( sr ) {
}
$( document ).ready( function () {
    console.log('document ready');
    console.log('$( "#csrfmiddlewaretoken" ).val() =', $( "#csrfmiddlewaretoken" ).val());
    ajax_startRowIndexFromSession();                // Receiving start row index from session
} );
*/
function getSelElementArr(){
    var arr = {};
    return arr;
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
        console.log('$( "#csrfmiddlewaretoken" ).val() =', $( "#csrfmiddlewaretoken" ).val());
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
        // Attension! in this test stub is name for sinon.spy, not sinon,stub
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
function ajaxSuccessHandler(){  // function declared in another file
}
QUnit.module( "browtab_ajax ajax", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var xhr = sinon.useFakeXMLHttpRequest();
    var requests = sinon.requests;
    requests = [];
    xhr.onCreate = function ( request ) {
        requests.push(request);
    };
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'ajax_selRowIndexToSession', function ( assert ) {
        expect( 6 );
        
        stub.success = sinon.stub( window, "ajax_selRowIndexToSession_success_handler" );
        stub.error   = sinon.stub( window, "ajax_selRowIndexToSession_error_handler" );

        var res = ajax_selRowIndexToSession( );

        assert.equal( requests.length, 1 , "request length should be 1" );
        assert.equal( requests[0].url, "/ajax-selrowindex-to-session", "request should have proper url" );
		
	    requests[0].respond( 200, { "Content-Type": "application/json" }, '[]');

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.ok( stub.success.calledWith( ), 'success should be called with arg' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_selRowIndexToSession should return false' );
    });
} );
//=============================================================================


