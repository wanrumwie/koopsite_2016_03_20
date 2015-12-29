/*
Global:  $ (?), QUnit (?), console (?), expect (?), set_dummy_error_first_row, set_dummy_error_last_row, set_dummy_error_row
 */
console.log('start loading test_koopsite_functions.js');

/********************************************************************/

//TODO-create test for on("change") listener

QUnit.test( "error message not be hidden unless there is a keypress", function ( assert ) {
set_listeners(); 
    expect( 2 );
    set_dummy_error_first_row();
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), true );
    assert.equal( $( 'tr' ).last().find( '.errorlist' ).is( ':visible' ), false );
    $( 'tr' ).first().find( 'input' ).trigger( 'keypress' );
});

QUnit.test( "error message should be hidden on keypress in error field", function ( assert ) {
set_listeners(); 
    expect( 2 );
    set_dummy_error_first_row();
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), true );
    $( 'tr' ).first().find( 'input' ).trigger( 'keypress' );
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), false );
});


QUnit.test( "error message not be hidden on keypress in onother field", function ( assert ) {
set_listeners(); 
    expect( 2 );
    set_dummy_error_first_row();
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), true );
    $( 'tr' ).last().find( 'input' ).trigger( 'keypress' );
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), true );
});

QUnit.test( "only proper error message should be hidden on keypress", function ( assert ) {
set_listeners(); 
    expect( 4 );
    set_dummy_error_first_row();
    set_dummy_error_last_row();
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), true );
    assert.equal( $( 'tr' ).last().find( '.errorlist' ).is( ':visible' ), true );
    $( 'tr' ).first().find( 'input' ).trigger( 'keypress' );
    assert.equal( $( 'tr' ).first().find( '.errorlist' ).is( ':visible' ), false );
    assert.equal( $( 'tr' ).last().find( '.errorlist' ).is( ':visible' ), true );
});


/********************************************************************/


function set_dummy_error_row( row ){
console.log('row=', row);
    row.toggleClass( "error", true );
    var err = '<ul class="errorlist"><li>ERROR MESSAGE.</li></ul>';
    row.find('input').before( err );    
}
function set_dummy_error_first_row(){
    var row = $( 'tr' ).first();
    set_dummy_error_row( row );
}
function set_dummy_error_last_row(){
    var row = $( 'tr' ).last();
    set_dummy_error_row( row );
}
