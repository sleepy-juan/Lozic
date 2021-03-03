#
#   Parser.py
#  
from Expression import *

# class RawExpression
class RawExpression:
    @staticmethod
    def raw(rawexp):
        return RawExpression(rawexp, {}, 0).expression()

    def __init__(self, raw, innerExps, depth):
        self.raw = raw.strip()
        self.innerExps = innerExps
        self.depth = depth
        
        self.NAMING_RULE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"
    
    def __str__(self):
        return self.raw

    def _binaryOp(self, OP, symbol, raw, exps, depth):
        first, second = raw.split(symbol)
        firstExp = RawExpression(first, exps, depth+1).expression()
        secondExp = RawExpression(second, exps, depth+1).expression()
        return OP(firstExp, secondExp)
    
    def expression(self):
        # split parenthesis
        parenthesisCount = 0
        previousParenthesisIdx = -1
        parsedExp = ''
        for idx in range(len(self.raw)):
            if self.raw[idx] == '(':
                parenthesisCount += 1
                if parenthesisCount == 1:
                    previousParenthesisIdx = idx
            elif self.raw[idx] == ')':
                parenthesisCount -= 1
                if parenthesisCount == 0:
                    expID = '__EXP%d_%d__' % (self.depth, idx)
                    parsedExp += expID
                    innerExp = RawExpression(self.raw[previousParenthesisIdx+1:idx], {}, self.depth+1).expression()
                    self.innerExps[expID] = PARENTHESES(innerExp)
            elif parenthesisCount == 0:
                parsedExp += self.raw[idx]
        
        # iff
        iff = parsedExp.find("<->")
        if iff != -1:
            return self._binaryOp(IFF, "<->", parsedExp, self.innerExps, self.depth)

        # implies
        limp = parsedExp.find("<-")
        rimp = parsedExp.find("->")

        if limp != -1 and rimp != -1:
            if limp < rimp:
                return self._binaryOp(LEFT_IMPLIES, "<-", parsedExp, self.innerExps, self.depth)
            else:
                return self._binaryOp(IMPLIES, "->", parsedExp, self.innerExps, self.depth)
        elif limp != -1:
            return self._binaryOp(LEFT_IMPLIES, "<-", parsedExp, self.innerExps, self.depth) 
        elif rimp != -1:
            return self._binaryOp(IMPLIES, "->", parsedExp, self.innerExps, self.depth)
        
        # not
        _parsedExp = ''
        lastlyAdded = 0
        idxNot = parsedExp.find("~")
        if idxNot != -1:
            while idxNot != -1:
                _parsedExp += parsedExp[lastlyAdded:idxNot]

                while parsedExp[idxNot] not in self.NAMING_RULE:
                    idxNot += 1
                beginExp = idxNot
                while idxNot < len(parsedExp) and parsedExp[idxNot] in self.NAMING_RULE:
                    idxNot += 1 
                
                lastlyAdded = idxNot
                expID = "__NOT%d_%d__" % (self.depth, beginExp)
                innerExp = RawExpression(parsedExp[beginExp: idxNot], self.innerExps, self.depth+1).expression()
                self.innerExps[expID] = NOT(innerExp)
                _parsedExp += expID
                idxNot = parsedExp.find("~", idxNot)
            _parsedExp += parsedExp[lastlyAdded:]
            parsedExp = _parsedExp 

        # and, or
        idxAnd = parsedExp.find("&")
        idxOr = parsedExp.find("|")

        if idxAnd != -1 and idxOr != -1:
            if idxAnd < idxOr:
                return self._binaryOp(AND, "&", parsedExp, self.innerExps, self.depth)
            else:
                return self._binaryOp(OR, "|", parsedExp, self.innerExps, self.depth)
        elif idxAnd != -1:
            return self._binaryOp(AND, "&", parsedExp, self.innerExps, self.depth) 
        elif idxOr != -1:
            return self._binaryOp(OR, "|", parsedExp, self.innerExps, self.depth)
        
        # equal, unequal
        idxEqual = parsedExp.find("=")
        idxUnequal = parsedExp.find("!=")

        if idxEqual != -1 and idxUnequal != -1:
            if idxEqual < idxUnequal:
                return self._binaryOp(EQUAL, "=", parsedExp, self.innerExps, self.depth)
            else:
                return self._binaryOp(UNEQUAL, "!=", parsedExp, self.innerExps, self.depth)
        elif idxEqual != -1:
            return self._binaryOp(EQUAL, "=", parsedExp, self.innerExps, self.depth) 
        elif idxUnequal != -1:
            return self._binaryOp(UNEQUAL, "!=", parsedExp, self.innerExps, self.depth)
        
        # or,
        return Variable(parsedExp)