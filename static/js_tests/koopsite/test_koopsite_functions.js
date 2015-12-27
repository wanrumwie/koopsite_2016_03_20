/*
global $, test, equal
*/

/********************************************************************/


/********************************************************************/


QUnit.test( "errors should be hidden on keypress in field with error", function ( assert ) {
    expect( 1 );
    $( '#id_name' ).trigger( 'keypress' );
    assert.equal( $( '.errorlist' ).is( ':visible' ), false );
});
QUnit.test( "errors not be hidden on keypress in field without error", function ( assert ) {
    expect( 1 );
    $( '#id_created_on' ).trigger( 'keypress' );
    assert.equal( $( '.errorlist' ).is( ':visible' ), true );
});
QUnit.test( "errors not be hidden unless there is a keypress", function ( assert ) {
    expect( 1 );
    assert.equal( $( '.errorlist' ).is( ':visible' ), true);
});
