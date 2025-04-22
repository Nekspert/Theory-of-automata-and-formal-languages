from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def accept(self, v: 'IVisitor') -> None:
        ...


class PNode(Node):
    def __init__(self):
        super().__init__('P')

    O: 'ONode'
    K: 'KNode'

    def accept(self, v: 'IVisitor'):
        v.visitPNode(self)


class ONode(Node):
    def __init__(self):
        super().__init__('O')

    second_word: 'ReservedNode'
    equal: 'ReservedNode'
    C: 'CNode'

    def accept(self, v: 'IVisitor'):
        v.visitONode(self)


class KNode(Node, ABC):
    def __init__(self):
        super().__init__('K')


class KNode1(KNode):
    comma: 'ReservedNode'
    O: ONode
    K: KNode

    def accept(self, v: 'IVisitor'):
        v.visitKNode1(self)


class KNode2(KNode):
    def accept(self, v: 'IVisitor'):
        v.visitKNode2(self)


class CNode(Node, ABC):
    def __init__(self):
        super().__init__('C')


class CNode1(CNode):
    first_word1: 'ReservedNode'
    first_word2: 'ReservedNode'

    def accept(self, v: 'IVisitor'):
        v.visitCNode1(self)


class CNode2(CNode):
    LeftParen: 'ReservedNode'
    O: ONode
    RightParen: 'ReservedNode'

    def accept(self, v: 'IVisitor'):
        v.visitCNode2(self)


class ReservedNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

    def accept(self, v: 'IVisitor'):
        v.visitReservedNode(self)
