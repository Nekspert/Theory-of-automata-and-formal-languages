from enum import Enum, auto

from LexicalAnalyzer import LexicalAnalyzer, TokenKind
from SyntaxTree import PNode, ONode, KNode1, KNode2, CNode1, CNode2, KNode, CNode


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

    def P(self) -> PNode:
        """II → O K"""
        p = PNode()
        p.O = self.O()
        p.K = self.K()
        return p

    def K(self) -> KNode:
        """K → , O K | ε"""
        if self.lexer.token.Type == TokenKind.Comma:
            self.lexer.RecognizeNextToken()
            k = KNode1()
            k.O = self.O()
            k.K = self.K()
            return k
        elif self.lexer.token.Type == TokenKind.EndOfText:
            return KNode2()
        else:
            raise self.__SyntaxError('Ожидались либо запятая, либо конец текста.')

    def O(self) -> ONode:
        """O → <2> = C"""
        o = ONode()
        if self.lexer.token.Type == TokenKind.Identifier:
            o.second_word = self.lexer.token
            self.lexer.RecognizeNextToken()

            if self.lexer.token.Type == TokenKind.Equal:
                o.equal = self.lexer.token
                self.lexer.RecognizeNextToken()
                o.C = self.C()
                return o
            else:
                raise self.__SyntaxError('Ожидался символ "=".')
        else:
            raise self.__SyntaxError('Ожидались буквы вида: "abcd".')

    def C(self) -> CNode:
        """C-> <1> <1> | (O)"""
        if self.lexer.token.Type == TokenKind.Number:
            c = CNode1()
            c.first_word = self.lexer.token
            self.lexer.RecognizeNextToken()

            if self.lexer.token.Type == TokenKind.Number:
                c.second_word = self.lexer.token
                self.lexer.RecognizeNextToken()
                return c
            raise self.__SyntaxError('Ожидались две цифры "01".')

        elif self.lexer.token.Type == TokenKind.LeftParen:
            c = CNode2()
            c.LeftParen = self.lexer.token
            self.lexer.RecognizeNextToken()

            c.O = self.O()

            if self.lexer.token.Type == TokenKind.RightParen:
                c.RightParen = self.lexer.token
                self.lexer.RecognizeNextToken()
                return c
            raise self.__SyntaxError('Ожидалась закрывающая правая скобка.')
        else:
            raise self.__SyntaxError('Ожидались либо цифры, либо открывающая скобка.')

    def ParseText(self) -> PNode:
        root = self.P()
        if self.lexer.token.Type != TokenKind.EndOfText:
            self.__SyntaxError('После выражения идет еще какой-то текст.')
        return root
