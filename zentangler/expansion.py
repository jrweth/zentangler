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

        self.matched = []
        self.added = []
        self.remainder = []

        if matched is not None:
            self.matched = matched

        if added is not None:
            self.added = added

        if remainder is not None:
            self.remainder = remainder

        self.shapes = self.appendAllShapes()

    def appendAllShapes(self):
        self.shapes = []

        if self.matched is not None:
            for m in self.matched:
                self.shapes.append(m)

        if self.added is not None:
            for a in self.added:
                self.shapes.append(a)

        if self.remainder is not None:
            for r in self.remainder:
                self.shapes.append(r)

        return self.shapes
                
    def addToMatched(self, shape: Shape):
        self.matched.append(shape)
        self.shapes.append(shape)
        
    def addToAdded(self, shape: Shape):
        self.added.append(shape)
        self.shapes.append(shape)

    def addToRemainder(self, shape: Shape):
        self.remainder.append(shape)
        self.shapes.append(shape)

    def getShapesForNewExpansion(self):
        shapes = []

        if self.added is not None:
            for a in self.added:
                shapes.append(a)

        if self.remainder is not None:
            for r in self.remainder:
                shapes.append(r)

        return shapes
