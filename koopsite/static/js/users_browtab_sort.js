// JavaScript Document
console.log('start loading user_browtab_sort.js');

/*
 *********************************************************************
 * Order buttons:
 *********************************************************************
 */
var orderAsc        = [];       // set of values: ascending (+1) or decsendind (-1) order for columns  
var orderGroup      = false;    // if true - ordering with Folders first, otherwise - mixed
appendOrderButtons( 1, columnsNumber );
changeOrderIcon( 1, 1, columnsNumber );
/*changeOrderGroupIcon( 1 );*/

/*
 *********************************************************************
 * Set listener for ordering buttons:
 *********************************************************************
 */

appendOrderListeners();

function appendOrderListeners(){
    var selector, i;
    for ( i = 1 ; i <= columnsNumber ; i++ ) {
        selector = "#button-sort-" + i;
        $( selector ).on( "click", function() {
                                        var s = 'button-sort-';
                                        var len = s.length;
                                        var col = this.id.slice( len );
                                        col = parseInt( col, 10 );
                                        ordering( col ); 
                                    });
    }
}
function ordering( col ){
    changeOrderIcon( col, 1, columnsNumber );
    qs_TR_arr = sort_table( qs_TR_arr, col, orderAsc[col] );
    display_qs_TR_arr();
//console.log('display_qs_TR_arr: after: -------------------');
//console.log('selTR =', selTR);
//console.log('selRowIndex =', selRowIndex);
//console.log('selElement =', selElement);
//console.log('=============================================');
}

/*
 *********************************************************************
 * Sort 2D-array: queryset data + <TR> object:
 *********************************************************************
 */

function floatSa( s ){   // convert string to number
    var z, isnum;
    if ( s ) {
        isnum = $.isNumeric( s );
        z = parseFloat( s );
        if ( !isnum ){
            z = z + 0.1;    // for string like "12a" convert to 12.1
        }
    }
    else {
        z = 0.0;
    }
    return z;
}
 
function sort_table( arr, col, asc ){
    // sort the array by the specified column number (col) and order (asc)
    var x, y, dif;
    arr.sort(function( a, b ){
            x = a[col];     // rename comparison fields for simplisity
            y = b[col];
            switch ( col ) {
                case 1:
                case 2:
                case 4:
                    // string -> lower case for comparison
                    x = x.toLowerCase();
                    y = y.toLowerCase();
                    dif = ( x == y ) ? 0 : (( x > y ) ? asc : -1*asc );
                    break;
                case 3:         // "78" --> 78 , "78a" --> 78.1
                    x = floatSa( x );
                    y = floatSa( y );
                    dif = ( x == y ) ? 0 : (( x > y ) ? asc : -1*asc );
                    break;
                case 5:         // date formated as string
                    dif = ( x == y ) ? 0 : (( x > y ) ? asc : -1*asc );
                    break;
                default:        // other fields
                    dif = ( x == y ) ? 0 : (( x > y ) ? asc : -1*asc );
                    break;
            }
        return dif;
    });
    return arr;
}
 
