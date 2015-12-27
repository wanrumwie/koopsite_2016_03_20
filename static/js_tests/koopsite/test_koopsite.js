/*
Global:  QUnit (?), expect (?), getSelRowIndex (?), rowsNumber (?)
*/

/********************************************************************/


/********************************************************************/

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
