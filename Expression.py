#
#   Expression.py
#

# class Expression
# - super class for the expressions
class Expression:
    def __init__(self, operator, op1, op2 = None):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2 == None:
            return "%s%s" % (self.operator, self.op1)
        return "%s %s %s" % (self.op1, self.operator, self.op2)
    
    def __len__(self):
        return len(self.__str__())
    
    def variables(self):
        vars = []
        if isinstance(self.op1, Expression):
            vars.extend(self.op1.variables())
        elif isinstance(self.op1, str):
            vars.append(self.op1)
        if isinstance(self.op2, Expression):
            vars.extend(self.op2.variables())
        elif isinstance(self.op2, str):
            vars.append(self.op2)
        vars = list(set(vars))
        vars.sort()
        return vars
    
    def solve(self, vars):
        self._op1 = self.op1
        if isinstance(self.op1, Expression):
            self._op1 = self.op1.solve(vars)
        elif self.op1 in vars:
            self._op1 = vars[self.op1]
        
        if self.op2 != None:
            self._op2 = self.op2
            if isinstance(self.op2, Expression):
                self._op2 = self.op2.solve(vars)
            elif self.op2 in vars:
                self._op2 = vars[self.op2]

#------------------------------------------------#
# VARIABLE                                       #
#------------------------------------------------#

# class Variable
class Variable(Expression):
    def __init__(self, strSymbol):
        super().__init__("", strSymbol)
    
    def __str__(self):
        if self.op1.lower() == "true":
            return "T"
        elif self.op1.lower() == "false":
            return "F"
        return self.op1
    
    def variables(self):
        try:
            numeric = float(self.op1)
            return []
        except:
            lowerOp = self.op1.lower()
            if lowerOp == "true" or lowerOp == "false":
                return []
            
            return [self.op1]
    
    def solve(self, vars):
        if self.op1 in vars:
            return vars[self.op1]
        try:
            numeric = float(self.op1)
            return numeric
        except:
            if self.op1.lower() == "true":
                return True 
            elif self.op1.lower() == "false":
                return False
            
            return self.op1

#------------------------------------------------#
# DESCRIPTIVE OPERATIONS                         #
#------------------------------------------------#

# class THEREFORE
class THEREFORE(Expression):
    def __init__(self, op):
        super().__init__("∴", op)

# class BECAUSE
class BECAUSE(Expression):
    def __init__(self, op):
        super().__init__("∵", op)

# class PARENTHESES
class PARENTHESES(Expression):
    def __init__(self, op):
        super().__init__("()", op)
    
    def __str__(self):
        return "(%s)" % self.op1
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1

#------------------------------------------------#
# LOGICAL OPERATIONS                             #
#------------------------------------------------#

# class AND
class AND(Expression):
    def __init__(self, op1, op2):
        super().__init__("∧", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 and self._op2

# class OR
class OR(Expression):
    def __init__(self, op1, op2):
        super().__init__("∨", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 or self._op2

# class NOT
class NOT(Expression):
    def __init__(self, op):
        super().__init__("¬", op)
    
    def solve(self, vars):
        super().solve(vars)
        return not self._op1

# class LEFT_IMPLIES
class LEFT_IMPLIES(Expression):
    def __init__(self, op1, op2):
        super().__init__("←", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return (not self._op2) or self._op1

# class IMPLIES
class IMPLIES(Expression):
    def __init__(self, op1, op2):
        super().__init__("→", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return (not self._op1) or self._op2

# class IFF
class IFF(Expression):
    def __init__(self, op1, op2):
        super().__init__("↔", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return ((not self._op1) or self._op2) and ((not self._op2) or self._op1)

#------------------------------------------------#
# ARITHMETIC OPERATIONS                          #
#------------------------------------------------#

# class EQUAL
class EQUAL(Expression):
    def __init__(self, op1, op2):
        super().__init__("=", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 == self._op2

# class UNEQUAL
class UNEQUAL(Expression):
    def __init__(self, op1, op2):
        super().__init__("≠", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 != self._op2

# class LESS
class LESS(Expression):
    def __init__(self, op1, op2):
        super().__init__("<", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 < self._op2

# class GREATER
class GREATER(Expression):
    def __init__(self, op1, op2):
        super().__init__(">", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 > self._op2

# class LESS_EQUAL
class LESS_EQUAL(Expression):
    def __init__(self, op1, op2):
        super().__init__("≤", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 <= self._op2

# class GREATER_EQUAL
class GREATER_EQUAL(Expression):
    def __init__(self, op1, op2):
        super().__init__("≥", op1, op2)
    
    def solve(self, vars):
        super().solve(vars)
        return self._op1 >= self._op2