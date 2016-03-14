/*
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "folder_browtab_sort document ready", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        columnsNumber = 4;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'folder_browtab_sort_document_ready_handler', function ( assert ) {
        expect( 9 );

        stub.appendOrderButtons                         = sinon.stub( window, "appendOrderButtons" );
        stub.changeOrderIcon                            = sinon.stub( window, "changeOrderIcon" );
        stub.changeOrderGroupIcon                       = sinon.stub( window, "changeOrderGroupIcon" );
        stub.set_folder_browtab_sort_buttons_listeners  = sinon.stub( window, "set_folder_browtab_sort_buttons_listeners" );

        var res = folder_browtab_sort_document_ready_handler( );

        assert.ok( stub.appendOrderButtons.calledOnce, 'appendOrderButtons should be called once' );
        assert.ok( stub.appendOrderButtons.calledWithExactly( 1, columnsNumber ), 
                                                        'appendOrderButtons should be called with arg' );
        assert.ok( stub.changeOrderIcon.calledOnce, 'changeOrderIcon should be called once' );
        assert.ok( stub.changeOrderIcon.calledWithExactly( 2, 2, columnsNumber ), 
                                                        'changeOrderIcon should be called with arg' );
        assert.ok( stub.changeOrderGroupIcon.calledOnce, 'changeOrderGroupIcon should be called once' );
        assert.ok( stub.changeOrderGroupIcon.calledWithExactly( 1 ), 
                                                        'changeOrderGroupIcon should be called with arg' );
        assert.ok( stub.set_folder_browtab_sort_buttons_listeners.calledOnce, 
                                                        'set_folder_browtab_sort_buttons_listeners should be called once' );
        assert.ok( stub.set_folder_browtab_sort_buttons_listeners.calledWithExactly( ), 
                                                        'set_folder_browtab_sort_buttons_listeners should be called with arg' );

        assert.equal( res, undefined, 'folder_browtab_sort_document_ready_handler should return false' );
    });
    QUnit.test( 'set_folder_browtab_sort_buttons_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 19 );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = set_folder_browtab_sort_buttons_listeners( );

        assert.equal( stub.off.callCount, columnsNumber, 'off should be called columnsNumber times' );
        assert.equal( stub.on.callCount, columnsNumber, 'on should be called columnsNumber times' );

        var col;
        for ( col=1 ; col<=columnsNumber ; col++ ){
            assert.deepEqual( stub.off.thisValues[col-1], $( "#button-sort-"+col ), 
                                                                        col+': off called as method of proper this' );
            assert.deepEqual( stub.on.thisValues[col-1], $( "#button-sort-"+col ), 
                                                                        col+': on called as method of proper this' );
            assert.ok( stub.off.getCall( col-1 ).calledWithExactly( "click" ), col+':on called with args' );
            assert.ok( stub.on.getCall( col-1 ).calledWith( "click"), col+': off called with proper args' );
        }
        assert.equal( res, undefined, 'set_folder_browtab_sort_buttons_listeners should return false' );
    });
    QUnit.test( 'set_folder_browtab_sort_buttons_listeners functional', function ( assert ) {
        expect( 6 );

        stub.grouping = sinon.stub( window, "grouping" );
        stub.ordering = sinon.stub( window, "ordering" );

        appendOrderButtons( 1, columnsNumber );
        set_folder_browtab_sort_buttons_listeners( );

        var col, s;
        for ( col = 1 ; col <= columnsNumber ; col++ ){
            s = "#button-sort-" + col;
            $( s )[0].click();
        }

        assert.equal( stub.grouping.callCount, 1, 'grouping should be called 1 times' );
        assert.equal( stub.ordering.callCount, columnsNumber-1, 'ordering should be called columnsNumber-1 times' );
        col = 1;
        assert.deepEqual( stub.grouping.args[col-1], [ col ], 'grouping should be called with args' );
        for ( col = 2 ; col <= columnsNumber ; col++ ){
            assert.deepEqual( stub.ordering.args[col-2], [ col ], 'ordering should be called with args' );
        }
    });
} );
//=============================================================================
