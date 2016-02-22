/*
Global:  $ (?), JSON (?), QUnit (?), TR_start (?), auxiliary_handler, columnsNumber, create_qs_TR_arr (?), display_qs_TR_arr (?), expect (?), getRowIndexbyID (?), getSelRowIndex (?), getTRbyID (?), getTRbyIndex (?), getTRfromTbodyByIndex (?), get_m_id_n_ByIndex (?), get_qs_TR_arr (?), markSelRow (?), onClick_handler (?), onDblclick_handler (?), onKeyDown (?), onKeydown_handler (?), qs_TR_arr (?), restore_qs_TR_arr (?), rowsNumber (?), selElement (?), selRowFocus (?), selRowIndex (?), selTR (?), selectRow (?), selectStyle (?), setSelRow (?), setStartRow (?), set_browtab_listeners (?), sinon (?), storeSelRowIndex (?), stub, window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "browtab listeners", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var selector;
    hooks.beforeEach( function( assert ) {
        stub = {};
        selector = "#td_qwerty";
        set_browtab_listeners(); 
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'onClick_handler', function ( assert ) {
        expect( 3 );
        var e = {                               // e is needed as onClick argument
            currentTarget: sinon.stub()
        };
        stub.selectRow = sinon.stub( window, "selectRow" );
        var res = onClick_handler( e );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
        assert.ok( stub.selectRow.calledWith( e.currentTarget ), 'selectRow should be called with arg' );
        assert.equal( res, false, 'onClick_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "click",... STUB selectRow', function ( assert ) {
        expect( 1 );
        stub.selectRow = sinon.stub( window, "selectRow" );
        $( selector ).trigger( 'click' );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
    });
    QUnit.test( 'onDblclick_handler', function ( assert ) {
        expect( 5 );
        var e = {                               // e is needed as onClick argument
            currentTarget: sinon.stub()
        };
        stub.selectRow = sinon.stub( window, "selectRow" );
        stub.runhref = sinon.stub( window, "runhref" );
        var res = onDblclick_handler( e );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
        assert.ok( stub.selectRow.calledWith( e.currentTarget ), 'selectRow should be called with arg' );
        assert.ok( stub.runhref.calledOnce, 'runhref should be called once' );
        assert.ok( stub.runhref.calledWith(), 'runhref should be called with no arg' );
        assert.equal( res, false, 'onDblclick_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "dblclick",... STUB called func.', function ( assert ) {
        expect( 2 );
        stub.selectRow = sinon.stub( window, "selectRow" );
        stub.runhref = sinon.stub( window, "runhref" );
        $( selector ).trigger( 'dblclick' );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
        assert.ok( stub.runhref.calledOnce, 'runhref should be called once' );
    });
    QUnit.test( 'onKeydown_handler', function ( assert ) {
        expect( 3 );
        var e = {                               // e is needed as onClick argument
            which: sinon.stub()
        };
        stub.onKeyDown = sinon.stub( window, "onKeyDown" );
        var res = onKeydown_handler( e );
        assert.ok( stub.onKeyDown.calledOnce, 'onKeyDown should be called once' );
        assert.ok( stub.onKeyDown.calledWith( e.which ), 'onKeyDown should be called with arg' );
        assert.equal( res, false, 'onKeydown_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "keydown",... STUB onKeyDown', function ( assert ) {
        expect( 1 );
        stub.onKeyDown = sinon.stub( window, "onKeyDown" );
        $( selector ).trigger( $.Event( "keydown", { keyCode: 9 } ) );
        assert.ok( stub.onKeyDown.calledOnce, 'onKeyDown should be called once' );
    });
} );
/*  It's impossible to stub function inside on():  $( ... ).on( ..., onClick_handler ) ?
QUnit.test( '$( ... ).on( "click",... STUB onClick_handler', function ( assert ) {
    stub = sinon.stub( window, "onClick_handler" );
    $( selector ).trigger( 'click' );
    assert.equal( stub.calledOnce, true, 'onClick_handler should be called once' );
});
*/
//=============================================================================

