// JavaScript Document
console.log('start loading folder_browtab_ajax.js');

/*
 *********************************************************************
 *  Actions in case of success server responce for AJAX or XMLHttpRequest:
 *********************************************************************
 */
function ajaxSuccessHandler( sr ) {
console.log('ajaxSuccessHandler(sr): ==================================');
console.log('sr=', sr);
console.log('selRow =', selRow);
console.log('selRowIndex =', selRowIndex);
console.log('selElement =', selElement);
console.log('qs_TR_arr[selRowIndex] =', qs_TR_arr[selRowIndex]);
    xhrSuccessHandler( sr );
}
function xhrSuccessHandler( sr ) {
console.log('sr=', sr);
    dialogMessage( sr.message, sr.type, sr.title, 2000 );
    switch (sr.type) {
        case 'Error': // transfer success, but server tell about error in data
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'IncorrectData':
            // dialog remains open, message - red
            break;
        case 'Forbidden':
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'Normal':
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'NoChange':
            $( "#dialog-box-form" ).dialog( "close" );
            break;
        case 'NewRow':
            $( "#dialog-box-form" ).dialog( "close" );
            addNewElement( sr.changes, sr.supplement ); // add new element; changes has all values of new element
            break;
        case 'Rename':
            $( "#dialog-box-form" ).dialog( "close" );
            changeSelElement( sr.changes, sr.supplement ); // change row
            set_name_to_selElement( sr.changes[0].name ); // new name must be stored in selElement & qs_TR_arr
            break;
        case 'MoveElement':
            $.jstree.destroy();
            $( "#dialog-box-tree" ).dialog( "close" );
            moveElement(); // remove selected element from current folder
            break;
        case 'DeleteRow':
            $( "#dialog-box-form" ).dialog( "close" );
            deleteElement(); // delete selected element
            break;
        default:
            $( "#dialog-box-form" ).dialog( "close" );
            break;
    }
//console.log('after: xhrSuccessHandler( sr )  : ========================');
//console.log('selRow =', selRow);
//console.log('selRowIndex =', selRowIndex);
//console.log('selElement =', selElement);
//console.log('qs_TR_arr[selRowIndex] =', qs_TR_arr[selRowIndex]);
}
/*
 *********************************************************************
 *  Defining data array for send by AJAX:
 *********************************************************************
 */
function selElementArr(){
    var arr = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = $( "#parent_id" ).val();   // parent folder id
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    arr.model       = selElement.model;          // selected element model name
    arr.id          = selElement.id;             // selected element id
    arr.name        = selElement.name;           // selected element name
//    console.log('arr=', arr);
    return arr;
}
/*
 *********************************************************************
 *  AJAX receiving Folders Tree HTML code:
 *********************************************************************
 */
