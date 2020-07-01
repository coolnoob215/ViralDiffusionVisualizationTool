import sys
import os
import visualization
from xlwt import Workbook


def generate_excel(num):
    if os.path.exists("Transmission Rate Inputs.xls"):
        os.remove("Transmission Rate Inputs.xls")

    wb = Workbook()
    sheet = wb.add_sheet("Transmission Rate Inputs")

    for i in range(num):
        sheet.write((i + 1), 0, "Node {}".format(i))
        sheet.write(0, (i + 1), "Node {}".format(i))

        for j in range(num):
            sheet.write((i + 1), (j + 1), 0.0)

    wb.save('Transmission Rate Inputs.xls')


def main(num):
    generate_excel(num)
    fig = visualization.Figure(num)
    visualization.show()


if __name__ == '__main__':
    num_nodes = float(sys.argv[1])
    if not num_nodes.is_integer() or num_nodes <= 0:
        raise Exception("Only Positive Integers are allowed.")
    if num_nodes > 12:
        raise Exception("Values greater than 12 are not supported at this time due to figure size.")
    main(int(num_nodes))
