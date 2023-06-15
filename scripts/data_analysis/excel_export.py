from openpyxl import Workbook

from enum import Enum

class ColorMode(Enum):
    all = 0,
    red = 1,
    green = 2,
    blue = 3

def exportToExcel(columNames, data, filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(columNames)

    for row in data:
        sheet.append(row)

    workbook.save(filename)
