/*
Global:  $ (?), QUnit (?), expect (?), getSelRowIndex (?), onClick_handler (?), onDblclick_handler (?), onKeydown_handler (?), rowsNumber (?), selector, set_browtab_listeners (?), sinon (?), stub, window (?)
*/

//QUnit.config.reorder = false;

//=============================================================================
var stub, selector;
QUnit.module( "browtab listeners", {
    beforeEach: function () {
        stub = {};
        selector = "#td_qwerty";
//        selector = "#browtable thead";
        set_browtab_listeners(); 
    },
    afterEach: function () {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    }
});
/*  It's impossible to stub function inside on():  $( ... ).on( ..., onClick_handler ) ?
QUnit.test( '$( ... ).on( "click",... STUB onClick_handler', function ( assert ) {
    stub = sinon.stub( window, "onClick_handler" );
    $( selector ).trigger( 'click' );
    assert.equal( stub.calledOnce, true, 'onClick_handler should be called once' );
});
*/
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
//=============================================================================

QUnit.module( "browtab sel row functions", {
    beforeEach: function () {
        stub = {};
    },
    afterEach: function () {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    }
});
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
    stub.getSelRowIndex = sinon.stub( window, "getSelRowIndex" );
    stub.getSelRowIndex.returns( 7 );
    stub.getTRbyIndex = sinon.stub( window, "getTRbyIndex" );
    stub.getTRbyIndex.returns( 9 );
    stub.scrollToRow = sinon.stub( window, "scrollToRow" );
    stub.markSelRow = sinon.stub( window, "markSelRow" );
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
    assert.equal( selRow, 9, 'setSelRow should set selRow value' );
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
    selRow = "#tr_qwerty";
    $( selRow ).find( 'A' ).blur();
    assert.notOk( $( "#a_qwerty" ).is(':focus'), 'proper <a> should not be focused before selRowFocus');
    var res = selRowFocus();
    assert.equal( res, undefined, 'selRowFocus should return undefined' );
    assert.ok( $( "#a_qwerty" ).is(':focus'), 'proper <a> should be focused');
});
QUnit.test( 'markSelRow', function ( assert ) {
    expect( 11 );
    selElement = undefined;
    stub.get_m_id_n_ByIndex = sinon.stub( window, "get_m_id_n_ByIndex" );
    stub.get_m_id_n_ByIndex.returns( { id: '0'} );
    stub.storeSelRowIndex = sinon.stub( window, "storeSelRowIndex" );
    stub.selRowFocus = sinon.stub( window, "selRowFocus" );
    selRow = "#tr_qwerty";
    assert.notOk( $( selRow ).is('.'+selectStyle), 'selRow should not be not selectStyled before markSelRow');
    var res = markSelRow();
    assert.notOk( $( "#tr_qwerty_s" ).is('.'+selectStyle), 'previous selRow should not be not selectStyled after markSelRow');
    assert.ok( $( selRow ).is('.'+selectStyle), 'selRow should be selectStyled after markSelRow');
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
    assert.equal( $( selRow )[0], $( "#tr_qwerty_s" )[0], 'selectRow should set selRow value' );
//
//    all prop identical except "selector":
//    var prop;
//    for ( prop in $( selRow ) ) {
//        if ( prop != "selector" ){
//            assert.equal( $( selRow )[prop], $( "#tr_qwerty_s" )[prop], 'selectRow should set selRow value' );
//        }
//    }
//    assert.deepEqual( $( selRow ), $( "#tr_qwerty_s" ), 'selectRow should set selRow value' );
});
//=============================================================================

QUnit.module( "browtab storeSelRowIndex", {
    beforeEach: function () {
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
    },
    afterEach: function () {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    }
});
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
function auxiliary_handler(){
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

//=============================================================================
QUnit.module( "browtab onKeyDown", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var arr = {};
    var tbody_tr_selector;
    var stub;
    hooks.beforeEach( function( assert ) {
        stub = {};
        tbody_tr_selector = "#browtable tbody tr";
        stub.runhref = sinon.stub( window, "runhref" );
        stub.getVisibleIndex = sinon.stub( window, "getVisibleIndex" );
        stub.getVisibleIndex.returns( arr );
        stub.setSelRow = sinon.stub( window, "setSelRow" );
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
