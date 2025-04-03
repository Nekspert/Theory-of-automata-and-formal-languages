from enum import Enum, auto

from LexicalAnalyzer import LexicalAnalyzer, TokenKind


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

    def P(self):
        """II → O K"""
        self.O()
        self.K()

    def K(self):
        """K → , O K | ε"""
        if self.lexer.token.Type == TokenKind.Comma:
            self.O()
            self.K()
        elif self.lexer.token.Type == TokenKind.EndOfText:
            pass
        else:
            raise self.__SyntaxError('Ожидались либо запятая, либо конец текста.')

    def O(self):
        """O → <2> = <1> <1> | <2> = (O)"""
        if self.lexer.token.Type == TokenKind.Identifier:
            self.lexer.RecognizeNextToken()

            if self.lexer.token.Type == TokenKind.Equal:
                self.lexer.RecognizeNextToken()

                if self.lexer.token.Type == TokenKind.Number:
                    self.lexer.RecognizeNextToken()

                    if self.lexer.token.Type == TokenKind.Number:
                        self.lexer.RecognizeNextToken()
                        return
                    raise self.__SyntaxError('Ожидались цифры "01".')

                elif self.lexer.token.Type == TokenKind.LeftParen:
                    self.lexer.RecognizeNextToken()
                    self.O()

                    if self.lexer.token.Type == TokenKind.RightParen:
                        self.lexer.RecognizeNextToken()
                        return
                    raise self.__SyntaxError('Ожидалась закрывающая правая скобка.')

                else:
                    raise self.__SyntaxError('Ожидались либо цифры "01", либо открывающая левая скобка.')
            else:
                raise self.__SyntaxError('Ожидался символ "=".')
        else:
            raise self.__SyntaxError('Ожидались буквы вида: "abcd" (токен букв).')

    def ParseText(self):
        self.P()
        if self.lexer.token.Type != TokenKind.EndOfText:
            self.__SyntaxError('После выражения идет еще какой-то текст.')