function ajax_FoldersTreeFromBase() {
    console.log("ajax_FoldersTreeFromBase()");
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folders-tree-from-base";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    // dataType = "html";
    as.success = function( json ) {
            console.log( "ajax_FoldersTreeFromBase() success" );
            var sr = json.server_response;
            dialogFoldersTreeHTML( sr );
        };
    as.error = function( xhr ) {
            setStartRow(); // select row for startRowIndex from previous load of this page
            xhrErrorAlert( xhr, 'ajax_FoldersTreeFromBase' );
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Folder Create form:
 *********************************************************************
 */
function ajax_folderCreate() {
    var arr = selElementArr();
    arr.name = $( "#id_name" ).val();  // redefine: new folder name
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folder-create";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Folder Rename form:
 *********************************************************************
 */
function ajax_folderRename() {
    var arr = selElementArr();
    arr.name = $( "#id_name" ).val();    // redefine: folder new name
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folder-rename";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Report Rename form:
 *********************************************************************
 */
function ajax_reportRename() {
    var arr = selElementArr();
    arr.name = $( "#id_name" ).val();    // redefine: report new name
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-report-rename";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Element Move dialog:
 *********************************************************************
 */
function ajax_elementMove( target_id ) {
    var arr = selElementArr();
    arr.target_id = target_id;                  // additional element in arr
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-element-move";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Folder Delete form:
 *********************************************************************
 */
function ajax_folderDelete() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folder-delete";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Report Delete form:
 *********************************************************************
 */
function ajax_reportDelete() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-report-delete" + "/" + arr.id + "/";    // pk added to url as argument for decorator
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 * Common function for XMLHttpRequest file download:
 *********************************************************************
 */
function xhr_POST( url, encoded_json_string ) {
    var xhr = new XMLHttpRequest();
    xhr.addEventListener( "load",  transferSuccess,  false );
    xhr.addEventListener( "error", transferFailed,   false );       // ADD FUNCTION !!!
    xhr.addEventListener( "abort", transferCanceled, false );       // ADD FUNCTION !!!

    xhr.onprogress = progressHandler;
    xhr.onloadend = loadEndHandler;
    defineAbortButton( xhr );
    progressbarShow();

    type = "POST";
    xhr.open(type, url, true);
    xhr.setRequestHeader( "X-CSRFToken", csrf_token);    // from cookie or from HTML
    xhr.setRequestHeader( "X-client-request", encoded_json_string);
    xhr.responseType = 'blob';
    xhr.send();

    function transferSuccess() {
        var json, sr, cd, h, fn;
        if ( xhr.readyState == 4 && xhr.status == 200 ) {
            h    = xhr.getAllResponseHeaders();
            cd   = xhr.getResponseHeader( 'Content-Disposition' );
            fn   = cd.filename;
            json = xhr.getResponseHeader( 'server_response' );
            sr   = JSON.parse( json );
            download( xhr.response, sr.title );
            xhrSuccessHandler( sr );
        } else {
            xhrErrorHandler( xhr );
        }
    }
}
/*
 *********************************************************************
 *  AJAX rendering file Download form:
 *********************************************************************
 */
function xhr_reportDownload() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    var encoded_json_string = encodeURIComponent( json_string );
    var url = "/folders/ajax-report-download";
    xhr_POST( url, encoded_json_string );
}
function xhr_folderDownload() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    var encoded_json_string = encodeURIComponent( json_string );
    var url = "/folders/ajax-folder-download";
    xhr_POST( url, encoded_json_string );
}
/*
 *********************************************************************
 *  XMLHttpRequest rendering Report Upload form:
 *********************************************************************
 */
// TODO: DRY xhr_reportUpload:
function xhr_reportUpload() {
    input = document.getElementById( 'id_file' );
    file = input.files[0];
    if ( !file ){
        dialogMessage( "File name empty", "Error", "File name empty title", 2000 );
        return;
    }
    var arr = selElementArr();
    arr.fileName = file.name;
    arr.fileSize = file.size;
    arr.fileType = file.type;
    arr.fileLastModifiedDate = file.lastModifiedDate;
    var json_string = JSON.stringify( arr );
    var encoded_json_string = encodeURIComponent( json_string );

    var xhr = new XMLHttpRequest();
    xhr.addEventListener( "load",  transferSuccess,  false );
    xhr.addEventListener( "error", transferFailed,   false );       // ADD FUNCTION !!!
    xhr.addEventListener( "abort", transferCanceled, false );       // ADD FUNCTION !!!

    xhr.upload.onprogress = progressHandler;
    xhr.onloadend = loadEndHandler;
    defineAbortButton(xhr);
    progressbarShow();

    type = "POST";
    url = "/folders/ajax-report-upload";
    xhr.open( type, url, true );
    xhr.setRequestHeader( "X-CSRFToken", csrf_token);    // from cookie or from HTML
    xhr.setRequestHeader( "X-client-request", encoded_json_string );
    xhr.send( file );

    function transferSuccess() {
        var json, sr;
        if ( xhr.readyState == 4 && xhr.status == 200 ) {
            json = xhr.getResponseHeader( 'server_response' );
            sr = JSON.parse( json );
            xhrSuccessHandler( sr );
        } else {
            xhrErrorHandler( xhr );
        }
    }
}
