// jQuery UI Document
console.log('start loading user_browtab_ui.js');
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
$( "#button-activate-all" ).button({
    icons: {
        primary:    "ui-icon-unlocked",
        secondary:  "ui-icon-folder-collapsed"
    }
});
$( "#button-set-member-all" ).button({
    icons: {
        primary:    "ui-icon-person",
        secondary:  "ui-icon-folder-collapsed"
    }
});
$( "#button-recognize-account" ).button({
    icons: {
        primary:    "ui-icon-check",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-activate-account" ).button({
    icons: {
        primary:    "ui-icon-unlocked",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-deactivate-account" ).button({
    icons: {
        primary:    "ui-icon-locked",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-deny-account" ).button({
    icons: {
        primary:    "ui-icon-cancel",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-set-member-account" ).button({
    icons: {
        primary:    "ui-icon-person",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-deny-member-account" ).button({
    icons: {
        primary:    "ui-icon-cancel",
        secondary:  "ui-icon-tag"
    }
});
$( "#button-delete-account" ).button({
    icons: {
        primary:    "ui-icon-trash",
        secondary:  "ui-icon-tag"
    }
});
/*
 *********************************************************************
 * Common body function for opening dialogs
 *********************************************************************
 */
//console.log('ajax_Function=', ajax_Function);
//console.log('typeof ajax_Function=', typeof ajax_Function);
//console.log('dialogTitle=', dialogTitle);
//console.log('inputLabel=', inputLabel);
//console.log('disabledInput=', disabledInput);

function buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg ) {
    if ( dialogTitle    === undefined ) { dialogTitle   = ""; }
    if ( inputLabel     === undefined ) { inputLabel    = ""; }
    if ( disabledInput  === undefined ) { disabledInput = false; }
    if ( inputVal       === undefined ) { inputVal      = ""; }
    if ( condLabel      === undefined ) { condLabel     = ""; }
    if ( condVal        === undefined ) { condVal       = false; }
    if ( confirmTitle   === undefined ) { confirmTitle  = ""; }
    if ( confirmMsg     === undefined ) { confirmMsg    = ""; }
    var buttons = get_dialog_default_buttons();
    var confirm_buttons = get_confirm_dialog_default_buttons();
    if ( selRowIndex >= 0 && selRowIndex < rowsNumber ) {
        // $( "#dialog-box-form tr:nth-child(1)" ).html( nameFormTR );
        $dialog_box_form.find( "tr:nth-child(1)" ).html( nameFormTR );
        $( "#id_name" ).prop( "disabled", disabledInput );          // input field disabled or not
        $( "#id_name" ).val( inputVal );
        $( "label[for='id_name']" ).text( inputLabel );
        if ( condLabel ){
            $dialog_box_form.find( "tr:nth-child(2)" ).html( condFormTR );
            $( "#id_cond" ).prop('checked', condVal );
            $( "label[for='id_cond']" ).text( condLabel );
        }
        else {
            $dialog_box_form.find( "tr:nth-child(2)" ).html( emptyFormTR );
        }
        $dialog_box_form.dialog( "open" );
        $dialog_box_form.dialog( "option", "title", dialogTitle );
        if ( confirmTitle ){                                        // confirmation dialog needed
            buttons[0].click = function( e ) {
                e.preventDefault();
                $dialog_confirm.dialog( "open" );
                $dialog_confirm.dialog( "option", "title", confirmTitle );
                $dialog_confirm.html( confirmMsg );
                confirm_buttons[0].click = function( e ) {
                    $dialog_confirm.dialog( "close" );
                    e.preventDefault();
                    ajax_Function();
                };
                $dialog_confirm.dialog( "option", "buttons", confirm_buttons );      // new confirm_buttons
                $dialog_confirm.siblings().find( "button:eq(0)" ).focus(); 
            };
        }
        else {                                                      // run ajax without confirmation
            buttons[0].click = function( e ) {
                e.preventDefault();
                ajax_Function();
            };
        }
        $dialog_box_form.dialog( "option", "buttons", buttons );     // new buttons
        if ( disabledInput ) {                                              // because input field disabled
            $dialog_box_form.siblings().find( "button:eq(0)" ).focus(); 
        }
    }
    else {
        noSelectionMessage("Users Table");
    }
}
/*
 *********************************************************************
 * Opening dialogs
 *********************************************************************
 */
$( "#button-activate-all" ).on( "click", function() {
    var ajax_Function   = ajax_activateAllAccounts; 
    var dialogTitle     = "Активація ВСІХ обраних акаунтів";
    var inputLabel      = "Активувати";
    var disabledInput   = true;
    var inputVal        = rowsNumber + " акаунтів";
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "Групова дія";
    var confirmMsg      = "Ви намагаєтеся активувати одразу " + 
                                    rowsNumber + " акаунтів. Ви впевнені?";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-set-member-all" ).on( "click", function() {
    var ajax_Function   = ajax_setMemberAllAccounts; 
    var dialogTitle     = "Прова доступу члена кооперативу для ВСІХ обраних акаунтів";
    var inputLabel      = "Надати";
    var disabledInput   = true;
    var inputVal        = rowsNumber + " акаунтів";
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "Групова дія";
    var confirmMsg      = "Ви намагаєтеся надати права доступу одразу " + 
                                    rowsNumber + " акаунтів. Ви впевнені?";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-recognize-account" ).on( "click", function() {
    var ajax_Function   = ajax_recognizeAccount; 
    var dialogTitle     = "Підтвердження акаунту";
    var inputLabel      = "Підтвердити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-deny-account" ).on( "click", function() {
    var ajax_Function   = ajax_denyAccount; 
    var dialogTitle     = "Відмова підтвердження акаунту";
    var inputLabel      = "Відмовити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-activate-account" ).on( "click", function() {
    var ajax_Function   = ajax_activateAccount; 
    var dialogTitle     = "Активація акаунту";
    var inputLabel      = "Активувати";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "";
    var confirmMsg      = "";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-deactivate-account" ).on( "click", function() {
    var ajax_Function   = ajax_deactivateAccount; 
    var dialogTitle     = "Деактивація акаунту";
    var inputLabel      = "Деактивувати";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "";
    var confirmMsg      = "";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-set-member-account" ).on( "click", function() {
    var ajax_Function   = ajax_setMemberAccount; 
    var dialogTitle     = "Права доступу члена кооперативу";
    var inputLabel      = "Надати";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "";
    var confirmMsg      = "";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-deny-member-account" ).on( "click", function() {
    var ajax_Function   = ajax_denyMemberAccount; 
    var dialogTitle     = "Права доступу члена кооперативу";
    var inputLabel      = "Вилучити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});
$( "#button-delete-account" ).on( "click", function() {
    var ajax_Function   = ajax_deleteAccount; 
    var dialogTitle     = "Видалення акаунту";
    var inputLabel      = "Видалити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "Видалення акаунту";
    var confirmMsg      = "Замість видалення акаунт краще деактивувати. Ви наполягаєте на видаленні?";
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg );
});

console.log('$( "#button-set-member-all" )=', $( "#button-set-member-all" ));
