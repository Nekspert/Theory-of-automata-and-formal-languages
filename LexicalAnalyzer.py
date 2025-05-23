from enum import Enum, auto

from Transliterator import Transliterator


class TokenKind(Enum):
    Number = auto()
    Identifier = auto()
    Comma = ','
    Equal = '='
    LeftParen = '('
    RightParen = ')'
    EndOfText = auto()
    Unknown = auto()


class Token:
    def __init__(self):
        self.__value: str = None
        self.__type: TokenKind = None
        self.__lineIndex: int = None
        self.__symStartIndex: int = None

        self.Reset()

    @property
    def Value(self) -> str:
        return self.__value

    @Value.setter
    def Value(self, value: str):
        self.__value = value

    @property
    def Type(self) -> TokenKind:
        return self.__type

    @Type.setter
    def Type(self, value: TokenKind):
        self.__type = value

    @property
    def LineIndex(self) -> int:
        return self.__lineIndex

    @LineIndex.setter
    def LineIndex(self, value: int):
        self.__lineIndex = value

    @property
    def SymStartIndex(self) -> int:
        return self.__symStartIndex

    @SymStartIndex.setter
    def SymStartIndex(self, value: int):
        self.__symStartIndex = value

    def Reset(self):
        self.Value = ''
        self.Type = TokenKind.Unknown
        self.LineIndex = -1
        self.SymStartIndex = -1


class LexAnException(Exception):
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


class LexicalAnalyzer:
    class FirstWordEnum(Enum):
        A = auto()
        B = auto()
        C = auto()
        D = auto()
        E = auto()
        F_Fin = auto()
        G = auto()
        H = auto()
        Quit = auto()

    class SkipCommentEnum(Enum):
        A = auto()
        B = auto()
        Quit = auto()

    class SecondWordEnum(Enum):
        A = 0
        A_Fin = 1
        B_Fin = 2
        Quit = auto()

    _SecondWordMarksTable: tuple[tuple[tuple[SecondWordEnum], bool]] = (
        ({'a': SecondWordEnum.A_Fin, 'b': SecondWordEnum.B_Fin, 'c': SecondWordEnum.A_Fin, 'd': SecondWordEnum.A_Fin},
         False),
        ({'a': SecondWordEnum.A_Fin, 'b': SecondWordEnum.B_Fin, 'c': SecondWordEnum.A_Fin, 'd': SecondWordEnum.A_Fin},
         True),
        ({'a': SecondWordEnum.A_Fin, 'b': SecondWordEnum.B_Fin, 'c': SecondWordEnum.A_Fin, 'd': SecondWordEnum.A},
         True),
    )

    def __init__(self, transliterator: Transliterator):
        self.__token: Token | None = None
        self._transliterator = transliterator

        self._transliterator.ReadNextSymbol()

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value: Token):
        self.__token = value

    def __LexicalError(self, msg: str):
        raise LexAnException(msg, self._transliterator.curLineIndex, self._transliterator.curSymIndex)

    def __RecognizeSecondWord(self):
        state = self.SecondWordEnum.A
        while state != self.SecondWordEnum.Quit:
            if self._transliterator.curSymKind == self._transliterator.SymbolKind.Letter:
                self.token.Value += self._transliterator.curSym
                state = self._SecondWordMarksTable[state.value][0][self._transliterator.curSym]
                self._transliterator.ReadNextSymbol()
            else:
                if self._SecondWordMarksTable[state.value][1]:
                    self.token.Type = TokenKind.Identifier
                    state = self.SecondWordEnum.Quit
                else:
                    if self.token.Value[-2] == 'b' and self.token.Value[-1] == 'd':
                        self.__LexicalError('Недопустимый конец слова')
                    else:
                        self.__LexicalError('Недопустимый символ')

    def __RecognizeFirstWord(self):
        state = self.FirstWordEnum.A
        while True:
            match state:
                case self.FirstWordEnum.A:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '0':
                            state = self.FirstWordEnum.C
                        else:
                            state = self.FirstWordEnum.B
                        self.token.Value += self._transliterator.curSym
                        self._transliterator.ReadNextSymbol()
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.B:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '1':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.D
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.C:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '0':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.E
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.D:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '1':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.A
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.E:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '0':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.F_Fin
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.F_Fin:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '0':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.G
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        state = self.FirstWordEnum.Quit
                case self.FirstWordEnum.G:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '0':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.H
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.H:
                    if self._transliterator.curSymKind == self._transliterator.SymbolKind.Digit:
                        if self._transliterator.curSym == '1':
                            self.token.Value += self._transliterator.curSym
                            self._transliterator.ReadNextSymbol()
                            state = self.FirstWordEnum.F_Fin
                        else:
                            self.__LexicalError('Недопустимая цифра')
                    else:
                        self.__LexicalError('Недопустимый символ')
                case self.FirstWordEnum.Quit:
                    self.token.Type = TokenKind.Number
                    return

    def __SkipComment(self):
        state = self.SkipCommentEnum.A
        while True:
            match state:
                case self.SkipCommentEnum.A:
                    if self._transliterator.curSym == self._transliterator._commentSymbol1:
                        self._transliterator.ReadNextSymbol()
                        state = self.SkipCommentEnum.B
                    else:
                        self.__LexicalError(f'Ожидалось {self._transliterator._commentSymbol1}')
                case self.SkipCommentEnum.B:
                    if self._transliterator.curSymKind in (
                            self._transliterator.SymbolKind.EndOfLine, self._transliterator.SymbolKind.EndOfText):
                        self._transliterator.ReadNextSymbol()
                        state = self.SkipCommentEnum.Quit
                    else:
                        self._transliterator.ReadNextSymbol()
                case self.SkipCommentEnum.Quit:
                    return

    def __RecognizeReservedSymbol(self):
        match self._transliterator.curSym:
            case ',':
                self.token.Value += self._transliterator.curSym
                self.token.Type = TokenKind.Comma
                self._transliterator.ReadNextSymbol()
            case '=':
                self.token.Value += self._transliterator.curSym
                self.token.Type = TokenKind.Equal
                self._transliterator.ReadNextSymbol()
            case '(':
                self.token.Value += self._transliterator.curSym
                self.token.Type = TokenKind.LeftParen
                self._transliterator.ReadNextSymbol()
            case ')':
                self.token.Value += self._transliterator.curSym
                self.token.Type = TokenKind.RightParen
                self._transliterator.ReadNextSymbol()
            case _:
                self.__LexicalError(f'Неизвестный зарезервированный символ: "{self._transliterator.curSym}"')

    def RecognizeNextToken(self):
        while self._transliterator.curSymKind in (self._transliterator.SymbolKind.Space,
                                                  self._transliterator.SymbolKind.EndOfLine,
                                                  self._transliterator._commentSymbol1):
            if self._transliterator.curSym == self._transliterator._commentSymbol1:
                self.__SkipComment()
            else:
                self._transliterator.ReadNextSymbol()

        self.token = Token()
        self.token.LineIndex = self._transliterator.curLineIndex
        self.token.SymStartIndex = self._transliterator.curSymIndex

        match self._transliterator.curSymKind:
            case self._transliterator.SymbolKind.Digit:
                self.__RecognizeFirstWord()
            case self._transliterator.SymbolKind.Letter:
                self.__RecognizeSecondWord()
            case self._transliterator.SymbolKind.Reserved:
                self.__RecognizeReservedSymbol()
            case self._transliterator.SymbolKind.EndOfText:
                self.token.Type = TokenKind.EndOfText
            case _:
                self.__LexicalError('Недопустимый символ')
