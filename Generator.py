from SyntaxAnalyzer import TokenKind
from SyntaxTree import PNode, ONode, KNode1, KNode2, CNode1, CNode2, ReservedNode, Node
from Visitor import IVisitor


class GeneratorVisitor(IVisitor):
    def __init__(self):
        self.stack: list[Node] = []
        self.__outputText: list[str] = []

    @property
    def outputText(self) -> list[str]:
        return self.__outputText

    def saveItem(self, cur_node: ReservedNode):
        depth = sum(1 for n in self.stack if isinstance(n, CNode2))
        if cur_node.name in (TokenKind.LeftParen.value, TokenKind.RightParen.value):
            indent = max(depth - 1, 0) * 10
        else:
            indent = depth * 10
        if cur_node.name in (TokenKind.Comma.value, TokenKind.Equal.value):
            indent += 10

        self.__outputText.append(' ' * indent + cur_node.name)

    def visitReservedNode(self, node: ReservedNode) -> None:
        self.saveItem(node)

    def visitPNode(self, node: PNode) -> None:
        self.stack.append(node)

        node.O.accept(self)
        node.K.accept(self)

        self.stack.pop()

    def visitONode(self, node: ONode) -> None:
        self.stack.append(node)

        node.second_word.accept(self)
        node.equal.accept(self)
        node.C.accept(self)

        self.stack.pop()

    def visitCNode1(self, node: CNode1) -> None:
        self.stack.append(node)

        node.first_word1.accept(self)
        node.first_word2.accept(self)

        self.stack.pop()

    def visitCNode2(self, node: CNode2) -> None:
        self.stack.append(node)

        node.LeftParen.accept(self)
        node.O.accept(self)
        node.RightParen.accept(self)

        self.stack.pop()

    def visitKNode1(self, node: KNode1) -> None:
        self.stack.append(node)

        node.comma.accept(self)
        node.O.accept(self)
        node.K.accept(self)

        self.stack.pop()

    def visitKNode2(self, node: KNode2) -> None:
        self.stack.append(node)
        self.stack.pop()
