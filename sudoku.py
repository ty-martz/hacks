solution = [[9, 5, 3, 1, 6, 7, 4, 2, 8],
          [4, 2, 8, 3, 5, 9, 7, 6, 1],
          [7, 6, 1, 8, 2, 4, 9, 5, 3],
          [5, 8, 4, 9, 3, 6, 2, 1, 7],
          [6, 3, 9, 7, 1, 2, 5, 8, 4],
          [2, 1, 7, 4, 8, 5, 6, 3, 9],
          [3, 4, 5, 6, 9, 1, 8, 7, 2],
          [8, 7, 2, 5, 4, 3, 1, 9, 6],
          [1, 9, 6, 2, 7, 8, 3, 4, 5]]  

board = [[0, 0, 0, 0, 0, 0, 6, 8, 0],
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
        if num == grid[row][x]:
            return False
    for x in range(9):
        if num == grid[x][col]:
            return False
    
    crow = row - row % 3
    ccol = col - col % 3

    for r in range(3):
        for c in range(3):
            if grid[crow+r][ccol+c] == num:
                return False

    return True


def solve(grid, row, col):
    #print(f'ROW={row}, COL={col}')

    # check for end of line
    if col == 9:
        if row == 8:
            return True, grid
        row += 1
        col = 0

    # check if should be solved
    if grid[row][col] > 0:
        solve(grid, row, col + 1)

    # solve
    for n in range(1,10):
        if check_valid(grid, n, row, col):
            grid[row][col] = n

            if solve(grid, row, col+1)[0]:
                return True, grid

        grid[row][col] = 0

    return False, grid

soln = solve(board, 0, 0)
if soln[0]:
    print(soln[1])