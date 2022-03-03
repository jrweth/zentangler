from zentangler.operator.ungroup_operator import UngroupOperator

class Grammar:
    def load_from_file(self, filename):
        op = UngroupOperator()
        self.operators.push(op)

    def load_from_string(self, grammar_string):
        op = UngroupOperator()
        self.operators.push(op)