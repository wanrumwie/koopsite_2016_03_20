$( document ).ready(function ( $ ) {
    $( '.errorlist' ).siblings().on( 'keypress', function () {
        $( '.errorlist' ).hide();
    });
});
