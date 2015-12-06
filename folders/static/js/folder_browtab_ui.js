// jQuery UI Document
console.log('start loading folder_browtab_ui.js');

/*
 *********************************************************************
 * Adding UI buttons (only icons) to <button>:
 *********************************************************************
 */

/*
 *********************************************************************
 * Main functions buttons:
 *********************************************************************
 */
$( "#button-create-folder" ).button({
    icons: {
        primary:    "ui-icon-plus",
        secondary:  "ui-icon-folder-collapsed"
    }
});
$( "#button-upload-report" ).button({
    icons: {
        primary:    "ui-icon-arrowthickstop-1-n",
        secondary:  "ui-icon-document"
    }
});
$( "#button-rename-element" ).button({
    icons: {
        primary:    "ui-icon-pencil",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-move-element" ).button({
    icons: {
        primary:    "ui-icon-cart",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-download-element" ).button({
    icons: {
        primary:    "ui-icon-arrowthickstop-1-s",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-delete-element" ).button({
    icons: {
        primary:    "ui-icon-trash",
        secondary:  "ui-icon-tag"
    }
});
/*
 *********************************************************************
 * Adding UI dialog form (with common properties) to div:
 *********************************************************************
 */
$( "#dialog-box-tree" ).dialog({
    dialogClass:    "no-close",
    autoOpen:       false,
    modal:          true,
    closeOnEscape:  true,
    height:         1.1 * dialog_width(), 
    width:          0.7 * dialog_width(), 
    open:           dialog_open_func_default(),
    buttons:        dialog_buttons_default()   // no comma - last item in array
});

/*
 *********************************************************************
 * Opening dialogs
 *********************************************************************
 */
$( "#button-create-folder" ).on( "click", function() {
    $( "#dialog-box-form tr:nth-child(1)" ).html( nameFormTR );
    $( "#dialog-box-form tr:nth-child(2)" ).html( emptyFormTR );
    $( "#dialog-box-form" ).dialog( "open" );
    $( "#dialog-box-form" ).dialog( "option", "title", "Нова тека" );
    $( "label[for='id_name']" ).text( "Назва теки" );
    $( "#id_name" ).val( "Тека без назви" );
    var buttons = dialog_buttons_default();
    // Redefine function on click for button nr 0:
    buttons[0].click =
        function(e) {
            e.preventDefault();
            ajax_folderCreate();
        };
    $( "#dialog-box-form" ).dialog( "option", "buttons", buttons );
});

$( "#button-upload-report" ).on( "click", function() {
    $( "#dialog-box-form tr:nth-child(1)" ).html( fileFormTR );
    $( "#dialog-box-form tr:nth-child(2)" ).html( emptyFormTR );
    $( "#dialog-box-form" ).dialog( "open" );
    $( "#dialog-box-form" ).dialog( "option", "title", "Заладувати файл" );
    $( "label[for='id_file']" ).text( "Назва файла" );
    var buttons = dialog_buttons_default();
    // Redefine function on click for button nr 0:
    buttons[0].click =
        function(e) {
            e.preventDefault();
            xhr_reportUpload();
        };
    $( "#dialog-box-form" ).dialog( "option", "buttons", buttons );
});

$( "#button-rename-element" ).on( "click", function() {
    var buttons = dialog_buttons_default();
    var f_name = $( "#thisfolder span" ).text();    // parent folder name
    if ( selElement.id > 0) {
        $( "#dialog-box-form tr:nth-child(1)" ).html( nameFormTR );
        $( "#dialog-box-form tr:nth-child(2)" ).html( emptyFormTR );
        $( "#dialog-box-form" ).dialog( "open" );
        $( "#id_name" ).val( selElement.name );
        if ( selElement.model == "folder" ) {
            $( "#dialog-box-form" ).dialog( "option", "title", "Перейменування теки" );
            $( "label[for='id_name']" ).text( "Нова назва" );
            // Redefine function on click for button nr 0:
            buttons[0].click = function( e ) {
                e.preventDefault();
                ajax_folderRename();
            };
        }
        else if ( selElement.model == "report" ) {
            $( "#dialog-box-form" ).dialog( "option", "title", "Перейменування документа" );
            $( "label[for='id_name']" ).text( "Нова назва" );
            // Redefine function on click for button nr 0:
            buttons[0].click = function( e ) {
                e.preventDefault();
                ajax_reportRename();
            };
        }
        $( "#dialog-box-form" ).dialog( "option", "buttons", buttons ); // new buttons
    }
    else {
        noSelectionMessage( f_name );
    }
});

$( "#button-move-element" ).on( "click", function() {
    var buttons = dialog_buttons_default();
    var f_name = $( "#thisfolder span" ).text();    // parent folder name
    if ( selElement.id > 0 ) {
        ajax_FoldersTreeFromBase(); // in case of success transform this ajax function 
                                    // will call dialogFoldersTreeHTML(sr) 
    }
    else {
        noSelectionMessage( f_name );
    }
});

function dialogFoldersTreeHTML( sr ) {    // callse by ajax_FoldersTreeFromBase() if success
    var parent_id = $( "#parent_id" ).val();
    var target_id = parent_id;              // id of target folder to move selected element
    var buttons = dialog_buttons_default();
    $( '#folders-tree-container' ).html( sr );
    $( '#folders-tree-container' ).jstree();
    $( '#folders-tree-container' ).jstree( "set_theme", "koopstyle" ); 
    $( '#folders-tree-container' ).jstree( 'show_node', parent_id );
    $( '#folders-tree-container' ).jstree( 'select_node', parent_id );
    $( '#folders-tree-container' ).on( 'changed.jstree', function( e, data ) {
            target_id = data.selected[0];  // selected taget is the first element of data.selected 1D array
            console.log("jsTree: data.selected=", data.selected);
    });
    $( "#dialog-box-tree" ).dialog( "open" );
    $( "#dialog-box-tree" ).dialog( "option", "title", "Перемістити елемент до теки..." );
    // Redefine function on click for button nr 0:
    buttons[0].click = function( e ) {
        e.preventDefault();
        ajax_elementMove( target_id );
    };
    buttons[1].click = function() {
        $( this ).dialog( "close" );
        selRowFocus();
        $.jstree.destroy();
    };
    $( "#dialog-box-tree" ).dialog( "option", "buttons", buttons ); // new buttons
}

$( "#button-delete-element" ).on( "click", function() {
    var buttons = dialog_buttons_default();
    var f_name = $( "#thisfolder span" ).text();    // parent folder name
    if ( selElement.id > 0 ) {
        $( "#dialog-box-form tr:nth-child(1)" ).html( nameFormTR );
        $( "#dialog-box-form tr:nth-child(2)" ).html( emptyFormTR );
        $( "#id_name" ).prop( "disabled", true );
        $( "#dialog-box-form" ).dialog( "open" );
        $( "#id_name" ).val( selElement.name );
        if ( selElement.model == "folder" ) {
            $( "#dialog-box-form" ).dialog( "option", "title", "Видалення теки" );
            $( "label[for='id_name']" ).text( "Видалити" );
            buttons[0].click = function( e ) {
                e.preventDefault();
                ajax_folderDelete();
            };
        }
        else if ( selElement.model == "report" ) {
            $( "#dialog-box-form" ).dialog( "option", "title", "Видалення документа" );
            $( "label[for='id_name']" ).text( "Видалити" );
            buttons[0].click = function( e ) {
                e.preventDefault();
                ajax_reportDelete();
            };
        }
        $( "#dialog-box-form" ).dialog( "option", "buttons", buttons ); // new buttons
        $( "#dialog-box-form" ).siblings().find( "button:eq(0)" ).focus();  // because input field disabled
    }
    else {
        noSelectionMessage( f_name );
    }
});

$( "#button-download-element" ).on( "click", function() {
    var buttons = dialog_buttons_default();
    var f_name = $( "#thisfolder span" ).text();    // parent folder name
    if ( selElement.id > 0 ) {
        $( "#dialog-box-form tr:nth-child(1)" ).html( nameFormTR );
        $( "#dialog-box-form tr:nth-child(2)" ).html( emptyFormTR );
        $( "#id_name" ).prop( "disabled", true );
        $( "#dialog-box-form" ).dialog( "open" );
        $( "#id_name" ).val( selElement.name );
        if ( selElement.model == "folder" ) {
            $( "#dialog-box-form" ).dialog( "option", "title", "Завантаження теки" );
            $( "label[for='id_name']" ).text( "Завантажити" );
            buttons[0].click = function( e ) {
                e.preventDefault();
                xhr_folderDownload();
            };
        }
        else if ( selElement.model == "report" ) {
            $( "#dialog-box-form" ).dialog( "option", "title", "Завантаження документа" );
            $( "label[for='id_name']" ).text( "Завантажити" );
            buttons[0].click = function( e ) {
                e.preventDefault();
                xhr_reportDownload();
            };
        }
        $( "#dialog-box-form" ).dialog( "option", "buttons", buttons ); // new buttons
        $( "#dialog-box-form" ).siblings().find( "button:eq(0)" ).focus();  // because input field disabled
    }
    else {
        noSelectionMessage( f_name );
    }
});
