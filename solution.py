#!/usr/bin/env python

class Solution(object):

    def __init__(self, keys=(), values=()):
        self.values = values
        self.keys = keys


    def add(self, keys=(), values=()):
        self.add_values(values)
        self.add_keys(keys)


    def add_keys(self, keys=()):
        if (
            self._is_valid_input(keys) and
            len(self._keys.union(keys)) <= len(self._values)
        ):
            self._keys.update(keys)
        else:
            raise ValueError("Cannot add keys: {keys}".format(
                keys=keys
            ))


    def add_values(self, values=()):
        if self._is_valid_input(values):
            self._values.update(values)
        else:
            raise ValueError("Cannot add values: {values}".format(
                values=values
            ))


    @property
    def complete(self):
        return(len(self.keys) == len(self.values))


    def delete(self, keys=(), values=()):
        self.delete_keys(keys)
        self.delete_values(values)


    def delete_keys(self, keys=()):
        if self._is_valid_input(keys):
            self._keys -= keys
        else:
            raise ValueError("Cannot delete keys: {keys}".format(
                keys=keys
            ))


    def delete_values(self, values=()):
        if self._is_valid_input(values):
            self._values -= values
        else:
            raise ValueError("Cannot delete values".format(
                values=values
            ))


    @property
    def keys(self):
        return(self._keys)


    @keys.setter
    def keys(self, keys):
        self._keys = set([])
        self.add_keys(keys)


    @property
    def solved(self):
        return(
            self.complete and
            len(self.keys) == 1
        )


    @property
    def values(self):
        return(self._values)


    @values.setter
    def values(self, values):
        self._values = set([])
        self.add_values(values)


    def _is_valid_input(self, values):
        return(
            isinstance(values, (list, tuple)) and
            len(filter(lambda v: isinstance(v, int), values)) == len(values)
        )


    def __str__(self):
        return("[{keys}] = [{values}]".format(
            keys=", ".join(map(lambda v: str(v), sorted(self._keys))),
            values=", ".join(map(lambda v: str(v), sorted(self._values)))
        ))


    def __repr__(self):
        return(self.__str__())


class SolutionSet(object):

    def __init__(self, solutions=()):
        self.solutions = solutions


    def add(self, solution=Solution()):
        if self._is_valid_input(solution):
            for s in self.solutions:
                if s.values == solution.values:
                    s.add_keys(list(solution.keys))
                    break
            else:
                self._solutions.append(solution)
        else:
            raise ValueError("Cannot add solution: {solution}".format(
                solution=solution
            ))


    def append(self, solutions=(Solution(),)):
        if isinstance(solutions, (list, tuple)):
            for solution in solutions:
                self.add(solution)
        else:
            raise ValueError("Cannot add solutions: {solutions}".format(
                solutions=solutions
            ))


    @property
    def solutions(self):
        return(self._solutions)


    @solutions.setter
    def solutions(self, solutions):
        self._solutions = []
        self.append(solutions)


    @property
    def solved(self):
        return(
            len(self.solutions) == len(
                filter(lambda s: s.solved, self.solutions)
            )
        )

    def _is_valid_input(self, value):
        return(isinstance(value, Solution))


    def __str__(self):
        return("\n".join(map(lambda s: str(s), self.solutions)))


    def __repr__(self):
        return(self.__str__())
