/*
Global:  QUnit (?), expect (?), getSelRowIndex (?), rowsNumber (?)
*/

/********************************************************************/


/********************************************************************/

//QUnit.config.reorder = false;

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

var stub, selector;
QUnit.module( "browtab functions tests", {
    beforeEach: function () {
        selector = "#browtable tbody td";
//        selector = "#browtable thead";
        set_browtab_listeners(); 
    },
    afterEach: function () {
        if ( stub ) {
            stub.restore();
        }
    }
});

//-----------------------------------------------------------------------------

QUnit.test( '$( ... ).on( "click",... STUB onClick_func', function ( assert ) {
    stub = sinon.stub( window, "onClick_func" );
    $( selector ).trigger( 'click' );
    assert.equal( stub.calledOnce, true, 'onClick_func should be called once' );
});

//-----------------------------------------------------------------------------

QUnit.test( '$( ... ).on( "click",... STUB selectRow', function ( assert ) {
    stub = sinon.stub( window, "selectRow" );
    $( selector ).trigger( 'click' );
    assert.equal( stub.calledOnce, true, 'selectRow should be called once' );
});

QUnit.test( '$( ... ).on( "click",... STUB selectRow 2', function ( assert ) {
    stub = sinon.stub( window, "selectRow" );
    $( selector ).trigger( 'click' );
    assert.equal( stub.calledOnce, true, 'selectRow should be called once' );
});

//-----------------------------------------------------------------------------

QUnit.test( 'onClick_func', function ( assert ) {
    var e = {                               // e is needed as onClick argument
        preventDefault: sinon.stub(),
        stopPropagation: sinon.stub()
    };
    stub = sinon.stub( window, "selectRow" );
    onClick_func( e );
    assert.equal( stub.calledOnce, true, 'selectRow should be called once' );
    assert.equal( e.preventDefault.calledOnce, true, 'event.preventDefault should be called once' );
});

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

QUnit.module( "browtab functions tests", {});

//-----------------------------------------------------------------------------

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