QUnit.module( "browtab sel row functions", function( hooks ) { // This test described in tbody_hidden.xlsx file
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'setStartRow', function ( assert ) {
        expect( 6 );
        stub.setSelRow = sinon.stub( window, "setSelRow" );
        $( "#selRowIndex" ).val( 55 );
        var res = setStartRow();
        assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
        assert.ok( stub.setSelRow.calledWith( 55 ), 'selectRow should be called with arg' );
        assert.equal( res, undefined, 'setStartRow should return undefined' );

        stub.setSelRow.reset();
        $( "#selRowIndex" ).val( "" );
        res = setStartRow();
        assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
        assert.ok( stub.setSelRow.calledWith( 0 ), 'selectRow should be called with arg' );
        assert.equal( res, undefined, 'setStartRow should return undefined' );
    });
    QUnit.test( 'setSelRow', function ( assert ) {
        expect( 11 );
        stub.getSelRowIndex = sinon.stub( window, "getSelRowIndex" ).returns( 7 );
        stub.getTRbyIndex   = sinon.stub( window, "getTRbyIndex" ).returns( 9 );
        stub.scrollToRow    = sinon.stub( window, "scrollToRow" );
        stub.markSelRow     = sinon.stub( window, "markSelRow" );
        rowsNumber = 10;
        var res = setSelRow( 5 );
        assert.equal( res, undefined, 'setSelRow should return undefined' );
        rowsNumber = 0;
        res = setSelRow( 5 );
        assert.ok( stub.getSelRowIndex.calledOnce, 'getSelRowIndex should be called once' );
        assert.ok( stub.getSelRowIndex.calledWith( 5 ), 'getSelRowIndex should be called with arg' );
        assert.ok( stub.getTRbyIndex.calledOnce, 'getTRbyIndex should be called once' );
        assert.ok( stub.getTRbyIndex.calledWith( 7 ), 'getTRbyIndex should be called with arg' );
        assert.ok( stub.scrollToRow.calledOnce, 'scrollToRow should be called once' );
        assert.ok( stub.scrollToRow.calledWith( 7 ), 'scrollToRow should be called with arg' );
        assert.ok( stub.markSelRow.calledOnce, 'markSelRow should be called once' );
        assert.ok( stub.markSelRow.calledWith(), 'markSelRow should be called with arg' );
        assert.equal( res, undefined, 'setSelRow should return undefined' );
        assert.equal( selTR, 9, 'setSelRow should set selTR value' );
    });
    QUnit.test('getSelRowIndex', function ( assert ) {
        expect( 6 );
        rowsNumber = 10;
        assert.strictEqual( getSelRowIndex( -1 ), 0, 'sel row index min value must be 0');
        assert.strictEqual( getSelRowIndex(  5 ), 5, 'sel row index must be = 5');
        assert.strictEqual( getSelRowIndex( rowsNumber ), rowsNumber - 1, 'sel row index max value must be rowsNumber-1');
        rowsNumber = 0;
        assert.strictEqual( getSelRowIndex( -1 ), 0, 'sel row index must be 0 if rowsNumber=0');
        assert.strictEqual( getSelRowIndex(  0 ), 0, 'sel row index must be 0 if rowsNumber=0');
        assert.strictEqual( getSelRowIndex( 10 ), 0, 'sel row index must be 0 if rowsNumber=0');
    });
    QUnit.test('selRowFocus', function ( assert ) {
        expect( 3 );
        selTR = "#tr_qwerty";
        $( selTR ).find( 'A' ).blur();
        assert.notOk( $( "#a_qwerty" ).is(':focus'), 'proper <a> should not be focused before selRowFocus');
        var res = selRowFocus();
        assert.equal( res, undefined, 'selRowFocus should return undefined' );
        assert.ok( $( "#a_qwerty" ).is(':focus'), 'proper <a> should be focused');
    });
    QUnit.test( 'markSelRow', function ( assert ) {
        expect( 11 );
        selElement = undefined;
        stub.get_m_id_n_ByIndex = sinon.stub( window, "get_m_id_n_ByIndex" ).returns( { id: '0'} );
        stub.storeSelRowIndex   = sinon.stub( window, "storeSelRowIndex" );
        stub.selRowFocus        = sinon.stub( window, "selRowFocus" );
        selTR = "#tr_qwerty";
        assert.notOk( $( selTR ).is('.'+selectStyle), 'selTR should not be not selectStyled before markSelRow');
        var res = markSelRow();
        assert.notOk( $( "#tr_qwerty_s" ).is('.'+selectStyle), 'previous selTR should not be not selectStyled after markSelRow');
        assert.ok( $( selTR ).is('.'+selectStyle), 'selTR should be selectStyled after markSelRow');
        assert.ok( stub.get_m_id_n_ByIndex.calledOnce, 'get_m_id_n_ByIndex should be called once' );
        assert.ok( stub.get_m_id_n_ByIndex.calledWith( selRowIndex ), 'get_m_id_n_ByIndex should be called with arg' );
        assert.ok( stub.storeSelRowIndex.calledOnce, 'storeSelRowIndex should be called once' );
        assert.ok( stub.storeSelRowIndex.calledWith(), 'storeSelRowIndex should be called with arg' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.ok( stub.selRowFocus.calledWith(), 'selRowFocus should be called with arg' );
        assert.equal( res, false, 'markSelRow should return false' );
        assert.equal( selElement.id, '0', 'markSelRow should set selElement value' );
    });
    QUnit.test( 'selectRow', function ( assert ) {
        expect( 5 );
        var targ = "#td_qwerty_s";
        stub.markSelRow = sinon.stub( window, "markSelRow" );
        var res = selectRow( targ );
        assert.ok( stub.markSelRow.calledOnce, 'markSelRow should be called once' );
        assert.ok( stub.markSelRow.calledWith(), 'markSelRow should be called with arg' );
        assert.equal( res, false, 'selectRow should return false' );
        assert.equal( selRowIndex, 1, 'selectRow should set selRowIndex value' );
        assert.equal( $( selTR )[0], $( "#tr_qwerty_s" )[0], 'selectRow should set selTR value' );
    //
    //    All properties of $( selTR) object are identical with $( "#tr_qwerty_s" ) once except "selector":
    //    var prop;
    //    for ( prop in $( selTR ) ) {
    //        if ( prop != "selector" ){
    //            assert.equal( $( selTR )[prop], $( "#tr_qwerty_s" )[prop], 'selectRow should set selTR value' );
    //        }
    //    }
    //    This not works:
    //    assert.deepEqual( $( selTR ), $( "#tr_qwerty_s" ), 'selectRow should set selTR value' );
    });
} );
//=============================================================================

