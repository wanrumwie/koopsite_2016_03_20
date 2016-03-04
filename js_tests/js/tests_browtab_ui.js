/*
Global:  $ (?), JSON (?), QUnit (?), TR_start (?), auxiliary_handler, browtab_document_ready_handler (?), changeSelElement (?), columnsNumber, create_qs_TR_arr (?), deleteElement (?), display_qs_TR_arr (?), expect (?), getRowIndexbyID (?), getSelRowIndex (?), getSelectorTR (?), getTRbyID (?), getTRbyIndex (?), getTRfromTbodyByIndex (?), getVisibleIndex (?), get_m_id_n_ByIndex (?), get_qs_TR_arr (?), markSelRow (?), normalStyle (?), onClick_handler (?), onDblclick_handler (?), onKeyDown (?), onKeydown_handler (?), qs_TR_arr (?), restore_qs_TR_arr (?), rowsNumber (?), scrollToRow (?), selElement (?), selRowFocus (?), selRowIndex (?), selTR (?), selectRow (?), selectStyle (?), setSelRow (?), setStartRow (?), setValToHTML, setValToHTMLrow (?), set_browtab_listeners (?), sinon (?), storeSelRowIndex (?), stub, totalOuterHeight (?), window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "browtab_ui document ready", function( hooks ) { 
//    var $tbody;
//    var tbody_selector;
//    var target_selector;
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'browtab_ui_document_ready_handler', function ( assert ) {
        expect( 6 );
        stub.add_browtab_ui_dialogs = sinon.stub( window, "add_browtab_ui_dialogs" );
        var res = browtab_ui_document_ready_handler( );
        assert.deepEqual( $dialog_box_form , $( "#dialog-box-form" ), "js file set proper value to $dialog_box_form" );
        assert.deepEqual( $dialog_confirm  , $( "#dialog-confirm" ), "js file set proper value to $dialog_confirm" );
        assert.deepEqual( $dialog_message  , $( "#dialog-message" ), "js file set proper value to $dialog_message" );
        assert.ok( stub.add_browtab_ui_dialogs.calledOnce, 'add_browtab_ui_dialogs should be called once' );
        assert.ok( stub.add_browtab_ui_dialogs.calledWithExactly( ), 'add_browtab_ui_dialogs should be called with arg' );
        assert.equal( res, undefined, 'browtab_ui_document_ready_handler should return false' );
    });
    QUnit.test( 'add_browtab_ui_dialogs', function ( assert ) {
        expect( 13 );
        browtab_ui_document_ready_handler( );

        stub.dialog_box_form = sinon.stub( $dialog_box_form, "dialog" );
        stub.dialog_confirm  = sinon.stub( $dialog_confirm, "dialog" );
        stub.dialog_message  = sinon.stub( $dialog_message, "dialog" );

        stub.dialog_width                       = sinon.stub( window, "dialog_width" ).returns( 400 );
        stub.get_dialog_default_buttons         = sinon.stub( window, "get_dialog_default_buttons" ).returns( 'buttons' );
        stub.get_confirm_dialog_default_buttons = 
                                    sinon.stub( window, "get_confirm_dialog_default_buttons" ).returns('confirm_buttons');   

        var arr1 = {    // main dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            width:          400,
            open:           set_Ok_button_on_Enter,
            close:          selRowFocus,
            buttons:        "buttons"   // no comma - last item in array
        };
        var arr2 = {     // confirm dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            width:          320,
            buttons:        "confirm_buttons"   // no comma - last item in array
        };
        var arr3 = {     // message dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            close:          selRowFocus,
            buttons:        { Ok: dialog_close }   // no comma - last item in array
        };

        var res = add_browtab_ui_dialogs( );

        assert.ok( stub.dialog_box_form.calledOnce, 'dialog_box_form should be called once' );
        assert.ok( stub.dialog_confirm.calledOnce, 'dialog_confirm should be called once' );
        assert.ok( stub.dialog_message.calledOnce, 'dialog_message should be called once' );

        assert.ok( stub.dialog_box_form.calledWithExactly( arr1 ), 'dialog_box_form should be called with arg' );
        assert.ok( stub.dialog_confirm.calledWithExactly( arr2 ), 'dialog_confirm should be called with arg' );
        assert.ok( stub.dialog_message.calledWithExactly( arr3 ), 'dialog_message should be called with arg' );

        assert.ok( stub.dialog_width.calledTwice, 'dialog_width should be called twice' );
        assert.ok( stub.dialog_width.alwaysCalledWithExactly( ), 'dialog_width should be called with arg' );
        assert.ok( stub.get_dialog_default_buttons.calledOnce, 'get_dialog_default_buttons should be called once' );
        assert.ok( stub.get_dialog_default_buttons.calledWithExactly( ), 
                                                                'get_dialog_default_buttons should be called with arg' );
        assert.ok( stub.get_confirm_dialog_default_buttons.calledOnce, 
                                                                'get_confirm_dialog_default_buttons should be called once' );
        assert.ok( stub.get_confirm_dialog_default_buttons.calledWithExactly( ), 
                                                            'get_confirm_dialog_default_buttons should be called with arg' );

        assert.equal( res, undefined, 'add_browtab_ui_dialogs should return false' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        // stubbing callback functions before they will be setted as parameters in dialogs:
        stub.set_Ok_button_on_Enter = sinon.stub( window, "set_Ok_button_on_Enter" );
        stub.selRowFocus            = sinon.stub( window, "selRowFocus" );
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'dialog_width 400px', function ( assert ) {
        expect( 3 );
        stub.width = sinon.stub( $tbody, "width" ).returns( 400 );
        var res = dialog_width();
        assert.ok( stub.width.calledOnce, 'width should be called once' );
        assert.ok( stub.width.calledWithExactly( ), 'width should be called with arg' );
        assert.equal( res, 400 * 0.75, 'width should return proper value' );
    });
    QUnit.test( 'dialog_width 600px', function ( assert ) {
        expect( 3 );
        stub.width = sinon.stub( $tbody, "width" ).returns( 600 );
        var res = dialog_width();
        assert.ok( stub.width.calledOnce, 'width should be called once' );
        assert.ok( stub.width.calledWithExactly( ), 'width should be called with arg' );
        assert.equal( res, 450, 'width should return proper value' );
    });
    QUnit.test( 'dialog_close', function ( assert ) {
        expect( 4 );
        
        stub.dialog = sinon.spy( jQuery.prototype, "dialog" );

        var res = dialog_close.call( $dialog_box_form );

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWithExactly( 'close' ), 'dialog should be called with args' );

        assert.equal( res, undefined, 'dialog_close should return undefined' );
    });
    QUnit.test( 'dialog_close functional test', function ( assert ) {
        // Check if onClose callback function, i.e. selRowFocus() is called and dialog is really closed.
        expect( 5 );
	    $dialog_box_form.dialog( "open" );
	    var isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.ok( isOpen, 'dialog should be open before test' );
        assert.ok( stub.set_Ok_button_on_Enter.calledOnce, 'set_Ok_button_on_Enter should be called once' );
        
        var res = dialog_close.call( $dialog_box_form );

        isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.notOk( isOpen, 'dialog should be closed after dialog_close.call' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.equal( res, undefined, 'dialog_close should return undefined' );
    });
    QUnit.test( 'dialog_box_form_close', function ( assert ) {
        expect( 2 );
        
        stub.dialog = sinon.spy( $dialog_box_form, "dialog" );

        var res = dialog_box_form_close( );

        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWithExactly( 'close' ), 'dialog should be called with args' );

    });
    QUnit.test( 'defineAbortButton', function ( assert ) {
        expect( 13 );
        var buttons = [
            {
                text  : "Abort loading",
                click : function( e ) {
                            dialog_box_form_close();
                            xhr.abort();
                            return false;
                }
            }
        ];

        var xhr = new XMLHttpRequest();
	    $dialog_box_form.dialog( "open" );
	    var isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.ok( isOpen, 'dialog should be open before test' );
        assert.ok( stub.set_Ok_button_on_Enter.calledOnce, 'set_Ok_button_on_Enter should be called once' );

        stub.dialog                 = sinon.spy( $dialog_box_form, "dialog" );
        stub.dialog_box_form_close  = sinon.spy( window, "dialog_box_form_close" );
        stub.abort                  = sinon.stub( xhr, "abort" );

        var res = defineAbortButton( xhr );

        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWith( "option", "buttons" ), 'dialog should be called with arg' );
        assert.deepEqual( stub.dialog.args[0][2][0].text, buttons[0].text, 'dialog should be called with text arg' );
        assert.equal( trim_all_spaces( stub.dialog.args[0][2][0].click ), 
                      trim_all_spaces( buttons[0].click ), 'dialog should be called with click arg' );

        assert.equal( res, undefined, 'defineAbortButton should return proper value' );

        // Simulation of button click:
        $dialog_box_form.parent().find( "button:contains('Abort loading')" ).trigger( "click" );
        assert.ok( stub.dialog_box_form_close.callCount, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 
                                                                'dialog_box_form_close should be called with arg' );
        assert.ok( stub.abort.callCount, 'abort should be called once' );
        assert.ok( stub.abort.calledWithExactly( ), 'abort should be called with arg' );

        isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.notOk( isOpen, 'dialog should be closed after dialog_box_form_close() call' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
    });
} );
function trim_all_spaces( f ){
    var s = String( f ).replace( / /g, '' );
    return s;
}
//=============================================================================
QUnit.module( "browtab_ui functions 2", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'get_dialog_default_buttons', function ( assert ) {
        expect( 1 );
        var expected = [
            { text: "Ok",       click: undefined },
            { text: "Cancel",   click: dialog_close }
        ];
        var res = get_dialog_default_buttons();
        assert.deepEqual( res, expected, 'get_dialog_default_buttons should return proper value' );
    });
    QUnit.test( 'get_confirm_dialog_default_buttons', function ( assert ) {
        expect( 1 );
        var expected = [
            { text: "Ok",       click: undefined },
            { text: "Cancel",   click: dialog_close }
        ];
        var res = get_confirm_dialog_default_buttons();
        assert.deepEqual( res, expected, 'get_confirm_dialog_default_buttons should return proper value' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui click_Ok_button_on_Enter", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
        $dialog_box_form.dialog( "open" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        $dialog_box_form.dialog( "close" );
    } );
    QUnit.test( 'Enter key', function ( assert ) {
        expect( 8 );
        var e = {};
        e.keyCode = $.ui.keyCode.ENTER;

        var buttons = { Ok: undefined };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        stub.parent = sinon.spy( jQuery.prototype, "parent" );
        stub.find   = sinon.spy( jQuery.prototype, "find" );
        stub.trigger = sinon.stub( jQuery.prototype, "trigger" );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.deepEqual( stub.parent.thisValues[0], $dialog_box_form, 'parent called as method of proper this' );
        assert.equal( stub.parent.callCount, 1, 'parent should be called once' );
        assert.ok( stub.parent.calledWithExactly( ), 'parent should be called with arg' );
        assert.equal( stub.find.callCount, 1, 'find should be called once' );
        assert.ok( stub.find.calledWithExactly( "button:contains('Ok')" ), 'find should be called with arg' );
        assert.equal( stub.trigger.callCount, 1, 'trigger should be called once' );
        assert.ok( stub.trigger.calledWithExactly( "click" ), 'trigger should be called with arg' );

        assert.equal( res, false, 'click_Ok_button_on_Enter should return false' );
    });
    QUnit.test( 'Not Enter key', function ( assert ) {
        expect( 4 );
        var e = {};
        e.keyCode = $.ui.keyCode.LEFT;

        var buttons = { Ok: undefined };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        stub.parent = sinon.spy( jQuery.prototype, "parent" );
        stub.find   = sinon.spy( jQuery.prototype, "find" );
        stub.trigger = sinon.stub( jQuery.prototype, "trigger" );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.equal( stub.parent.callCount, 0, 'parent should not be called' );
        assert.equal( stub.find.callCount, 0, 'find should not be called' );
        assert.equal( stub.trigger.callCount, 0, 'trigger should not be called' );

        assert.equal( res, undefined, 'click_Ok_button_on_Enter should return undefined' );
    });
    QUnit.test( 'Enter key functional', function ( assert ) {
        expect( 2 );
        var e = {};
        e.keyCode = $.ui.keyCode.ENTER;

        var callback = sinon.spy();

        var buttons = { Ok: callback };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.ok( callback.calledOnce, 'callback should be called once' );
        assert.equal( res, false, 'click_Ok_button_on_Enter should return false' );
        $dialog_box_form.dialog( "close" );
    });
    QUnit.test( 'not Enter key functional', function ( assert ) {
        expect( 2 );
        var e = {};
        e.keyCode = $.ui.keyCode.LEFT;

        var callback = sinon.spy();

        var buttons = { Ok: callback };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.notOk( callback.called, 'callback should not be called' );
        assert.equal( res, undefined, 'click_Ok_button_on_Enter should return undefined' );
    });
    QUnit.test( 'set_Ok_button_on_Enter', function ( assert ) {
        expect( 3 );

        stub.keypress = sinon.spy( $dialog_box_form, "keypress" );
        stub.click_Ok_button_on_Enter = sinon.stub( window, "click_Ok_button_on_Enter" );

        var res = set_Ok_button_on_Enter.call( $dialog_box_form );
        $dialog_box_form.keypress();

        assert.ok( stub.keypress.calledOnce, 'keypress should be called once' );
        assert.ok( stub.click_Ok_button_on_Enter.calledOnce, 'click_Ok_button_on_Enter should be called once' );
        assert.equal( res, undefined, 'set_Ok_button_on_Enter should return undefined' );
    });
} );
//=============================================================================
QUnit.test( 'js file start assignments', function ( assert ) {
    assert.equal( nameFormLabel , '<label for="id_name">Тека:</label>');
    assert.equal( nameFormInput , '<input id="id_name" maxlength="256" name="name" type="text" autofocus/>');
    assert.equal( nameFormTR    , '<td>' + nameFormLabel + '</td>' +
                                  '<td>' + nameFormInput + '</td>');
    assert.equal( fileFormLabel , '<label for="id_file">Файл:</label>');
    assert.equal( fileFormInput , '<input id="id_file" maxlength="256" name="file" type="file" autofocus/>');
    assert.equal( fileFormTR    , '<td>' + fileFormLabel + '</td>' +
                                  '<td>' + fileFormInput + '</td>');
    assert.equal( condFormLabel , '<label for="id_cond">Повідомити ч/з email</label>');
    assert.equal( condFormInput , '<input id="id_cond" name="cond" type="checkbox"/>');
    assert.equal( condFormTR    , '<td>' + '</td>' +
                                  '<td>' + condFormLabel + condFormInput + '</td>');
    assert.equal( progressTR    , '<td>Progress:</td><td><div id="progressbar"></div></td>');
    assert.equal( emptyFormTR   , '<td></td><td></td>');
});
//=============================================================================
QUnit.module( "browtab_ui progress", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'progressbarShow', function ( assert ) {
        expect( 7 );
    
        stub.find        = sinon.spy( jQuery.prototype, "find" );
        stub.html        = sinon.spy( jQuery.prototype, "html" );
        stub.progressbar = sinon.spy( jQuery.prototype, "progressbar" );

        var res = progressbarShow();

        assert.equal( stub.find.callCount, 1, 'find should be called once' );
        assert.ok( stub.find.calledWithExactly( "tr:nth-child(2)" ), 'find should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called once' );
        assert.ok( stub.html.calledWithExactly( progressTR ), 'html should be called with arg' );
        assert.equal( stub.progressbar.callCount, 1, 'progressbar should be called once' );
        assert.ok( stub.progressbar.calledWithExactly( { value: 0 } ), 'html should be called with arg' );
        assert.equal( res, undefined, 'progressbarShow should return undefined' );
    });
    QUnit.test( 'setProgress #1', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = 200;
        var pmax = 300;
        var arr = { value: 5, max: 200 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ), 
                                                                            '0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ), 
                                                                            '1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), 
                                                                            '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'setProgress #2', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = 200;
        var pmax = undefined;
        var arr = { value: 5, max: 200 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ), 
                                                                            '0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ), 
                                                                            '1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), 
                                                                            '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'setProgress #3', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = undefined;
        var pmax = 300;
        var arr = { value: 5, max: 300 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ), 
                                                                            '0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ), 
                                                                            '1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), 
                                                                            '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'setProgress #4', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = undefined;
        var pmax = undefined;
        var arr = { value: 5, max: 100 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ),'0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ),'1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'progressHandler true', function ( assert ) {
        expect( 3 );
        var pe = {};
        pe.lengthComputable = true;
        pe.loaded = 'load';
        pe.total  = 'total';

        stub.setProgress = sinon.stub( window, "setProgress" );

        var res = progressHandler( pe );

        assert.equal( stub.setProgress.callCount, 1, 'setProgress should be called ones' );
        assert.ok( stub.setProgress.calledWithExactly( pe.loaded, pe.total ), 'setProgress should be called with arg' );
        assert.equal( res, undefined, 'progressHandler should return undefined' );
    });
    QUnit.test( 'progressHandler false', function ( assert ) {
        expect( 3 );
        var pe = {};
        pe.lengthComputable = false;
        pe.loaded = 'load';
        pe.total  = 'total';

        stub.setProgress = sinon.stub( window, "setProgress" );

        var res = progressHandler( pe );

        assert.equal( stub.setProgress.callCount, 1, 'setProgress should be called ones' );
        assert.ok( stub.setProgress.calledWithExactly( false ), 'setProgress should be called with arg' );
        assert.equal( res, undefined, 'progressHandler should return undefined' );
    });
    QUnit.test( 'loadEndHandler', function ( assert ) {
        expect( 3 );
        var pe = {};
        pe.loaded = 'load';

        stub.setProgress = sinon.stub( window, "setProgress" );

        var res = loadEndHandler( pe );

        assert.equal( stub.setProgress.callCount, 1, 'setProgress should be called ones' );
        assert.ok( stub.setProgress.calledWithExactly( pe.loaded ), 'setProgress should be called with arg' );
        assert.equal( res, undefined, 'loadEndHandler should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui dialogMessage", function( hooks ) { 
    var clock;
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'get_dlgClass', function ( assert ) {
        expect( 5 );
        assert.equal( get_dlgClass( "IncorrectData") , "no-close ui-state-error" );
        assert.equal( get_dlgClass( "Forbidden"    ) , "no-close ui-state-error" );
        assert.equal( get_dlgClass( "Error"        ) , "no-close ui-state-error" );
        assert.equal( get_dlgClass( "Normal"       ) , "no-close ui-state-highlight" );
        assert.equal( get_dlgClass( ""             ) , "no-close ui-state-highlight" );
    });
    QUnit.test( '#1', function ( assert ) {
        expect( 13 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = "title";
        var time = 100;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 2, 'setTimeout should be called 1 + 1 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.deepEqual( trim_all_spaces( stub.setTimeout.args[1][0] ), 
                          trim_all_spaces( timeout_arg ), 'setTimeout should be called with 0. arg' );
        assert.deepEqual( stub.setTimeout.args[1][1], time, 'setTimeout should be called with 1. arg' );
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 4, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "option", "title", title ),          '2 dialog arg' );
        assert.ok( stub.dialog.getCall( 3 ).calledWithExactly( "close" ),                           '3 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
    });
    QUnit.test( '#2', function ( assert ) {
        expect( 12 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = undefined;
        var time = 100;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 2, 'setTimeout should be called 1 + 1 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.deepEqual( trim_all_spaces( stub.setTimeout.args[1][0] ), 
                          trim_all_spaces( timeout_arg ), 'setTimeout should be called with 0. arg' );
        assert.deepEqual( stub.setTimeout.args[1][1], time, 'setTimeout should be called with 1. arg' );
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "close" ),                           '3 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
    });
    QUnit.test( '#3', function ( assert ) {
        expect( 10 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = "title";
        var time = undefined;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 1, 'setTimeout should be called 1 + 0 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "option", "title", title ),          '2 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
        $dialog_message.dialog( "close" );
    });
    QUnit.test( '#4', function ( assert ) {
        expect( 10 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = "title";
        var time = -1;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 1, 'setTimeout should be called 1 + 0 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "option", "title", title ),          '2 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
        $dialog_message.dialog( "close" );
    });
    QUnit.test( '#5', function ( assert ) {
        expect( 9 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = undefined;
        var time = undefined;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 1, 'setTimeout should be called 1 + 0 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 2, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
        $dialog_message.dialog( "close" );
    });
    QUnit.test( 'folderEmptyMessage', function ( assert ) {
        expect( 3 );

        var f_name = "f_name";
        stub.dialogMessage = sinon.stub( window, "dialogMessage" );

        var res = folderEmptyMessage( f_name );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "Ця тека порожня.", "", f_name, 1000 ), 
                                                                        'dialogMessage should be called with arg' );
        assert.equal( res, undefined, 'folderEmptyMessage should return undefined' );
    });
    QUnit.test( 'noSelectionMessage', function ( assert ) {
        expect( 3 );

        var f_name = "f_name";
        stub.dialogMessage = sinon.stub( window, "dialogMessage" );

        var res = noSelectionMessage( f_name );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "Нічого не вибрано!", "Error", f_name, 1000 ), 
                                                                        'dialogMessage should be called with arg' );
        assert.equal( res, undefined, 'noSelectionMessage should return undefined' );
    });
    QUnit.test( 'functionOnDevelopeMessage', function ( assert ) {
        expect( 3 );

        stub.dialogMessage = sinon.stub( window, "dialogMessage" );

        var res = functionOnDevelopeMessage( );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( 
                                        "Ця процедура ще розробляється...", "", "", 2000 ), 
                                                                        'dialogMessage should be called with arg' );
        assert.equal( res, undefined, 'functionOnDevelopeMessage should return undefined' );
    });
} );

//=============================================================================
