// JavaScript Document
console.log('start loading browtab_ajax.js');

var csrf_token;

$( document ).ready( function() {
    create_qs_TR_arr();
console.log('finished create_qs_TR_arr()');
    // csrf_token = $.cookie('csrftoken');             // Receiving the csrf_token value from cookie
    csrf_token = $( "#csrfmiddlewaretoken" ).val();   // Receiving the csrf_token value from template
    ajax_startRowIndexFromSession();                // Receiving start row index from session
console.log('finished ajax_startRowIndexFromSession()');
    return false;
});

set_browtab_ajax_listeners(); 

function set_browtab_ajax_listeners(){
    $( '#selRowIndex'     ).off( "change"        ).on( "change",         onChange_handler );
}
function onChange_handler( event ) {
console.log('onChange_handler start');
    ajax_selRowIndexToSession();                    // Sending selected row index to session
console.log('onChange_handler finish');
    return false;
}


/*
 *********************************************************************
 *  Defining error and cancel handlers for xhr: 
 *********************************************************************
 */
function xhrErrorAlert( xhr, ss ) {
    if ( ss === undefined ) { ss = ''; }
    alert('xhrErrorAlert:' + 
                '\n xhr.status='        + xhr.status + 
                '\n xhr.statusText='    + xhr.statusText + 
                '\n xhr.responseText='  + xhr.responseText );
}
function xhrErrorHandler(xhr) {
    if ( xhr.status == 401 || xhr.status == 403 ) { // Redirect to login
        //window.location = xhr.responseText;
        dialogMessage( "Ви не маєте доступу до цієї операції!",
                      "Error", "Помилка доступу", 3000 );
        $( "#dialog-box-form" ).dialog( "close" );
    } else {
        xhrErrorAlert( xhr, 'xhrErrorHandler' ); }
}
function transferFailed( evt ) {
	dialogMessage( "An error occurred while transferring the file. Probably file too long", 
                        "Error", "UPLOAD ERROR", 3000 );
    $( "#dialog-box-form" ).dialog( "close" );
//  alert( "An error occurred while transferring the file." );
}
function transferCanceled( evt ) {
	dialogMessage( "The transfer has been canceled by the user.", "", "UPLOAD CANCELED", 2000 );
    $( "#dialog-box-form" ).dialog( "close" );
    
//  alert( "The transfer has been canceled by the user." );
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
 *  AJAX sending data to session:
 *********************************************************************
 */
function ajax_selRowIndexToSession() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/ajax-selrowindex-to-session";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    as.success = function( json ) { };            // response no needed
    as.error = function( xhr ) {
            xhrErrorAlert( xhr, 'ajax_selRowIndexToSession' );
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX receiving start RowIndex for selected row from sesssion and setting it in tag:
 *********************************************************************
 */
function ajax_startRowIndexFromSession() {
    var f_name = $( "#thisfolder span" ).text();    // parent folder name
    var arr = selElementArr();  // at this moment the only known values are: arr.browTabName & arr.parent_id. 
                                // It is enough for start... fromSession
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/ajax-startrowindex-from-session";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    as.success = function( json ) {
            var sr = json.server_response;
            $( "#selRowIndex" ).val( sr.selRowIndex );
            $( "#selElementModel" ).val( sr.model );
            $( "#selElementID" ).val( sr.id );
            setStartRow(); // function from folder_contents.js, which load earlier
            if ( rowsNumber === 0 ) {
                folderEmptyMessage( f_name );
            }
        };
    as.error = function( xhr ) {
            setStartRow(); // select row for startRowIndex from previous load of this page
            xhrErrorAlert( xhr, 'ajax_startRowIndexFromSession' );
        };
    $.ajax( as );
    return false;
}



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
