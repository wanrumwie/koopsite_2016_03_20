__author__ = 'Мирослава'
'''
Функції для доступу до даних з таблиць в базі даних Access
'''

import pypyodbc

pypyodbc.lowercase = False

def mdbTableList(cursor):
    # повертає список таблиць і запитів у базі даних
    tab = cursor.tables()
    tableList = []
    queryList = []
    for t in tab:
        if t[3] == "TABLE": tableList.append(t[2])
        if t[3] == "VIEW" : queryList.append(t[2])
    return tableList, queryList

def mdbColumnList(cursor, table):
    # повертає список найменувань полів у таблиці у базі даних
    col = cursor.columns(table=table)
    columnList = []
    for c in col:
        columnList.append(c[3])
    return columnList

def mdbColumnParameters(cursor, table, column):
    # повертає кортеж параметрів обраної колонки
    col = cursor.columns(table=table, column=column)
    l = list(col)
    t = l[0]
    return t

def rowAttributes(row):
    # повертає словник: {columnName: n},
    # де n - номер елемента в кортежі row,
    # який відповідає колонці з назвою columnName
    coldict = {}
    # також повертає список тих же columnname
    # (сортований на відміну від словника)
    collist = []
    for i in range(len(row.cursor_description)):
        columnName = row.cursor_description[i][0]
        collist.append(columnName)
        coldict[columnName] = i
    return coldict, collist

def allfieldnamesprint(cursor):
    print('-'*50)
    print('ДРУК НАЗВ КОЛОНОК ВСІХ ТАБЛИЦЬ У БАЗІ ДАНИХ access:')
    tableList, queryList = mdbTableList(cursor)
    for table in tableList:
        print('-'*50)
        print('table=', table)
        print('-'*50)
        columnList = mdbColumnList(cursor, table)
        for column in columnList:
            columnParameters = mdbColumnParameters(cursor, table, column)
            s = '"%s"' % columnParameters[3]
            print(': %-40s' % s)

