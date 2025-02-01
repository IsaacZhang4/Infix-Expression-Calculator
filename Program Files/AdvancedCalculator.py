from Calculator import Calculator

class AdvancedCalculator:
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        # Check if empty
        if not word:
            return False
        # Check if alphanumeric
        if not word.isalnum():
            return False
        # Check if first char is not alphabetical
        if not word[0].isalpha():
            return False
        return True

    def _replaceVariables(self, expr):
        output = []
        buffer = []
        prevChar = ''
        # Iterate through expression
        for char in expr + ' ':
            # If potential variable, add to buffer
            if char.isalnum():
                buffer.append(char)
            else:
                # If buffer is not empty, handle items
                if len(buffer) > 0:
                    word = ''.join(buffer)
                    if self._isVariable(word):
                        if word in self.states:
                            output.append(str(self.states[word]))
                        else:
                            return None  # Variable does not exist in states
                    else:
                        output.append(word)
                    buffer.clear()
                if char != ' ' or prevChar != ' ':  # To remove redundant spacer
                    output.append(char)
            prevChar = char
        # Join output with space and strip ending spaces
        return ''.join(output).strip()

    def calculateExpressions(self):
        self.states = {}
        calcObj = Calculator()  # method must use calcObj to compute each expression

        # Check for invalid expression
        if not self.expressions:
            return self.states

        output = {}
        # Attempt to calculate
        try:
            # Separate with ';'
            for line in self.expressions.split(';'):
                line = line.strip()
                variable = None
                expression = None
                # Separate with '='
                for sect in line.split('=', 1):  # Maximum split into two sections
                    if expression is None:
                        expression = sect.strip()
                    else:
                        variable = expression
                        expression = sect.strip()
                # Check if the variable is valid
                if not variable:
                    if line.startswith('return'):
                        variable = '_return_'
                        expression = line[len('return'):].strip()
                    else:
                        raise Exception(f"Line \"{line}\" does not contain '=' or starts with 'return'.")
                if not self._isVariable(variable) and variable != '_return_':
                    raise Exception(f"Variable name \"{variable}\" is invalid in line \"{line}\".")
                if not expression:
                    raise Exception(
                        f"Line \"{line}\" does not contain expression to calculate value for variable \"{variable}\".")
                # Replace the variables in expression with values and calculate
                if expression:
                    exprReplaced = self._replaceVariables(expression)
                    if exprReplaced is None:
                        raise Exception(f"Can not replace expression \"{expression}\" with variable values.")
                    # Replace variables in the expression with runtime values
                    calcObj.setExpr(exprReplaced)
                    result = calcObj.calculate  # Calculate
                    if result is None:
                        raise Exception(
                            f"Error to calculate value of expression \"{exprReplaced}\" in line \"{line}\".")
                    self.states[variable] = result
                # Check if the current variable is '_return_' for a special handling
                if variable == "_return_":
                    output["_return_"] = self.states["_return_"]
                    del self.states["_return_"]
                else:
                    # Make a top-level copy of self.states
                    statesCopy = {}
                    for key in self.states:
                        statesCopy[key] = self.states[key]
                    output[line] = statesCopy  # Put the copy into output
        # Case where calculation failed
        except Exception as e:
            self.states = {}
            return None
        return output