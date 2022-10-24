grid = [[0, 0, 0, 0, 0, 0, 6, 8, 0],
        [0, 0, 0, 0, 7, 3, 0, 0, 9],
        [3, 0, 9, 0, 0, 0, 0, 4, 5],
        [4, 9, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 3, 0, 5, 0, 9, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 3, 6],
        [9, 0, 6, 0, 0, 0, 3, 0, 8],
        [7, 0, 0, 6, 8, 0, 0, 0, 0],
        [0, 2, 8, 0, 0, 0, 0, 0, 0]]

def check_valid(grid, num, row, col):

    for x in range(9):
        if grid[row][x] == num:
            return False
        if grid[x][col] == num:
            return False
    
    crow = row - row % 3
    ccol = col - col % 3
    for r in range(3):
        for c in range(3):
            if grid[crow+r][ccol+c] == num:
                return False

    return True


def solve(grid, row, col):

    # check for end of line
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    # check if should be solved
    if grid[row][col] > 0:
        solve(grid, row, col + 1)

    # solve
    for n in range(1,10):
        if check_valid(grid, n, row, col):
            grid[row][col] = n

            if solve(grid, row, col+1):
                return True

        #grid[row][col] = 0

    return False, grid


if solve(grid,0,0):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' ')
        print()
else:
    print('No Solution')