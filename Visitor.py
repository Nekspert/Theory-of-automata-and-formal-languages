from abc import ABC, abstractmethod
from SyntaxTree import Node, PNode, ONode, KNode, KNode1, KNode2, CNode, CNode1, CNode2


class IVisitor(ABC):
    @abstractmethod
    def visit(self, node: Node):
        ...


class PrintVisitor(IVisitor):
    def __init__(self):
        self.result = ""

    def visit(self, node: Node):
        self.result += f"{node.name}\n"

        match node:
            case PNode():
                node.O.accept(self)
                node.K.accept(self)
            case KNode1():
                node.O.accept(self)
                node.K.accept(self)
            case KNode2():
                pass
            case ONode():
                node.C.accept(self)
            case CNode1():
                pass
            case CNode2():
                node.O.accept(self)

    def get_result(self):
        return self.result

