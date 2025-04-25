from enum import Enum, auto

from LexicalAnalyzer import LexicalAnalyzer, TokenKind
from SyntaxTree import PNode, ONode, KNode1, KNode2, CNode1, CNode2, KNode, CNode, ReservedNode


class SynAnException(Exception):
    def __init__(self, message: str, lineIndex: int, symIndex: int):
        super().__init__(message)
        self.__lineIndex = lineIndex
        self.__symIndex = symIndex

    @property
    def LineIndex(self) -> int:
        return self.__lineIndex

    @property
    def SymIndex(self) -> int:
        return self.__symIndex


class SyntaxAnalyzer:
    def __init__(self, lexer: LexicalAnalyzer):
        self.lexer = lexer
        self.current_token = self.lexer.RecognizeNextToken()

    def __SyntaxError(self, msg: str):
        raise SynAnException(msg, self.lexer._transliterator.curLineIndex, self.lexer._transliterator.curSymIndex)

    def P(self, different_identifiers: set) -> PNode:
        """II → O K"""
        p = PNode()
        p.O = self.O(different_identifiers)
        p.K = self.K(different_identifiers)
        return p

    def K(self, different_identifiers: set) -> KNode:
        """K → , O K | ε"""
        k = KNode1()
        if self.lexer.token.Type == TokenKind.Comma:
            k.comma = ReservedNode(self.lexer.token.Value)
            self.lexer.RecognizeNextToken()
            k.O = self.O(different_identifiers)
            k.K = self.K(different_identifiers)
            return k
        elif self.lexer.token.Type == TokenKind.EndOfText:
            return KNode2()
        else:
            raise self.__SyntaxError('Ожидались либо запятая, либо конец текста.')

    def O(self, different_identifiers: set) -> ONode:
        """O → <2> = C"""
        o = ONode()
        if self.lexer.token.Type == TokenKind.Identifier:
            if self.lexer.token.Value in different_identifiers:
                raise self.__SyntaxError('Все идентификаторы должны быть разными.')
            else:
                different_identifiers.add(self.lexer.token.Value)

            o.second_word = ReservedNode(self.lexer.token.Value)
            self.lexer.RecognizeNextToken()

            if self.lexer.token.Type == TokenKind.Equal:
                o.equal = ReservedNode(self.lexer.token.Value)
                self.lexer.RecognizeNextToken()
                o.C = self.C(different_identifiers)
                return o
            else:
                raise self.__SyntaxError('Ожидался символ "=".')
        else:
            raise self.__SyntaxError('Ожидались буквы вида: "abcd".')

    def C(self, different_identifiers: set) -> CNode:
        """C-> <1> <1> | (O)"""
        if self.lexer.token.Type == TokenKind.Number:
            c = CNode1()
            c.first_word1 = ReservedNode(self.lexer.token.Value)
            self.lexer.RecognizeNextToken()

            if self.lexer.token.Type == TokenKind.Number:
                c.first_word2 = ReservedNode(self.lexer.token.Value)
                self.lexer.RecognizeNextToken()
                return c
            raise self.__SyntaxError('Ожидались две цифры "01".')

        elif self.lexer.token.Type == TokenKind.LeftParen:
            c = CNode2()
            c.LeftParen = ReservedNode(self.lexer.token.Value)
            self.lexer.RecognizeNextToken()

            c.O = self.O(different_identifiers)

            if self.lexer.token.Type == TokenKind.RightParen:
                c.RightParen = ReservedNode(self.lexer.token.Value)
                self.lexer.RecognizeNextToken()
                return c
            raise self.__SyntaxError('Ожидалась закрывающая правая скобка.')
        else:
            raise self.__SyntaxError('Ожидались либо цифры, либо открывающая скобка.')

    def ParseText(self) -> PNode:
        different_identifiers = set()
        root = self.P(different_identifiers)
        if self.lexer.token.Type != TokenKind.EndOfText:
            self.__SyntaxError('После выражения идет еще какой-то текст.')
        return root
