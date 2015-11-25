// JavaScript Document
console.log('start loading user_browtab_filter.js');

appendFilterButtons();
appendFilterListeners();
appendDateFields();
appendDateFieldsListeners();


/*
 *********************************************************************
 * Filter buttons:
 *********************************************************************
 */
function appendFilterButtons(){
    $( "#button-apply-filter"  ).button( { icons: { primary: "ui-icon-circle-triangle-s" } } );
    $( "#button-cancel-filter" ).button( { icons: { primary: "ui-icon-circle-close" } } );
}
/*
 *********************************************************************
 * Set listener for ordering buttons:
 *********************************************************************
 */
function appendFilterListeners(){
    $( "#button-apply-filter"  ).on( "click", function() { applyFilter(); });
    $( "#button-cancel-filter" ).on( "click", function() { cancelFilter(); });
}


var radio_names = ['is_recognized', 'is_active', 'has_members', 'date_joined_all'];
var date_names = ['date_joined'];
var filt_val_default = get_filters_default();
var previous_filt_val = filt_val_default;


function applyFilter(){
    var filt_val = get_filters();
    var bool = equal_dict( previous_filt_val, filt_val_default ); // was previous filter equal to default (no filter)?
    bool = bool || equal_dict( previous_filt_val, filt_val );     // or is new filter equal to previous?
    if ( !bool ) {                                                // if no then first restore default table view
        changeOrderIcon( 1, 1, columnsNumber );
        restore_qs_TR_arr();
        display_qs_TR_arr();
    }
    qs_TR_arr = filter_table( qs_TR_arr, filt_val );
    rowsNumber = qs_TR_arr.length;
    selRowIndex = getSelRowIndex( selRowIndex ); // change selRowIndex if it is out of new rowsNumber
    display_qs_TR_arr();
    previous_filt_val = filt_val;
}
function cancelFilter(){
    $( "input:radio" ).val(['all']);
    changeOrderIcon( 1, 1, columnsNumber );
    restore_qs_TR_arr();
    display_qs_TR_arr();
    previous_filt_val = filt_val_default;
}

function get_filters_default() {
    var i, n, dict={};
    for ( i in radio_names ) {
        n = radio_names[i];
        dict[n]='all';
    }
    return dict;
}
function equal_dict( d1, d2 ){
    var bool = true;
    var i;
    for ( i in d1 ) {
        bool = ( bool && ( d1[i] == d2[i] ) );
    }
    return bool;
}

var date_joined_from, date_joined_to;

function get_filters(){
    var dict = {};
    var i, n, v, selector; 
    var sel_patt = "#filter_box input:radio[name=<>]:checked";
    date_joined_from = get_iso_field( "iso_", "#date_joined_from" );
    date_joined_to   = get_iso_field( "iso_", "#date_joined_to" );
    for ( i in radio_names ) {
        n = radio_names[i];
        selector = sel_patt.replace( '<>', n );
        v = $( selector ).val();
        dict[n] = v;
    }
    return dict;
}
function get_iso_field( iso, selector ){
    var v, iso_v;
    var iso_selector = "#" + iso + selector.slice(1);
    console.log("iso_selector=",iso_selector);
    v = $( selector ).val();
    if ( v === "" || !v ) {
        iso_v = "";
    }
    else {
        iso_v = $( iso_selector ).val();
    }
    return iso_v;
}

function filter_table( arr, filt_val ){
    // filter the array by the filt_val dictionary
    var a = [], bool, bool_all, x, n, v, col;
    arr = jQuery.grep(arr, function( a, i ){
        bool_all = true;
        for ( n in filt_val ) {
            v = filt_val[n];
            switch ( n ) {
                case 'date_joined_all':
                    col = 5;
                    break;
                case 'is_recognized':
                    col = 6;
                    break;
                case 'is_active':
                    col = 7;
                    break;
                case 'has_members':
                    col = 8;
                    break;
                default:
                    break;
            }
            x = a[col];     // rename comparison field for simplisity
            switch ( v ) {
                case 'all':
                    bool = true;
                    break;
                case 'yes':
                    bool = ( x === true );
                    break;
                case 'no':
                    if ( col == 5 ) {
                        x = x.slice( 0, 10 );
                        /*
                        bool = ( date_joined_from <= x && x <= date_joined_to );
                        */
                        bool = ( date_joined_from <= x || !date_joined_from || date_joined_from === '' );
                        bool = ( bool && ( x <= date_joined_to || !date_joined_to || date_joined_to === ''  ) );
                    }
                    else {
                        bool = ( x === false );
                    }
                    break;
                case 'none':
                    bool = ( x === null || x === undefined );
                    break;
                default:
            }
            bool_all = ( bool_all && bool );
//console.log('n =',n, 'v =',v, 'x =', x, 'i =',i, 'bool =',bool, 'bool_all =',bool_all);
        }
        return bool_all;
    });
//console.log('arr =', arr);
    return arr;
}
 
function appendDateFields() {
    $.datepicker.setDefaults({
        showOn:             "button",
        buttonImageOnly:    true,
        buttonImage:        "/static/admin/img/icon_calendar.gif",
        altFormat:          'yy-mm-dd',
        numberOfMonths:     1,
        selectOtherMonths:  true,
        showOtherMonths:    true,
        regional:           "uk"
    });
    $( "#date_joined_from" ).datepicker({
        altField: '#iso_date_joined_from', 
        defaultDate: "-1w",
        onClose: function( selectedDate ) {
            $( "#date_joined_to" ).datepicker( "option", "minDate", selectedDate );
        }
    });
    $( "#date_joined_to" ).datepicker({
        altField: '#iso_date_joined_to', 
        defaultDate: "",
        onClose: function( selectedDate ) {
            $( "#date_joined_from" ).datepicker( "option", "maxDate", selectedDate );
        }
    });
}

function appendDateFieldsListeners(){
    $( "#date_joined_from" ).on( "change", function() {
        var dstr = $( this ).val();
        var dobj = new Date( dstr );
console.log('dstr =', dstr);
console.log('dobj =', dobj);
        
    });
}
