import os
import zipfile
from io import BytesIO
from django.http.response import HttpResponse
from folders.models import Report, Folder
from koopsite.fileExtMimeTypes import mimeType
from koopsite.settings import MEDIA_ROOT

def response_for_download(report):
    """
    Preparing response for downloading file
    Content-Disposition header field from http://tools.ietf.org/html/rfc2183
    :param:     report - instance of Report model
    :return:    HttpResponse with report.file and some parameters
    """
    fileExt  = os.path.splitext(report.filename)[1]  # [0] returns path+filename
    ct = mimeType.get(fileExt.lower(), "application/octet-stream")
    fn = '; filename="%s"' % report.filename
    md = '; modification-date="%s"' % report.uploaded_on
    response = HttpResponse(report.file, content_type=ct)
    response['Content-Disposition'] = 'attachment' + fn + md
    response['Content-Length'] = report.file.size
    # print('response_for_download = ', response)
    return response

def response_for_download_zip(folder):
    """
    Preparing response for downloading zip-file,
    consist of all files in folder (without recursion!)
    Content-Disposition header field from http://tools.ietf.org/html/rfc2183
    :param:     folder - instance of Folder model
    :return:    HttpResponse with zip file and some parameters
                Message in case of zip file overflow max size
    """
    zipSubdir = folder.name
    zipFilename = "%s.zip" % folder.name
    sio = BytesIO()  # Open StringIO to grab in-memory ZIP contents
    zipFile = zipfile.ZipFile(sio, "w")    # The zip compressor
    maxFileSize = 200000000
    zipFileSize = 0
    msg = ""
    for report in Report.objects.filter(parent_id=folder.id):
        zipFileSize += report.file.size         #
        if zipFileSize > maxFileSize:
            msg = 'Завеликий zip. Решту файлів відкинуто'
            print(msg)
            break
        filename = report.filename              # "людська" назва файла
        filepath = report.file.name             # шлях до файла на диску
        abs_path = os.path.join(MEDIA_ROOT, filepath)
        zipPath = os.path.join(zipSubdir, filename) # шлях в архіві
        print("%-3s %-7s %-20s %-20s %-20s" % (report.id, filename, filepath, abs_path, zipPath))
        zipFile.write(abs_path, zipPath)            # add file to zip
    print('цикл закінчено')
    zipFile.close() # Must close zip for all contents to be written
    print('zipfile closed')
    fileExt  = ".zip"
    ct = mimeType.get(fileExt.lower(), "application/octet-stream")
    fn = '; filename="%s"' % zipFilename
    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = HttpResponse(sio.getvalue(), content_type=ct)
    response['Content-Disposition'] = 'attachment' + fn
    response['Content-Length'] = len(sio.getbuffer())
    return response, zipFilename, msg


tab = ' '*4

def wrap_li(level, folder):
    indent = tab * level
    li = indent + '<li id="%s">%s\n' % (folder.id, folder.name)
    qs = folder.children.all().order_by('name'.lower())
    if qs:
        li = li + wrap_ul(level, qs)
    li = li + indent + '</li>\n'
    return li

def wrap_ul(level, qs):
    indent = tab * level
    ul = indent + tab + '<ul>\n'
    for f in qs:
        ul = ul + wrap_li(level+2, f)
    ul = ul + indent + tab + '</ul>\n'
    return ul

def get_folders_tree_HTML(parent_qs=None):
    level = 0
    qs = parent_qs or Folder.objects.filter(parent=None).order_by('name'.lower())
    html = wrap_ul(level, qs)
    return html


