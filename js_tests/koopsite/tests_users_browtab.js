/*
Global:  $ (?), JSON (?), QUnit (?), TR_start (?), auxiliary_handler, browtab_document_ready_handler (?), changeSelElement (?), columnsNumber, create_qs_TR_arr (?), deleteElement (?), display_qs_TR_arr (?), expect (?), getRowIndexbyID (?), getSelRowIndex (?), getSelectorTR (?), getTRbyID (?), getTRbyIndex (?), getTRfromTbodyByIndex (?), getVisibleIndex (?), get_m_id_n_ByIndex (?), get_qs_TR_arr (?), markSelRow (?), normalStyle (?), onClick_handler (?), onDblclick_handler (?), onKeyDown (?), onKeydown_handler (?), qs_TR_arr (?), restore_qs_TR_arr (?), rowsNumber (?), scrollToRow (?), selElement (?), selRowFocus (?), selRowIndex (?), selTR (?), selectRow (?), selectStyle (?), setSelRow (?), setStartRow (?), setValToHTML, setValToHTMLrow (?), set_browtab_listeners (?), sinon (?), storeSelRowIndex (?), stub, totalOuterHeight (?), window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

var qs_TR_arr;  // var declared in another file
QUnit.test( 'js file start assignments', function ( assert ) {
    expect( 1 );
    assert.deepEqual( columnsNumber, 8, 'columnsNumber should be set immediately after page loaded');
});
//=============================================================================
QUnit.module( "users_browtab getLoginNameFlatbyIndex", function( hooks ) { // This test described in tbody_hidden.xlsx file
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( '#1', function ( assert ) {
        expect( 1 );
        qs_TR_arr = [ [ {}, 'john', 'Lennon John', '25a'] ];
        var expected = "john (Lennon John, кв.25a)";
        var res = getLoginNameFlatbyIndex( 0 );
        assert.equal( res, expected, 'getLoginNameFlatbyIndex should return proper value' );
    });
    QUnit.test( '#2', function ( assert ) {
        expect( 1 );
        qs_TR_arr = [ [ {}, 'john', '', '25a'] ];
        var expected = "john (кв.25a)";
        var res = getLoginNameFlatbyIndex( 0 );
        assert.equal( res, expected, 'getLoginNameFlatbyIndex should return proper value' );
    });
    QUnit.test( '#3', function ( assert ) {
        expect( 1 );
        qs_TR_arr = [ [ {}, 'john', 'Lennon John', ''] ];
        var expected = "john (Lennon John)";
        var res = getLoginNameFlatbyIndex( 0 );
        assert.equal( res, expected, 'getLoginNameFlatbyIndex should return proper value' );
    });
    QUnit.test( '#4', function ( assert ) {
        expect( 1 );
        qs_TR_arr = [ [ {}, 'john', '', ''] ];
        var expected = "john";
        var res = getLoginNameFlatbyIndex( 0 );
        assert.equal( res, expected, 'getLoginNameFlatbyIndex should return proper value' );
    });
    QUnit.test( 'getElementNamebyIndex', function ( assert ) {
        expect( 3 );
        var i = 55;
        var expected = "john";
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( expected );
        var res = getElementNamebyIndex( i );
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWith( i ), 'getLoginNameFlatbyIndex should be called with arg' );
        assert.equal( res, expected, 'getLoginNameFlatbyIndex should return proper value' );
    });
} );
//=============================================================================
function auxiliary_get_html_selectors( i ){
    // get all selectors for j row
    var j;
    var sels = [0];
    for ( j=1 ; j<=8 ; j++){
        sels[j] = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
    }
    return sels;
}
function auxiliary_get_html_values( sels ){
    // get all values for sel - array of selectors
    var j;
    var v;
    var vals = [0];
    var selector;
    for ( j=1 ; j<=8 ; j++){
        selector = sels[j]
        switch ( j ) {
            case 1:
                v = $( selector ).find( 'A' ).text();
                break;
            case 2:
            case 3:
            case 4:
                v = $( selector ).find( 'span' ).text();
                break;
            case 5:
                v = $( selector ).find( 'span' ).text();
                break;
            case 6:
            case 7:
            case 8:
                v = $( selector ).find( 'img' ).attr( "src" );
                break;
            default:
                break;
        }
        vals[j] = v;
    }
    return vals;
}
QUnit.module( "users_browtab setValToHTML", function( hooks ) { // This test described in tbody_hidden.xlsx file
    var sels;
    var vals;
    hooks.beforeEach( function( assert ) {
        stub = {};
        sels = auxiliary_get_html_selectors( 1 );
        vals = auxiliary_get_html_values( sels );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( '#0', function ( assert ) {
        expect( 9 );
        var i = 1;
        var j = 1;
        var k;
        var val = 'qwerty'
        var supplement = {};
        supplement.iconPath = [];

        var res = setValToHTML( i, j, val, supplement );

        var puts = auxiliary_get_html_values( sels );
        for ( k=1 ; k<=8 ; k++){
            if ( k == j ){
                assert.equal( puts[k], val, 'setValToHTML should put value in template' );
            }
            else {
                assert.equal( puts[k], vals[k], 'setValToHTML should no put value in template' );
            }

        }
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#1', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 1;
        var val = 'qwerty'
        var supplement = {};
        supplement.iconPath = [];
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'A' ).text();

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#2', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 2;
        var val = 'qwerty'
        var supplement = {};
        supplement.iconPath = [];
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'span' ).text();

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#3', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 3;
        var val = 'qwerty'
        var supplement = {};
        supplement.iconPath = [];
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'span' ).text();

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#4', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 4;
        var val = 'qwerty'
        var supplement = {};
        supplement.iconPath = [];
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'span' ).text();

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#5', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 5;
        var val = '2016-01-31'
        var d = new Date( val );             // transform f_date (string) to js Date object
        d = d.toLocaleDateString();    // format date to dd.mm.yyyy
        var supplement = {};
        supplement.iconPath = [];
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'span' ).text();

        assert.equal( put, d, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#6', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 6;
        var val = '/static/admin/img/icon-no.gif';
        var supplement = {};
        supplement.iconPath = [];
        supplement.iconPath[j] = val;
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'img' ).attr( "src" );

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#7', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 7;
        var val = '/static/admin/img/icon-no.gif';
        var supplement = {};
        supplement.iconPath = [];
        supplement.iconPath[j] = val;
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'img' ).attr( "src" );

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#8', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 8;
        var val = '/static/admin/img/icon-no.gif';
        var supplement = {};
        supplement.iconPath = [];
        supplement.iconPath[j] = val;
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'img' ).attr( "src" );

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
} );

