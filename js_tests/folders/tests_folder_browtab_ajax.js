/*
Global:  $ (?), JSON (?), QUnit (?), ajaxSuccessHandler, ajax_selRowIndexToSession (?), ajax_selRowIndexToSession_error_handler (?), ajax_selRowIndexToSession_success_handler (?), ajax_settings (?), ajax_startRowIndexFromSession (?), ajax_startRowIndexFromSession_error_handler (?), ajax_startRowIndexFromSession_success_handler (?), browtab_ajax_document_ready_handler (?), csrf_token (?), dialog, dialogMessage, dialog_box_form_close, expect (?), folderEmptyMessage, getSelElementArr, onChange_handler (?), rowsNumber (?), set_browtab_ajax_listeners (?), sinon (?), stub, transferCanceled (?), transferFailed (?), window (?), xhrErrorAlert (?), xhrErrorHandler (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test
//=============================================================================
function dialogMessage( a,b,c,d ){  // function declared in another file
}
function dialog_box_form_close(){  // function declared in another file
}
function dialogFoldersTreeHTML(){  // function declared in another file
}
QUnit.module( "folder_browtab_ajax handlers", function( hooks ) { 
    var sr;
    hooks.beforeEach( function( assert ) {
        stub = {};
        sr = {};
        sr.message  = 'qwerty';
        sr.type     = '';
        sr.title    = 'title';
        var ob = {};
        ob.model  = 'report';  
        ob.id     = 555;
        ob.name   = 'fred.pdf';
        sr.changes  = [ob, '', 'fred.pdf', '11.01.2016', 1234567];
        sr.supplement = {};
        sr.supplement.iconPath = "/static/img/file-icons/32px/pdf.png";
        
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );
        stub.addNewElement          = sinon.stub( window, "addNewElement" );
        stub.changeSelElement       = sinon.stub( window, "changeSelElement" );
        stub.set_name_to_selElement = sinon.stub( window, "set_name_to_selElement" );
        stub.moveElement            = sinon.stub( window, "moveElement" );
        stub.deleteElement          = sinon.stub( window, "deleteElement" );
        stub.destroy                = sinon.stub( $.jstree, "destroy" );

    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'ajaxSuccessHandler', function ( assert ) {
        expect( 3 );
        stub.xhrSuccessHandler = sinon.stub( window, "xhrSuccessHandler" );
        var res = ajaxSuccessHandler( sr );
        assert.ok( stub.xhrSuccessHandler.calledOnce, 'xhrSuccessHandler should be called once' );
        assert.ok( stub.xhrSuccessHandler.calledWithExactly( sr ), 'xhrSuccessHandler should be called with arg' );
        assert.equal( res, undefined, 'ajaxSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler IncorrectData', function ( assert ) {
        expect( 10 );

        sr.type = 'IncorrectData';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.notOk( stub.dialog_box_form_close.called, 'dialog_box_form_close should be not called' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Error', function ( assert ) {
        expect( 11 );

        sr.type = 'Error';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Forbidden', function ( assert ) {
        expect( 11 );

        sr.type = 'Forbidden';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Normal', function ( assert ) {
        expect( 11 );

        sr.type = 'Normal';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler NoChange', function ( assert ) {
        expect( 11 );

        sr.type = 'NoChange';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler NewRow', function ( assert ) {
        expect( 12 );

        sr.type = 'NewRow';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.ok( stub.addNewElement.calledOnce, 'addNewElement should be called once' );
        assert.ok( stub.addNewElement.calledWithExactly( sr.changes, sr.supplement ), 'addNewElement should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Rename', function ( assert ) {
        expect( 13 );

        sr.type = 'Rename';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.ok( stub.changeSelElement.calledOnce, 'changeSelElement should be called once' );
        assert.ok( stub.changeSelElement.calledWithExactly( sr.changes, sr.supplement ), 
                                                    'changeSelElement should be called with args' );
        assert.ok( stub.set_name_to_selElement.called, 'set_name_to_selElement should be called once' );
        assert.ok( stub.set_name_to_selElement.calledWithExactly( sr.changes[0].name ), 
                                                    'set_name_to_selElement should be called with args' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler MoveElement', function ( assert ) {
        expect( 13 );

        sr.type = 'MoveElement';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.ok( stub.moveElement.calledOnce, 'moveElement should be called once' );
        assert.ok( stub.moveElement.calledWithExactly( ), 'moveElement should be called with args' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.ok( stub.destroy.calledOnce, 'destroy should be called once' );
        assert.ok( stub.destroy.calledWithExactly( ), 'destroy should be called with args' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler DeleteRow', function ( assert ) {
        expect( 12 );

        sr.type = 'DeleteRow';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.ok( stub.deleteElement.called, 'deleteElement should be called once' );
        assert.ok( stub.deleteElement.calledWithExactly( ), 'deleteElement should be called with args' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler unknown', function ( assert ) {
        expect( 11 );

        sr.type = 'unknown';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.addNewElement.called, 'addNewElement should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.set_name_to_selElement.called, 'set_name_to_selElement should be not called' );
        assert.notOk( stub.moveElement.called, 'moveElement should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );
        assert.notOk( stub.destroy.called, 'destroy should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
} );
QUnit.test( 'getSelElementArr', function ( assert ) {
    expect( 1 );
    selElement.model = 'report';
    selElement.id    = 55;
    selElement.name  = 'name';
    var arr = {};
    arr.browTabName = "browTabName";
    arr.parent_id   = "parent.id";
    arr.selRowIndex = "selRowIndex";
    arr.model       = 'report';
    arr.id          = 55;
    arr.name        = 'name';
    
    var res = getSelElementArr( );

    assert.deepEqual( res, arr, 'getSelElementArr should return prorer value' );
    });
//=============================================================================
QUnit.module( "browtab_ajax ajax_FoldersTreeFromBase handlers", function( hooks ) { 
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
    QUnit.test( '_error_handler', function ( assert ) {
        expect( 5 );
        stub.xhrErrorAlert = sinon.stub( window, "xhrErrorAlert" );
        stub.setStartRow = sinon.stub( window, "setStartRow" );
        var res = ajax_FoldersTreeFromBase_error_handler( xhr );
        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWithExactly( xhr, 'ajax_FoldersTreeFromBase' ), 
                                                                'xhrErrorAlert should be called with arg' );
        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWithExactly( ), 'setStartRow should be called with arg' );
        assert.equal( res, undefined, 'ajax_FoldersTreeFromBase_error_handler should return undefined' );
    });
    QUnit.test( '_success_handler', function ( assert ) {
        expect( 3 );
        rowsNumber = 100;

        stub.dialogFoldersTreeHTML = sinon.stub( window, "dialogFoldersTreeHTML" );

        var res = ajax_FoldersTreeFromBase_success_handler( json );

        assert.ok( stub.dialogFoldersTreeHTML.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.dialogFoldersTreeHTML.calledWithExactly( json.server_response ), 'setStartRow should be called with arg' );

        assert.equal( res, undefined, 'ajax_FoldersTreeFromBase_success_handler should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_ajax ajax", function( hooks ) { 
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
    QUnit.test( 'ajax_FoldersTreeFromBase', function ( assert ) {
        expect( 15 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/folders/ajax-folders-tree-from-base";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_FoldersTreeFromBase_success_handler" );
        stub.error              = sinon.stub( window, "ajax_FoldersTreeFromBase_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_FoldersTreeFromBase( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_FoldersTreeFromBase_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_FoldersTreeFromBase_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_FoldersTreeFromBase should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_FoldersTreeFromBase error', function ( assert ) {
        expect( 15 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/folders/ajax-folders-tree-from-base";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_FoldersTreeFromBase_success_handler" );
        stub.error              = sinon.stub( window, "ajax_FoldersTreeFromBase_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_FoldersTreeFromBase( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_FoldersTreeFromBase_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_FoldersTreeFromBase_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called once' );

        assert.equal( res, false, 'ajax_FoldersTreeFromBase should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_folderCreate success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/folders/ajax-folder-create";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_folderCreate( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_folderCreate should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_folderCreate error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/folders/ajax-folder-create";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_folderCreate( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_folderCreate should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_folderRename success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/folders/ajax-folder-rename";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_folderRename( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_folderRename should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_folderRename error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/folders/ajax-folder-rename";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_folderRename( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_folderRename should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_reportRename success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/folders/ajax-report-rename";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_reportRename( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_reportRename should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_reportRename error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/folders/ajax-report-rename";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_reportRename( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_reportRename should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_elementMove success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var target_id = 88;
        arr.target_id = target_id;                  // additional element in arr
        var expected_url = "/folders/ajax-element-move";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_elementMove( target_id );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_elementMove should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_elementMove error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var target_id = 88;
        arr.target_id = target_id;                  // additional element in arr
        var expected_url = "/folders/ajax-element-move";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_elementMove( target_id );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_elementMove should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_folderDelete success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/folders/ajax-folder-delete";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_folderDelete( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_folderDelete should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_folderDelete error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/folders/ajax-folder-delete";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_folderDelete( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_folderDelete should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_reportDelete success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/folders/ajax-report-delete" + "/" + arr.id + "/";    // pk added to url as argument for decorator
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_reportDelete( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_reportDelete should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_reportDelete error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/folders/ajax-report-delete" + "/" + arr.id + "/";    // pk added to url as argument for decorator
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_reportDelete( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_reportDelete should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
} );
//=============================================================================
