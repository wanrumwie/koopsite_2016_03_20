/*
 * Global:  $ (?), console (?)
 */
console.log('start loading functions.js');
/*
 * Hiding the error message in form after user press key in fild with error data.
 */
set_listeners(); 

// TODO-add this Hiding the error message function to koopsite and flat templates.
// TODO-change function name?
function set_listeners(){
    $( 'input' ).on( 'keypress', function () {
        $( this ).siblings( '.errorlist' ).hide();
    });
    $( 'select' ).on( 'change', function () {
        $( this ).siblings( '.errorlist' ).hide();
    });
}

    

/*
$( 'table' ).on( 'keypress', '.error', function () {
    $( this ).find( '.errorlist' ).hide();
  });
*/
