from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Visitor import IVisitor
    from LexicalAnalyzer import Token


class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def accept(self, v: 'IVisitor'):
        pass


class PNode(Node):
    def __init__(self):
        super().__init__('P')

    O: 'ONode'
    K: 'KNode'

    def accept(self, v: 'IVisitor'):
        v.visit(self)


class ONode(Node):
    def __init__(self):
        super().__init__('O')

    second_word: 'Token'
    equal: 'Token'
    C: 'CNode'

    def accept(self, v: 'IVisitor'):
        v.visit(self)


class KNode(Node, ABC):
    def __init__(self):
        super().__init__('K')


class KNode1(KNode):
    comma: str
    O: ONode
    K: KNode

    def accept(self, v: 'IVisitor'):
        v.visit(self)


class KNode2(KNode):
    def accept(self, v: 'IVisitor'):
        v.visit(self)


class CNode(Node, ABC):
    def __init__(self):
        super().__init__('C')


class CNode1(CNode):
    first_word: 'Token'
    first_word: 'Token'

    def accept(self, v: 'IVisitor'):
        v.visit(self)


class CNode2(CNode):
    LeftParen: 'Token'
    O: ONode
    LeftParen: 'Token'

    def accept(self, v: 'IVisitor'):
        v.visit(self)
