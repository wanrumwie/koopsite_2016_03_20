/*
Global:  $ (?), JSON (?), QUnit (?), TR_start (?), auxiliary_handler, columnsNumber, create_qs_TR_arr (?), display_qs_TR_arr (?), expect (?), getRowIndexbyID (?), getSelRowIndex (?), getTRbyID (?), getTRbyIndex (?), getTRfromTbodyByIndex (?), get_m_id_n_ByIndex (?), get_qs_TR_arr (?), markSelRow (?), onClick_handler (?), onDblclick_handler (?), onKeyDown (?), onKeydown_handler (?), qs_TR_arr (?), restore_qs_TR_arr (?), rowsNumber (?), selElement (?), selRowFocus (?), selRowIndex (?), selTR (?), selectRow (?), selectStyle (?), setSelRow (?), setStartRow (?), set_browtab_listeners (?), sinon (?), storeSelRowIndex (?), stub, window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test
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
var columnsNumber = 2;
//=============================================================================
QUnit.module( "browtab_ajax document ready", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var $tbody;
    var selRowIndex_selector;
    var target_selector;
    var saved_csrf_token;
    hooks.beforeEach( function( assert ) {
        stub = {};
        target_selector = "#td_qwerty";
        selRowIndex_selector  = "#selRowIndex";
        $selRowIndex          = $( selRowIndex_selector );
        set_browtab_ajax_listeners(); 
        saved_csrf_token = $( "#csrfmiddlewaretoken" ).val();
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
        assert.equal( res, undefined, 'browtab_ajax_document_ready_handler should return false' );
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
        assert.equal( res, undefined, 'set_browtab_ajax_listeners should return false' );
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
