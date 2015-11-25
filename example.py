import os

def file_directory_print(startFolder):
    for (thisFolder, foldersList, filesList) in os.walk(startFolder):   # обходимо дерево
        '''
        thisFolder - на кожному рекурсивному кроці це папка,
                        в якій шукаються файли (ця папка)
        foldersList - список папок у цій папці
        filesList - список файлів у цій папці
        '''
        print('-'*50)
        print(thisFolder)
        print('-'*50)
        for filename in filesList:  # обходимо всі файли у цій папці
            pathfilename = os.path.join(thisFolder,filename)    # повна назва файлу з шляхом
            # print(pathfilename)
            print(filename)

startFolder = 'c:\pyPrograms\Django\koopsite\static'
file_directory_print(startFolder)