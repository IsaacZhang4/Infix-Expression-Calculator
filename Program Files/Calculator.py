from Stack import Stack

class Calculator:
    def __init__(self):
        self.__expr = None

    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr = new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        # Use try: except to attempt float conversion if it works, return True else False
        try:
            num = float(txt)
            return True
        except:
            return False

    # Define dict for operation characters and precedences
    operations = {
        'precedence': {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        },
        'operators': ['+', '-', '*', '/', '^'],
        'enclosures': ['()', '[]', '{}'],
        'whitespaces': [' '],
        'operandAllowed': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    }

    # Create function to check if input is operator
    def __isOperator(self, value):
        return value is not None and value in self.operations['operators']

    # Create function to check if input is an enclosure symbol
    def __isEnclosure(self, value):
        return value is not None and value in self.operations['enclosures']

    # Create function to get the precedence of an operator
    def __getOperatorPrecedence(self, value):
        return self.operations['precedence'][value]

    # Create function for checking if a char is valid for the calculation and postfix conversion

    def __validateChar(self, value):
        # Check if empty
        if not value:
            return None
        # Check if operator
        if value in self.operations['operators']:
            return {
                'operator': value,
                'precedence': self.operations['precedence'][value]
            }
        # Check if whitespace
        if value in self.operations['whitespaces']:
            return {
                'whitespace': value,
            }
        # Check if operand
        if value in self.operations['operandAllowed']:
            return {
                'operand': value
            }
        # Check if enclosure symbol
        for enclosure in self.operations['enclosures']:
            if value in enclosure:
                return {
                    'char': value,
                    'enclosure': {'begin': enclosure[0], 'end': enclosure[1]},
                    'isBegin': value == enclosure[0]
                }
        # Else, return None
        return None

    # Create function for handling operators as they appear
    def __handleOperator(self, operator, postfixStack, output, lastHandled):
        # Input operator must be a dict holding the operator validation, if not, return None
        if len(output) == 0:
            return None
        if lastHandled['type'] == 'operator':
            return None
        if lastHandled['type'] == 'begin':
            return None

        topValue = postfixStack.peek()
        popContinue = True
        # Iterate through stack for precedence
        while topValue and popContinue:
            if self.__isOperator(topValue):
                # Handle case by case based on operator precedence
                if topValue == '^' and operator['operator'] == '^':
                    popContinue = False
                else:
                    if self.__getOperatorPrecedence(topValue) >= operator['precedence']:
                        output.append(postfixStack.pop())
                        topValue = postfixStack.peek()
                    else:
                        popContinue = False
            else:  # enclosure is encountered because only operators and begin char of enclosure exists in the stack.
                popContinue = False
        postfixStack.push(operator['operator'])
        lastHandled['type'] = 'operator'
        lastHandled['operatorCount'] += 1

        return lastHandled

    def _getPostfix(self, txt):
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression

        # Check for cases where the input expression is invalid
        if not isinstance(txt, str) or not txt:
            return None

        output = []  # Store output of infix to postfix conversion
        operandBuffer = []  # Buffer to temporarily hold operand allowed chars
        lastHandled = {'type': '', 'prevCharWhitespace': False, 'operandCount': 0, 'operatorCount': 0}
        # Above 'type' in lastHandled marks what type is handled last time, 'operand' for operand, 'operator' for operator, 'begin' for begin enclosure, 'end' for end enclosure
        # Above 'prevCharWhitespace' in lastHandled, if true, the immediately previous char evaluated is a whitespace. Othwerwise, it is not.
        for char in txt + ' ':
            # Check for valid expression
            validation = self.__validateChar(char)
            if validation is None:
                return None
            # Case for operand
            if 'operand' in validation:
                operandBuffer.append(validation['operand'])
            else:
                # Enter operand if buffer is not empty
                if operandBuffer:
                    operand = ''.join(operandBuffer)
                    if self._isNumber(operand):
                        if lastHandled['type'] == 'end':  # Add implicit '*' operator for operand when last handle is end char of enclosure.
                            if not self.__handleOperator(self.__validateChar('*'), postfixStack, output, lastHandled):
                                return None
                        # Case where operand followed by operand
                        if lastHandled['type'] == 'operand':
                            return None
                        output.append(str(float(operand)))  # Output operand, also formatting operand before output.
                        lastHandled['type'] = 'operand'
                        lastHandled['operandCount'] += 1
                    # Case where operand is not operand
                    else:
                        return None
                    operandBuffer.clear()
                # Case for enclosure symbol
                if 'enclosure' in validation:
                    if validation['isBegin']:  # Handle begin char of enclosure
                        if lastHandled['type'] == 'operand' or lastHandled['type'] == 'end':  # Add implicit operator '*' if begin char of enclosure follows an operand or an end char of enclosure
                            if not self.__handleOperator(self.__validateChar('*'), postfixStack, output, lastHandled):
                                return None
                        postfixStack.push(validation['enclosure']['begin'])  # Push begin char of enclosure to stack
                    else:  # Handle end char of enclosure
                        # Case where operator is right before end enclosure
                        if lastHandled['type'] == 'operator':
                            return None
                        matchChar = validation['enclosure']['begin']
                        matched = False
                        topValue = postfixStack.peek()
                        # Handle enclosure content
                        while topValue and not matched:
                            if topValue == matchChar:  # Matched begin char of enclosure
                                postfixStack.pop()
                                matched = True
                            else:
                                if not self.__isEnclosure(topValue):
                                    output.append(postfixStack.pop())  # Pop and put to output
                                else:
                                    return None
                            topValue = postfixStack.peek()
                        # Case where no matching enclosure
                        if not matched:
                            return None
                    lastHandled['type'] = 'begin' if validation['isBegin'] else 'end'
                # Case for operator
                elif 'operator' in validation:
                    if validation['operator'] == '-' and (
                            lastHandled['type'] == '' or lastHandled['type'] == 'begin' or (
                            lastHandled['type'] == 'operator' and lastHandled['prevCharWhitespace'])):
                        operandBuffer.append(validation['operator'])  # treated as negative sign
                    elif not self.__handleOperator(validation, postfixStack, output, lastHandled):
                        return None

                if 'whitespace' in validation:
                    lastHandled[
                        'prevCharWhitespace'] = True  # This is to help determine whether '-' should be treated as an operator or a negative sign of operand.
                else:
                    lastHandled['prevCharWhitespace'] = False
        # Output remaining operators in the stack, also checking enclosure that should not exist.
        while not postfixStack.isEmpty():
            topValue = postfixStack.pop()
            if self.__isOperator(topValue):
                output.append(topValue)
            # Case where enclosure exists but shouldn't
            else:
                return None
        # Check for operands dealt with doesn't match operators which implies invalid expression
        if lastHandled['operandCount'] != lastHandled['operatorCount'] + 1:
            return None

        postfix = ' '.join(output)

        return postfix

    @property
    def calculate(self):
        if not isinstance(self.__expr, str) or len(self.__expr) <= 0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()  # method must use calcStack to compute the  expression

        # Check for case where input expression is invalid
        postfix = self._getPostfix(self.getExpr)
        if not postfix:
            return None

        # Split postfix by ' ' and calculate using calcStack
        for token in postfix.split(' '):
            # If token is operand, push to stack, else, perform calculation
            if not self.__isOperator(token):
                try:
                    calcStack.push(float(token))  # Push operand to stack
                except:
                    return None
            else:  # this is operator
                operator = token
                operand1 = calcStack.pop()
                operand2 = calcStack.pop()
                # Attempt to calculate
                try:
                    if operand1 is not None and operand2 is not None:
                        result = None
                        # Case for addition
                        if operator == '+':
                            result = operand2 + operand1
                        # Case for subtraction
                        elif operator == '-':
                            result = operand2 - operand1
                        # Case for multiplication
                        elif operator == '*':
                            result = operand2 * operand1
                        # Case for division
                        elif operator == '/':
                            result = operand2 / operand1
                        # Case for exponents
                        elif operator == '^':
                            result = operand2 ** operand1
                        # Case for invalid operator
                        else:
                            raise Exception(f"Unsupported operator {operator} is met. Invalid expression to calculate.")
                        # Check for empty calculation
                        if result is not None:
                            calcStack.push(result)
                        else:
                            raise Exception("Calculation failed.")
                    # Case for invalid opeartors
                    else:
                        raise Exception("Invalid expression to calculate")
                # Case for calculation failed
                except Exception as e:
                    return None
        # Check for empty result
        if len(calcStack) != 1:
            return None
        return calcStack.pop()