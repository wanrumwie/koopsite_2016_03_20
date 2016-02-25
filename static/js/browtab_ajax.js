// JavaScript Document
console.log('start loading browtab_ajax.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

var csrf_token;

// document_ready_handler called from html:
function browtab_ajax_document_ready_handler(){
    create_qs_TR_arr();
    // csrf_token = $.cookie('csrftoken');             // Receiving the csrf_token value from cookie
    csrf_token = $( "#csrfmiddlewaretoken" ).val();   // Receiving the csrf_token value from template
    ajax_startRowIndexFromSession();                // Receiving start row index from session
    set_browtab_ajax_listeners(); 
}
function set_browtab_ajax_listeners( $selRowIndex ){
    if ( $selRowIndex === undefined ) {
        $selRowIndex = $( "#selRowIndex" );
    }
    $selRowIndex.off( "change"        ).on( "change",         onChange_handler );
}
function onChange_handler( event ) {
    ajax_selRowIndexToSession();                    // Sending selected row index to session
    return false;
}
/*
 *********************************************************************
 *  Defining error and cancel handlers for xhr: 
 *********************************************************************
 */
function xhrErrorAlert( xhr, ss ) {
    if ( ss === undefined ) { ss = ''; }
    alert('xhrErrorAlert: ' + ss +
                '\n xhr.status='        + xhr.status + 
                '\n xhr.statusText='    + xhr.statusText + 
                '\n xhr.responseText='  + xhr.responseText );
}
function xhrErrorHandler( xhr ) {
console.log('xhrErrorHandler:', 'xhr=', xhr);
    if ( xhr.status == 401 || xhr.status == 403 ) { // Redirect to login
        //window.location = xhr.responseText;
        dialogMessage( "Ви не маєте доступу до цієї операції!",
                      "Error", "Помилка доступу", 3000 );
        dialog_box_form_close();
    } else {
        xhrErrorAlert( xhr, 'xhrErrorHandler' ); }
}
function transferFailed( evt ) {
	dialogMessage( "An error occurred while transferring the file. Probably file too long", 
                        "Error", "UPLOAD ERROR", 3000 );
    dialog_box_form_close();
//  alert( "An error occurred while transferring the file." );
}
function transferCanceled( evt ) {
	dialogMessage( "The transfer has been canceled by the user.", "", "UPLOAD CANCELED", 2000 );
    dialog_box_form_close();
}
/*
 *********************************************************************
 *  Defining function returning AJAX settings common for all $.ajax calls. 
 *********************************************************************
 */
function ajax_settings() {
    var as = {
        // Unique parameters - MUST be set before $.ajax call,
        // f.e.: ajax_settings.url =  "/folders/ajax-report-rename" :
        //url   : ... ,
        //data  : ... ,
        // Common parameters - can be leave before $.ajax call 
        type    : "POST",
        dataType: "json",
        // Mostly common parameters - can be leave or change before $.ajax call 
        success : ajaxSuccessHandler,
        error   : xhrErrorHandler
    };
    return as;
}
/*
 *********************************************************************
 *  AJAX exchanging data with session: handlers:
 *********************************************************************
 */
function ajax_selRowIndexToSession_success_handler( json ) { // response no needed
}
function ajax_selRowIndexToSession_error_handler( xhr ) {
    xhrErrorAlert( xhr, 'ajax_selRowIndexToSession' );
}
function ajax_startRowIndexFromSession_success_handler( json ) {
    var f_name = $( "#thisfolder span" ).text();    // parent folder name
    var sr = json.server_response;
    $( "#selRowIndex" ).val( sr.selRowIndex );
    $( "#selElementModel" ).val( sr.model );
    $( "#selElementID" ).val( sr.id );
    setStartRow(); // function from folder_contents.js, which load earlier
    if ( rowsNumber === 0 ) {
        folderEmptyMessage( f_name );
    }
}
function ajax_startRowIndexFromSession_error_handler( xhr ) {
    setStartRow(); // select row for startRowIndex from previous load of this page
    xhrErrorAlert( xhr, 'ajax_startRowIndexFromSession' );
}
/*
 *********************************************************************
 *  AJAX sending data to session:
 *********************************************************************
 */
function ajax_selRowIndexToSession() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/ajax-selrowindex-to-session";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    as.success  = ajax_selRowIndexToSession_success_handler;            
    as.error    = ajax_selRowIndexToSession_error_handler;
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX receiving start RowIndex for selected row from sesssion and setting it in tag:
 *********************************************************************
 */
function ajax_startRowIndexFromSession() {
    var arr = getSelElementArr();  // at this moment the only known values are: arr.browTabName & arr.parent_id. 
                                // It is enough for start... fromSession
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/ajax-startrowindex-from-session";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    as.success  = ajax_startRowIndexFromSession_success_handler;            
    as.error    = ajax_startRowIndexFromSession_error_handler;
    $.ajax( as );
    return false;
}

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/




// From internet:===========================================================
var fr;
  function handleFileSelect()
  {
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
      alert('The File APIs are not fully supported in this browser.');
      return;
    }

    input = document.getElementById('id_file');
    if (!input) {
      alert( "Um, could not find the fileinput element." );
    }
    else if (!input.files) {
      alert( "This browser does not seem to support the `files` property of file inputs." );
    }
    else if (!input.files[0]) {
      alert( "Please select a file before clicking 'Load'" );
    }
    else {
      file = input.files[0];
    alert( "file=" + file);
    alert( "file.name=" + file.name);
      fr = new FileReader();
      fr.onload = receivedText;
      fr.readAsText(file);
      //fr.readAsDataURL(file);
    }
  }

  function receivedText() {
    //result = fr.result;
               document.getElementById('editor').appendChild(document.createTextNode(fr.result)) ;
  }

function onprogressHandler(evt) {
    var percent = evt.loaded/evt.total*100;
    console.log('Upload progress: ' + percent + '%');
}
function transferComplete(evt) {
  alert( "The transfer is complete." );
}


function encode_utf8(s) {
    console.log(s);
    console.log(encodeURIComponent(s));
    console.log(unescape(encodeURIComponent(s)));
    return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
    console.log(s);
    console.log(escape(s));
    console.log(decodeURIComponent(escape(s)));
    return decodeURIComponent(escape(s));
}
