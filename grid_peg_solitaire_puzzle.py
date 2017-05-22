from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you
    def __str__(self):
        """

        @return:
        @rtype:
        """
        string_rep = ''
        for x in self._marker:
            for i in x:
                string_rep += i
            string_rep += '\n'

        return string_rep

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other

        @param self: GridPegSolitairePuzzle
        @param other: GridPegSolitairePuzzle | Any
        @rtype: bool
        """
        return (type(self) == type(other) and self._marker == other._marker and
                self._marker_set == other._marker_set)

    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """

        @return:
        @rtype:

        >>> grid = []
        >>> grid += [".", ".", ".", "."]
        >>> grid += [".", ".", "*", "*"]
        >>> grid += [".", "*", ".", "."]
        >>> grid += [".", "*", ".", "."]
        >>> g = GridPegSolitairePuzzle(grid, {".", "*", "#"})
        """
        moveable_pieces = self._get_coord()
        possible_moves = []

        for piece in moveable_pieces:
            grid = self._create_new_grid(piece[0], piece[2], piece[1])
            possible_moves += [GridPegSolitairePuzzle(grid, {"*", ".", "#"})]

        return possible_moves


    def _create_new_grid(self, piece_move, piece_del, empty):
        """
        Return a new grid given the coordinates of the piece to move, the
        piece being jumped over and the empty space

        @param
        """
        grid = self._copy_grid()
        grid[piece_move[1]][piece_move[0]] = '.'
        grid[piece_del[1]][piece_del[0]] = '.'
        grid[empty[1]][empty[0]] = '*'
        return grid

    def _copy_grid(self):
        grid = []
        for row in self._marker:
            row_elements = []
            for element in row:
                row_elements.append(element)
            grid.append(row_elements)
        return grid

    def _get_coord(self):
        """

        @return:
        @rtype:
        """
        coord = []
        row_index = 0
        for row in self._marker:
            if '.' in row:
                index = row.index('.')
                if index - 2 >= 0 and row[index - 2] == '*' and \
                        row[index - 1] == '*':
                    coord += [[[index - 2, row_index], [index, row_index],
                               [index - 1, row_index]]]

                if index + 2 < len(row) and row[index + 2] == '*' and \
                        row[index + 1] == '*':
                    coord += [[[index + 2, row_index], [index, row_index],
                              [index + 1, row_index]]]

                if row_index - 2 >= 0 and self._marker[row_index - 2][index]\
                        == '*' and self._marker[row_index - 1][index] == '*':
                    coord += [[[index, row_index - 2], [index, row_index],
                               [index, row_index - 1]]]

                if row_index + 2 < len(row) and self._marker[row_index + 2]\
                        [index] == '*' and self._marker[row_index + 1][index]\
                        == '*':
                    coord += [[[index, row_index + 2], [index, row_index],
                               [index, row_index + 1]]]
            row_index += 1
        return coord

    # TODO
    # override is_solved
    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """

        @return:
        @rtype:
        """
        count = 0
        for element in self._marker:
            for i in element:
                if i == '*':
                    count += 1
        return count == 1

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time
    start = time.time()
    from puzzle_tools import breadth_first_solve
    #solution2 = breadth_first_solve(gpsp)
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