function auxiliary_handler(){
}
QUnit.module( "browtab storeSelRowIndex", function( hooks ) { // This test described in tbody_hidden.xlsx file
    hooks.beforeEach( function( assert ) {
        stub = {};
        $( '#selRowIndex' ).off( "change").on( "change", function() {
            auxiliary_handler();
            return false;
        });
        expect( 3 );
        stub.auxiliary_handler = sinon.stub( window, "auxiliary_handler" );
        selRowIndex = "1";
        selElement.model = 'folder';
        selElement.id = "55";
        auxiliary_set_val_to_html();
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    function auxiliary_set_val_to_html(){
        $( '#selRowIndex').val( selRowIndex );
        $( '#selElementModel' ).val( selElement.model );
        $( '#selElementID' ).val( selElement.id );
    }
    function auxiliary_get_val_from_html(){
        var ri = $( '#selRowIndex').val();
        var md = $( '#selElementModel' ).val();
        var id = $( '#selElementID' ).val();
        return [ri, md, id];
    }
    QUnit.test( '#1', function ( assert ) {
        selRowIndex = "2";
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.ok( stub.auxiliary_handler.calledOnce, 'on change handler should be called once' );
    });
    QUnit.test( '#2', function ( assert ) {
        selElement.model = 'user';
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.ok( stub.auxiliary_handler.calledOnce, 'on change handler should be called once' );
    });
    QUnit.test( '#3', function ( assert ) {
        selElement.id = '77';
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.ok( stub.auxiliary_handler.calledOnce, 'on change handler should be called once' );
    });
    QUnit.test( '#4', function ( assert ) {
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.notOk( stub.auxiliary_handler.called, 'on change handler should not be called' );
    });
} );

//=============================================================================
QUnit.module( "browtab onKeyDown", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var arr = {};
    var tbody_tr_selector;
    hooks.beforeEach( function( assert ) {
        stub = {};
        tbody_tr_selector = "#browtable tbody tr";
        stub.runhref         = sinon.stub( window, "runhref" );
        stub.getVisibleIndex = sinon.stub( window, "getVisibleIndex" ).returns( arr );
        stub.setSelRow       = sinon.stub( window, "setSelRow" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "Enter key", function( assert ) {
        expect( 5 );
        var k   = 13;    // key pressed code
        var res = onKeyDown( k );
        assert.ok( stub.runhref.calledOnce, 'runhref should be called once' );
        assert.ok( stub.runhref.calledWith(), 'runhref should be called with arg' );
        assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
        assert.notOk( stub.setSelRow.called, 'setSelRow should not be called' );
        assert.equal( res, false, 'onKeyDown should return false' );
    } );
    QUnit.test( "Improper key", function( assert ) {
        expect( 4 );
        var k   = 0;    // key pressed code
        var res = onKeyDown( k );
        assert.notOk( stub.runhref.called, 'runhref should not be called' );
        assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
        assert.notOk( stub.setSelRow.called, 'setSelRow should not be called' );
        assert.equal( res, false, 'onKeyDown should return false' );
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#1", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex = 10;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -2; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 3; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#2", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex =  8;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#3", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex = 13;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#4", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  2;    // index of first visible record
            arr.i_bot   =  7;    // index of last visible record
            selRowIndex =  2;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#5", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   = 15;    // index of first visible record
            arr.i_bot   = 20;    // index of last visible record
            selRowIndex = 20;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#6", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 5;    // number of all records
            arr.i_top   = 0;    // index of first visible record
            arr.i_bot   = 4;    // index of last visible record
            selRowIndex = 2;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -2; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 2; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#7", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 1;    // number of all records
            arr.i_top   = 0;    // index of first visible record
            arr.i_bot   = 0;    // index of last visible record
            selRowIndex = 0;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = 0; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 0; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#8", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex =  6;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 7; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#9", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex = 15;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -7; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWith( tbody_tr_selector ), 'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
} );
//=============================================================================
QUnit.module( "browtab qs_TR_arr functions", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var arr = {};
    hooks.beforeEach( function( assert ) {
        stub = {};
        arr.length = 55;
        stub.get_qs_TR_arr = sinon.stub( window, "get_qs_TR_arr" ).returns( arr );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "create_qs_TR_arr", function( assert ) {
        expect( 5 );
        var res = create_qs_TR_arr();
        assert.ok( stub.get_qs_TR_arr.calledOnce, 'get_qs_TR_arr should be called once' );
        assert.ok( stub.get_qs_TR_arr.calledWith( true ), 'get_qs_TR_arr should be called with arg' );
        assert.equal( qs_TR_arr, arr, 'create_qs_TR_arr should set value to global object' );
        assert.equal( rowsNumber, 55, 'create_qs_TR_arr should set value to global object' );
        assert.equal( res, undefined, 'create_qs_TR_arr should return undefined' );
    } );
    QUnit.test( "restore_qs_TR_arr", function( assert ) {
        expect( 5 );
        var res = restore_qs_TR_arr();
        assert.ok( stub.get_qs_TR_arr.calledOnce, 'get_qs_TR_arr should be called once' );
        assert.ok( stub.get_qs_TR_arr.calledWith( false ), 'get_qs_TR_arr should be called with arg' );
        assert.equal( qs_TR_arr, arr, 'restore_qs_TR_arr should set value to global object' );
        assert.equal( rowsNumber, 55, 'restore_qs_TR_arr should set value to global object' );
        assert.equal( res, undefined, 'restore_qs_TR_arr should return undefined' );
    } );
    QUnit.test( "getTRfromTbodyByIndex", function( assert ) {
        expect( 1 );
        var i = 1;
        var res = getTRfromTbodyByIndex( i );
        assert.equal( res[0], $( "#tr_qwerty_s" )[0], 'getTRfromTbodyByIndex should return proper value' );
    } );
} );

//=============================================================================
var columnsNumber;  // var declared in another js file, not in browtab.js 
QUnit.module( "browtab get_qs_TR_arr", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var i, j, TR;
    var expected_arr = [];   // 2D array - table
    var qs_obj = {};    // array stringified on server side
    var expected_TR_start = [];
    hooks.beforeEach( function( assert ) {
        stub = {};
        qs_obj = { 
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
        columnsNumber = 2;
        for ( i in qs_obj ) {
            expected_arr[i] = [];
            TR = getTRfromTbodyByIndex( i );    // already tested function
            TR_start[i] = TR;
            expected_TR_start[i] = TR;
            expected_arr[i][0] = qs_obj[i][0];
            expected_arr[i][0].TR = TR;
            for ( j = 1 ; j <= columnsNumber; j++ ) {
                expected_arr[i][j] = qs_obj[i][j];
            }
        }
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "is_start=true", function( assert ) {
        expect( 2 );
        TR_start = []; // clear array before this test
        var res = get_qs_TR_arr( true );
        assert.deepEqual( TR_start, expected_TR_start, 'get_qs_TR_arr should set value to global object' );
        assert.deepEqual( res, expected_arr, 'get_qs_TR_arr should return proper value' );
    } );
    QUnit.test( "is_start=false", function( assert ) {
        expect( 2 );
        var res = get_qs_TR_arr( false );
        assert.deepEqual( TR_start, expected_TR_start, 'get_qs_TR_arr should set value to global object' );
        assert.deepEqual( res, expected_arr, 'get_qs_TR_arr should return proper value' );
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "Get different data from qs_TR_arr", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            qs_TR_arr = get_qs_TR_arr( true ); // already tested function
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'getTRbyIndex', function ( assert ) {
            expect( 1 );
            qs_TR_arr[1][0].TR = 'qwerty';
            var res = getTRbyIndex( 1 );
            assert.equal( res, 'qwerty', 'getTRbyIndex should return proper value' );
        });
        QUnit.test( 'get_m_id_n_ByIndex', function ( assert ) {
            expect( 1 );
            var expected = {'id': '1', 'model': 'user', 'name': 'john'};
            var res = get_m_id_n_ByIndex( 1 );
            assert.deepEqual( res, expected, 'get_m_id_n_ByIndex should return proper value' );
        });
        QUnit.test( 'getRowIndexbyID', function ( assert ) {
            expect( 5 );
            assert.equal( getRowIndexbyID( 'user'  , 3 ), 0, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'user'  , 1 ), 1, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'folder', 3 ), 2, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'report', 3 ), 0, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'user'  , 9 ), 0, 'getRowIndexbyID should return proper value' );
        });
        QUnit.test( 'getTRbyID', function ( assert ) {
            expect( 5 );
            assert.equal( getTRbyID( 'user'  , 3 ), getTRbyIndex( 0 ), 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'user'  , 1 ), getTRbyIndex( 1 ), 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'folder', 3 ), getTRbyIndex( 2 ), 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'report', 3 ), undefined, 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'user'  , 9 ), undefined, 'getTRbyID should return proper value' );
        });
        QUnit.test( 'display_qs_TR_arr', function ( assert ) {
            rowsNumber = 3;
            expect( 17 + rowsNumber );
            selElement.model = 'qwerty';
            selElement.id    = 77;
            var tbody_selector = "#browtable tbody";
            var TR = "<tr><th>hello!</th></tr>";
            stub.getTRbyIndex       = sinon.stub( window, "getTRbyIndex" ).returns( TR );
            stub.getRowIndexbyID    = sinon.stub( window, "getRowIndexbyID" ).returns( 55 );
            stub.setSelRow          = sinon.stub( window, "setSelRow" );
            stub.get_m_id_n_ByIndex = sinon.stub( window, "get_m_id_n_ByIndex" ).returns( {m:'mm', i:99} );
            stub.storeSelRowIndex   = sinon.stub( window, "storeSelRowIndex" );
            stub.scrollToRow        = sinon.stub( window, "scrollToRow" );
            stub.selRowFocus        = sinon.stub( window, "selRowFocus" );

            var res = display_qs_TR_arr();
            
            assert.equal( $( "td", tbody_selector ).length, 0, "old rows cleared successfully!" );
            assert.equal( $( "th", tbody_selector ).length, rowsNumber, "new rows added successfully!" );

            assert.equal( stub.getTRbyIndex.callCount, rowsNumber, 'getTRbyIndex should be called '+rowsNumber+' times' );
            for ( i = 0 ; i < rowsNumber ; i++ ) {
                assert.ok( stub.getTRbyIndex.calledWith( i ), 'getTRbyIndex should be called with i='+i );
            }
            assert.ok( stub.getRowIndexbyID.calledOnce, 'getRowIndexbyID should be called once' );
            assert.ok( stub.getRowIndexbyID.calledWith( 'qwerty', 77 ), 'getRowIndexbyID should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWith( 55 ), 'setSelRow should be called with arg' );
            assert.ok( stub.get_m_id_n_ByIndex.calledOnce, 'get_m_id_n_ByIndex should be called once' );
            assert.ok( stub.get_m_id_n_ByIndex.calledWith( 55 ), 'get_m_id_n_ByIndex should be called with arg' );
            assert.ok( stub.storeSelRowIndex.calledOnce, 'storeSelRowIndex should be called once' );
            assert.ok( stub.storeSelRowIndex.calledWith(), 'storeSelRowIndex should be called with arg' );
            assert.ok( stub.scrollToRow.calledOnce, 'scrollToRow should be called once' );
            assert.ok( stub.scrollToRow.calledWith( 55 ), 'scrollToRow should be called with arg' );
            assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
            assert.equal( selRowIndex, 55, 'display_qs_TR_arr should set value to global selRowIndex' );
            assert.deepEqual( selElement, {m:'mm', i:99}, 'display_qs_TR_arr should set value to global selElement' );
            assert.equal( res, undefined, 'display_qs_TR_arr should return proper value' );
        });
    } );
} );
//=============================================================================
QUnit.module( "Scrolling", function( hooks ) { // This test described in tbody_hidden.xlsx file
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'getSelectorTR', function ( assert ) {
        expect( 1 );
        var qq = 55, i = 77;
        var s = "#browtable tbody tr:" + qq + "(" + i + ")" ;
        var res = getSelectorTR( qq, i );
        assert.equal( res, s, 'getSelectorTR should return proper value' );
    });
    //-------------------------------------------------------------------------
    QUnit.module( "getVisibleIndex", function( hooks ) {
        var hi, tbody;
        var tbody_selector = "#browtable tbody";
        var tbody_tr_selector = "#browtable tbody tr";
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            rowsNumber = 20;
            tbody = $( tbody_selector )
            $( tbody_tr_selector ).remove(); // removing all <TR> from table
            var i, TR;
            for ( i = 0 ; i < rowsNumber ; i++ ) {    // adding all new <TR> to table
                TR = "<tr><td>" + i + "</td></tr>";
                $( tbody_selector ).append( TR ); 
            }
            hi = $( tbody_tr_selector ).outerHeight();   // height of i-th element
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( '#1', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.0;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
console.log('expected:', expected);            
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#2', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 1;
            var i_bot = 10;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.0;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#3', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 10;
            var i_bot = 19;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.0;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#4', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.40;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#5', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.60;
            h_tbody  -= hi * 0.40;
            expected.i_top = i_top + 1;
            expected.i_bot = i_bot + 0;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#6', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 1;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.000;
            h_tbody  += hi * 0.40;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#7', function ( assert ) {
            expect( 6 );
            var expected = {};
            var i_top = 1;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.000;
            h_tbody  += hi * 0.60;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 1;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#8', function ( assert ) {
            expect( 6 );
            $( tbody_tr_selector ).remove(); // removing all <TR> from table
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.00;
            h_tbody  += hi * 0.00;
            expected.i_top = undefined;
            expected.i_bot = undefined;

            stub.scrollTop = sinon.stub( tbody, "scrollTop" ).returns( h_hidden );
            stub.height = sinon.stub( tbody, "height" ).returns( h_tbody );
            var res = getVisibleIndex( tbody_tr_selector, tbody );
            assert.equal( $( "td", tbody_selector ).length, 0, "no rows shoild be in this test!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWith(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWith(), 'height should be called with arg' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
    } );
} );
//=============================================================================
