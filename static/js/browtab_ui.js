// jQuery UI Document
console.log('start loading browtab_ui.js');

/*
 *********************************************************************
 * Width for dialog widgets:
 *********************************************************************
 */
function dialog_width() {
    var tw = $( "#browtable tbody" ).width();
    var w = ( tw > 600 ) ? 450 : tw *0.75;
    return w;
}
/*
 *********************************************************************
 * Adding UI dialog form (with common properties) to div:
 *********************************************************************
 */
$( "#dialog-box-form" ).dialog({
    dialogClass:    "no-close",
    autoOpen:       false,
    modal:          true,
    closeOnEscape:  true,
    width:          dialog_width(),
    open:           dialog_open_func_default(),
    close:          dialog_close_func(),
    buttons:        dialog_buttons_default()   // no comma - last item in array
});

$( "#dialog-confirm" ).dialog({
    dialogClass:    "no-close",
    autoOpen:       false,
    modal:          true,
    closeOnEscape:  true,
//    width:          dialog_width(),
//    open:           dialog_open_func_default(),
    buttons:        confirm_dialog_buttons_default()   // no comma - last item in array
});

/*
 *********************************************************************
 *  Defining functions returning default "buttons" and "open" options 
 *  common for all UI dialog calls. 
 *********************************************************************
 */
function dialog_buttons_default() {
    var buttons = [
        {
            text: "Ok",
            click: function() { } // buttons[0].click will be redefined when dialog open
        },
        {
            text: "Cancel",
            click: function() {
                $( this ).dialog( "close" );
                selRowFocus();
            }
        }
    ];
    return buttons;
}
function confirm_dialog_buttons_default() {
    var buttons = [
        {
            text: "Ok",
            click: function() { } // buttons[0].click will be redefined when dialog open
        },
        {
            text: "Cancel",
            click: function() {
                $( this ).dialog( "close" );
                selRowFocus();
            }
        }
    ];
    return buttons;
}
function dialog_close_func( event, ui ) {
    var close_func = function( event, ui ) { 
        selRowFocus(); 
        };
    return close_func;
}
function dialog_open_func_default() {
    var open_func = function() {
            $( "#dialog-box-form" ).dialog( "option", "width", dialog_width() );
            $( this ).keypress( function( e ) {
                if ( e.keyCode == $.ui.keyCode.ENTER ) {
                    e.preventDefault();
                    $( this ).parent().find( "button:contains('Ok')" ).trigger( "click" );
                }
            });
    };
    return open_func;
}
function dialog_box_form_close() {
    $( "#dialog-box-form" ).dialog( "close" );
}

function defineAbortButton( xhr ){
    // Define text and function for the only button during upload file:
    var buttons = [
        {
            text  : "Abort loading",
            click : function( e ) {
                        e.preventDefault();
                        $( this ).dialog( "close" );
                        selRowFocus();
                        xhr.abort();
            }
        }
    ];
    $( "#dialog-box-form" ).dialog( "option", "buttons", buttons );
}

/*
 *********************************************************************
 * HTML for dynamically created dialogs:
 *********************************************************************
 */
var nameFormLabel = '<label for="id_name">Тека:</label>';
var nameFormInput = '<input id="id_name" maxlength="256" name="name" type="text" autofocus/>';
var nameFormTR    = '<td>' + nameFormLabel + '</td>' +
                    '<td>' + nameFormInput + '</td>';
var fileFormLabel = '<label for="id_file">Файл:</label>';
var fileFormInput = '<input id="id_file" maxlength="256" name="file" type="file" autofocus/>';
var fileFormTR    = '<td>' + fileFormLabel + '</td>' +
                    '<td>' + fileFormInput + '</td>';
var condFormLabel = '<label for="id_cond">Повідомити ч/з email</label>';
var condFormInput = '<input id="id_cond" name="cond" type="checkbox"/>';
var condFormTR    = '<td>' + '</td>' +
                    '<td>' + condFormLabel + condFormInput + '</td>';
var progressTR    = '<td>Progress:</td><td><div id="progressbar"></div></td>';
var emptyFormTR   = '<td></td><td></td>';

/*
 *********************************************************************
 * Adding UI dialog message to div:
 *********************************************************************
 */
$( "#dialog-message" ).dialog({
    dialogClass:    "no-close",
    autoOpen: false,
    modal: true,
    closeOnEscape: true,
//    dialogClass: "ui-state-highlight",
    buttons: {
        Ok: function() {
            $( this ).dialog( "close" );
            selRowFocus();
        }
    }
});

