from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you
    def __str__(self):
        """

        @return:
        @rtype:
        """
        string_rep = ''
        for x in self.from_grid:
            for i in x:
                string_rep += i
            string_rep += '\n'

        return string_rep

    def __eq__(self, other):
        """

        @param self: MNPuzzle
        @param other: MNPuzzle | Any
        @rtype: bool
        """
        return (isinstance(other, MNPuzzle) and
               self.from_grid == other.from_grid
               and self.to_grid == other.to_grid)


    # TODO
    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"

    def extensions(self):
        """

        @return:
        @rtype:
        """
        possible_moves = self._get_coord()
        empty_index = self._get_empty_space_index()
        moves = []
        for coord in possible_moves:
            moves += [MNPuzzle(self._create_new_grid(coord, empty_index),
                              self.to_grid)]
        return moves

    def _create_new_grid(self, possible_move, empty_index):
        """

        @param self:
        @type self:
        @return:
        @rtype:
        """
        grid = [list(x) for x in self.from_grid]
        grid[empty_index[1]][empty_index[0]],\
        grid[possible_move[1]][possible_move[0]] = \
            grid[possible_move[1]][possible_move[0]], '*'
        return tuple([tuple(x) for x in grid])

    def _get_empty_space_index(self):
        """

        @return:
        @rtype:
        """
        row_index = 0
        for row in self.from_grid:
            if '*' in row:
                column_index = row.index('*')
                return [column_index, row_index]
            row_index += 1


    def _get_coord(self):
        """

        @return:
        @rtype:
        """
        row_index = 0
        coord = []

        for row in self.from_grid:
            if '*' in row:
                index = row.index('*')
                if index - 1 >= 0:
                    coord += [[index-1, row_index]]
                if index + 1 < len(row):
                    coord += [[index+1, row_index]]
                if row_index - 1 >= 0:
                    coord += [[index, row_index - 1]]
                if row_index + 1 < len(self.from_grid):
                    coord += [[index, row_index + 1]]
            row_index += 1
        return coord

    # TODO
    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid

    def is_solved(self):
        """

        @return:
        @rtype:
        """
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    #target_grid = (("1", "2", "3"), ("4", "5", "*"))
    #start_grid = (("2", "*", "1"), ("3", "5", "4"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
