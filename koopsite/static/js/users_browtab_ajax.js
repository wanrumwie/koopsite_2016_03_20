// JavaScript Document
console.log('start loading user_browtab_ajax.js');

/*
 *********************************************************************
 *  Actions in case of success server responce for AJAX or XMLHttpRequest:
 *********************************************************************
 */
function ajaxSuccessHandler( sr ) {
//    console.log('ajax: sr=', sr);
    xhrSuccessHandler( sr );
}
function xhrSuccessHandler( sr ) {
    dialogMessage( sr.message, sr.type, sr.title, 5000  );
    switch ( sr.type ) {
        case 'Group':
            $( "#dialog-box-form" ).dialog( "close" );
            changeAllElements( sr.group ); // change row
            break;
        case 'NoChange':
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'Change':
            $( "#dialog-box-form" ).dialog( "close" );
            changeSelElement( sr.changes, sr.supplement ); // change row
            break;
        case 'DeleteRow':
            $( "#dialog-box-form" ).dialog( "close" );
            deleteElement(); // delete selected element
            break;
        case 'Error': // transfer success, but server tell about error in data
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        // other items leave from folder_browtab_ajax.js:
        case 'IncorrectData':
            // dialog remains open, message - red
            break;
        case 'Forbidden':
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'Normal':
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'Rename':
            $( "#dialog-box-form" ).dialog( "close" );
            // renameSelElement(sr.new_name); // new name
            break;
        default:
            $( "#dialog-box-form" ).dialog( "close" );
            break;
    }
}
/*
 *********************************************************************
 *  Defining data array for send by AJAX:
 *********************************************************************
 */
function selElementArr(){
    // only selected element in table
    var arr = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = '';                        // parent folder id - for compatibility with Folders model
    arr.sendMail    = $( "#id_cond" ).prop( "checked" );  // send mail to user condition
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    arr.model       = selElement.model;          // selected element model name
    arr.id          = selElement.id;             // selected element id
    arr.name        = selElement.name;           // selected element name
//    console.log('arr=', arr);
    return arr;
}
function allElementsArr(){
    // all elements in filtered table
    /* Structure of arr:
    arr = { 'browTabName' : browTabName,
            'parent_id'   : parent_id,
            'selRowIndex' : selRowIndex,
            'elemSet'     : [ elem1, elem1, ... elemN ]
            }
    where elemSet[i] = {'id'    : id,
                        'model' : model,
                        'name'  : name
                        }
    */
    var arr = {};
    var elemSet = [];
    var elem = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = '';   // parent folder id
    arr.sendMail    = $( "#id_cond" ).prop( "checked" );  // send mail to user condition
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    for ( i=0 ; i<qs_TR_arr.length; i++ ) {
        elem = {};
        elem.id    = qs_TR_arr[i][0].id;
        elem.model = qs_TR_arr[i][0].model;
        elem.name  = qs_TR_arr[i][1];
        elemSet[i] = elem;
    }
    arr.elemSet = elemSet;
console.log('allElementsArr=', arr);
    return arr;
}
/*
 *********************************************************************
 *  AJAX rendering Activate All Accounts form:
 *********************************************************************
 */
function ajax_activateAllAccounts() {
    var arr = allElementsArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-activate-all-accounts";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_setMemberAllAccounts() {
    var arr = allElementsArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-set-member-all-accounts";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Single Account forms:
 *********************************************************************
 */
function ajax_recognizeAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-recognize-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_denyAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-deny-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_activateAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-activate-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_deactivateAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-deactivate-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_setMemberAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-set-member-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_denyMemberAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-deny-member-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_deleteAccount() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-delete-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
