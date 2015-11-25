// JavaScript Document
console.log('start loading browtab_sort.js');

/*
 *********************************************************************
 * Order buttons:
 *********************************************************************
 */
function appendOrderButtons( ifirst, ilast ){
    var col, s;
    for ( col = ifirst ; col <= ilast ; col++ ){
        s = "#button-sort-" + col;
        $( s ).button();
        orderAsc[col] = 0;
    }
}
function clearOrderIcons( ifirst, ilast ){
    var col, s;
    var img = "ui-icon-blank";
    for ( col = ifirst ; col < ilast ; col++ ){
        s = "#button-sort-" + col;
        $( s ).button( "option", "icons", { secondary: img } );
        orderAsc[col] = 0;
    }
}
function changeOrderIcon( col, ifirst, ilast ){
    var img;
    var asc = orderAsc[col];
    clearOrderIcons( ifirst, ilast );
    if ( asc === 0 ) { asc  =  1; }
    else             { asc *= -1; }
    switch ( asc ){
        case -1: img = "ui-icon-carat-1-s"; break;
        case  0: img = "ui-icon-blank";     break;
        case  1: img = "ui-icon-carat-1-n"; break;
        default: img = "ui-icon-blank";     break;
    }
    var s = "#button-sort-" + col;
    $( s ).button( "option", "icons", { secondary: img } );
    orderAsc[col] = asc;
    var opt = $( s ).button( "option", "icons" );
}
function changeOrderGroupIcon( col ){
    orderGroup = !orderGroup;
    var img = ( orderGroup ) ? "ui-icon-transfer-e-w" : "ui-icon-shuffle";
    var s = "#button-sort-" + col;
    $( s ).button( "option", "icons", { secondary: img } );
}

 
