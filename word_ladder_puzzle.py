from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

        # implement __eq__ and __str__
        # __repr__ is up to you
    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle self.

        >>> word_set = {'came', 'case', 'cast', 'cost'}
        >>> s = WordLadderPuzzle("same", "cost", word_set)
        >>> print(s)
        same
        """
        return self._from_word

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other

        @param self: WordLadderPuzzle
        @param other: WordLadderPuzzle | Any
        @rtype: bool

        >>> word_set = {'came', 'case', 'cast', 'cost'}
        >>> s = WordLadderPuzzle("same", "cost", word_set)
        >>> s2 = WordLadderPuzzle("same", "cost", word_set)
        >>> s == s2
        True
        >>> s3 = WordLadderPuzzle("cost", "same", word_set)
        >>> s == s3
        False
        """
        return isinstance(other, WordLadderPuzzle) and (self._from_word ==
                                                        other._from_word and
                                                        self._to_word ==
                                                        other._to_word)

        # override extensions
        # legal extensions are WordLadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars
    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> word_set = {'came', 'case', 'cast', 'cost'}
        >>> s = WordLadderPuzzle("same", "cost", word_set)
        >>> s2 = WordLadderPuzzle("came", "cost", {'case', 'cast', 'cost'})
        >>> s2 in s.extensions()
        True
        >>> s3 = WordLadderPuzzle("same", "cost", set())
        >>> s3.extensions() is None
        True
        """
        if len(self._word_set) == 0:
            return None
        else:
            filtered_words = self._filter_len()
            usable_words = self._usable_word(filtered_words)
            extensions = []

            for word in usable_words:
                new_copy = filtered_words.copy()
                new_copy.discard(word)
                extensions.append(WordLadderPuzzle(word, self._to_word,
                                                   new_copy))
            return extensions

        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word
    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> word_set = {'came', 'case', 'cast', 'cost'}
        >>> s = WordLadderPuzzle("cost", "cost", word_set)
        >>> s.is_solved()
        True
        >>> s2 = WordLadderPuzzle("same", "cost", word_set)
        >>> s2.is_solved()
        False
        """
        return self._from_word == self._to_word

    # Helper Methods
    def _usable_word(self, filtered_words):
        """
        Return a set of words that have only a 1 letter difference from
        self._from_word.

        @type filtered_words: set{str}
        @type self: WordLadderPuzzle
        @rtype: set{str}
        """
        usable = set()
        for word in filtered_words:
            counter = 0
            for x in range(0, len(self._to_word)):
                if word[x] == self._from_word[x]:
                    counter += 1
            if counter == len(self._to_word) - 1:
                usable.add(word)
        return usable

    def _filter_len(self):
        """
        Return a set of words that have the same length as self.to_word

        @type self: WordLadderPuzzle
        @rtype: set{str}
        """
        if max([len(x) for x in self._word_set]) == len(self._to_word):
                return self._word_set
        else:
            new_words = set()
            for word in self._word_set:
                if len(self._from_word) == len(word):
                    new_words.add(word)

            return new_words

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
