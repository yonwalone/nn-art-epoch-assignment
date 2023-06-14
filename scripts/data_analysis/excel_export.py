from openpyxl import Workbook

def exportToExcel(columNames, data, filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(columNames)

    for row in data:
        sheet.append(row)

    workbook.save(filename)
