from zentangler.shape import Shape


class Expansion:
    """
    Expansion class that holds the state of tangle at a point in process of expansion
        (probably after a rule was applied)
        The shapes in a tangle at a particular expansion are the shapes in added & remainder
    """

    def __init__(self, matched: list, added: list, remainder: list): #, rule_applied):    # ??: include rule applied
        """
        initialize an expansion

        Parameters:
            matched: set of shapes matched with the rule
            added: set of new shapes added after rule is applied
            remainder: set of shaped on which rule was not applied
        """
        self.matched = matched
        self.added = added
        self.remainder = remainder

        self.shapes = []
        for m in matched:
            self.shapes.append(m)
        for a in added:
            self.shapes.append(a)
        for r in remainder:
            self.shapes.append(r)