/*
 *********************************************************************
 * Progress bar
 *********************************************************************
 */
function progressbarShow(){
    $( "#dialog-box-form tr:nth-child(2)" ).html(progressTR);
    $( "#progressbar" ).progressbar({ value: 0 });
}

function setProgress( x, max ){
    setTimeout( function(){
        var pmax = $( "#progressbar" ).progressbar( "option", "max" );
        if ( pmax === undefined ) { pmax = 100; }
        if ( max === undefined ) { max = pmax; }
            $( "#progressbar" ).progressbar({ 
                value:  x,
                max:    max         
                });
    },1000); // delay for test purpose
//    alert('progress: x =' + x + '   max =' + max);
}
function progressHandler( pe ) {
console.log( 'lengthComputable =', pe.lengthComputable );
    if ( pe.lengthComputable ) {
console.log('total =', pe.total, '   loaded =', pe.loaded );
        setProgress( pe.loaded, pe.total );
    } else { setProgress( false ); }
}
function loadEndHandler( pe ) {
console.log('end:', '   loaded =', pe.loaded );
    setProgress( pe.loaded );
}


/*
 *********************************************************************
 * Messages
 *********************************************************************
 */
function dialogMessage( msg, type, title, time ) {
    // Open message dialog of given type
    var dlgClass = "";
    switch ( type ) {
        case "IncorrectData":   dlgClass = "ui-state-error";        break;
        case "Forbidden":       dlgClass = "ui-state-error";        break;
        case "Error":           dlgClass = "ui-state-error";        break;
        case "Normal":          dlgClass = "ui-state-highlight";    break;
        default:                dlgClass = "ui-state-highlight";    break;
    }
    dlgClass = "no-close" + " " + dlgClass;
    $( "#dialog-message" ).dialog( "option", "dialogClass", dlgClass );
	$( "#dialog-message" ).dialog( "open" );
//	$( "#dialog-message" ).text( msg );
	$( "#dialog-message" ).html( msg );
    if ( title !== undefined ) {
        $( "#dialog-message" ).dialog( "option", "title", title );
    }
    if ( time !== undefined && time > 0 ) {
        setTimeout( function(){ 
            $( "#dialog-message" ).dialog( "close" ); 
            selRowFocus();
            }, 
            time );
    }
}

function folderEmptyMessage( f_name ) {
    // This function called from ...ajax.js
	dialogMessage( "Ця тека порожня.", "", f_name, 1000 );
}
function noSelectionMessage( f_name ) {
    // This function called on event dblClick or EnterKey
	dialogMessage( "Нічого не вибрано!", "Error", f_name, 1000 );
}
function functionOnDevelopeMessage() {
	dialogMessage( "Ця процедура ще розробляється...", "", "", 2000 );
}


// Temporary buttons to open widgets for test purposes

$( "#button-service" ).text("Check Focus");
$( "#button-service" ).on( "click", function() {
    $( "#dialog-box-form" ).dialog( "open" );
    $( "#dialog-box-form" ).dialog( "option", "Check Focus" );
    var buttons = dialog_buttons_default();
    // Redefine function on click for button nr 0:
    buttons[0].click =
        function(e) {
            e.preventDefault();
            $( this ).dialog( "close" );
            selRowFocus();
        };
    $( "#dialog-box-form" ).dialog( "option", "buttons", buttons );
});


$( "#button-service2" ).text("Select child_node");
$( "#button-service2" ).on( "click", function() {
    $(function () {
        $('#folders-tree-container').jstree(true).select_node('child_node');
    }); 
});


    function supportFileAPI() {
        var fi = document.createElement('INPUT');
        fi.type = 'file';
        return 'files' in fi;
    }

    function supportAjaxUploadProgressEvents() {
        var xhr = new XMLHttpRequest();
        return !! (xhr && ('upload' in xhr) && ('onprogress' in xhr.upload));
    }

function supportAjaxUploadWithProgress() {
    return supportFileAPI() && supportAjaxUploadProgressEvents();

}

/*
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
    } else {
        alert( "The File APIs are fully supported in this browser." );
        }

    if (supportAjaxUploadWithProgress()) {
        alert('AjaxUploadWithProgress is fully supported in this browser.');
    } else {
        alert( "AjaxUploadWithProgress is NOT supported in this browser" );
    }
*/
