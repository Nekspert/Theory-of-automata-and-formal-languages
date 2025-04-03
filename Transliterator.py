from enum import Enum, auto


class Transliterator:
    _commentSymbol1 = '#'

    class SymbolKind(Enum):
        Letter = auto()  # Буква
        Digit = auto()  # Цифра
        Space = auto()  # Пробел
        Reserved = auto()  # Зарезервированный
        Other = auto()  # Другой
        EndOfLine = auto()  # Конец строки
        EndOfText = auto()  # Конец текста

    def __init__(self, inputLines: list[str]):
        self.__curLineIndex: int = 0
        self.__curSymIndex: int = -1
        self.__curSym: str = '\0'
        self.__curSymKind: Transliterator.SymbolKind = None
        self.__inputLines: list[str] = inputLines

    @property
    def inputLines(self):
        return self.__inputLines

    @property
    def curLineIndex(self):
        return self.__curLineIndex

    @property
    def curSymIndex(self):
        return self.__curSymIndex

    @curSymIndex.setter
    def curSymIndex(self, value: int):
        self.__curSymIndex = value

    @property
    def curSym(self):
        return self.__curSym

    @curSym.setter
    def curSym(self, value: str):
        self.__curSym = value

    @property
    def curSymKind(self):
        return self.__curSymKind

    @curSymKind.setter
    def curSymKind(self, value: SymbolKind):
        self.__curSymKind = value

    @property
    def ClassifyCurrentSymbol(self):
        return self.__ClassifyCurrentSymbol

    @property
    def ReadNextSymbol(self):
        return self.__ReadNextSymbol

    def __ClassifyCurrentSymbol(self):
        if 'a' <= self.curSym <= 'd':
            self.curSymKind = self.SymbolKind.Letter
        elif '0' <= self.curSym <= '1':
            self.curSymKind = self.SymbolKind.Digit
        else:
            match self.curSym:
                case ' ':
                    self.curSymKind = self.SymbolKind.Space
                case self._commentSymbol1:
                    self.curSymKind = self._commentSymbol1
                case ',':
                    self.curSymKind = self.SymbolKind.Reserved
                case '=':
                    self.curSymKind = self.SymbolKind.Reserved
                case '(':
                    self.curSymKind = self.SymbolKind.Reserved
                case ')':
                    self.curSymKind = self.SymbolKind.Reserved
                case _:
                    self.curSymKind = self.SymbolKind.Other

    def __ReadNextSymbol(self):
        if self.curLineIndex >= len(self.inputLines):
            self.curSym = '\0'
            self.curSymKind = self.SymbolKind.EndOfText
            return

        self.curSymIndex += 1

        if self.curSymIndex >= len(self.inputLines[self.curLineIndex]):
            self.__curLineIndex += 1
            if self.curLineIndex < len(self.inputLines):
                self.__curSymIndex = -1
                self.curSym = '\0'
                self.curSymKind = self.SymbolKind.EndOfLine
            else:
                self.curSym = '\0'
                self.curSymKind = self.SymbolKind.EndOfText
            return

        self.curSym = self.inputLines[self.curLineIndex][self.curSymIndex]

        self.ClassifyCurrentSymbol()
