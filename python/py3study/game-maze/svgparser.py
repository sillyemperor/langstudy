def SetWall(mapData, row, col):
    row = int(row)
    col = int(col)
    mapData[col][row] = '#'


def SetStart(mapData, rows, cols):
    for col in range(cols):
        for row in range(rows):
            if row and col and row < rows - 1 and col < cols - 1:
                continue
            if ' ' == mapData[col][row]:
                mapData[col][row] = 'S'
                return


def SetEnd(mapData, rows, cols):
    for col in range(cols):
        for row in range(rows):
            if row and col and row < rows-1 and col < cols-1:
                continue
            if ' ' == mapData[col][row]:
                mapData[col][row] = 'X'
                return


def parsesvg(f):
    from xml.dom import minidom

    doc = minidom.parse(f)

    outline = [(int(i.getAttribute('width')) // 30 - 2, int(i.getAttribute('height')) // 30 - 2) for i in
               doc.getElementsByTagName('rect')][0]

    path_strings = [(float(path.getAttribute('x1')), float(path.getAttribute('y1')), float(path.getAttribute('x2')),
                     float(path.getAttribute('y2'))) for path
                    in doc.getElementsByTagName('line')]
    doc.unlink()

    cols = 2 * outline[0] + 1
    rows = 2 * outline[1] + 1

    mapData = [list([' '] * rows) for i in range(cols)]

    for i in path_strings:
        x1 = i[0]
        y1 = i[1]
        x2 = i[2]
        y2 = i[3]
        print(i)
        if x1 != x2 and y1 == y2:
            x3 = x1 + (x2 - x1) // 2
            col = int(y1 // 15)
            print('H', x2, col)
            SetWall(mapData, x1 // 15, col)
            SetWall(mapData, x2 // 15, col)
            SetWall(mapData, x3 // 15, col)
        if y1 != y2 and x1 == x2:
            y3 = y1 + (y2 - y1) // 2
            row = int(x1 // 15)
            print('V', y3, row)
            SetWall(mapData, row, y1 // 15)
            SetWall(mapData, row, y2 // 15)
            SetWall(mapData, row, y3 // 15)

    SetStart(mapData, rows, cols)
    SetEnd(mapData, rows, cols)

    return '\n'.join([''.join(r) for r in mapData])