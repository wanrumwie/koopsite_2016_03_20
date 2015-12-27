$( document ).ready( function ( $ ) {
    $( '.error' ).each( function () {
        $( this ).on( 'keypress', function () {
            $( this ).$( '.errorlist' ).hide();
        });
    });
});
