from abc import ABC, abstractmethod

from PyQt6.QtWidgets import QTreeWidgetItem, QTreeWidget

from SyntaxTree import PNode, ONode, KNode, KNode1, KNode2, CNode, CNode1, CNode2, ReservedNode


class IVisitor(ABC):
    @abstractmethod
    def visitPNode(self, node: PNode) -> None:
        ...

    @abstractmethod
    def visitONode(self, node: ONode) -> None:
        ...

    @abstractmethod
    def visitCNode1(self, node: CNode1) -> None:
        ...

    @abstractmethod
    def visitCNode2(self, node: CNode2) -> None:
        ...

    @abstractmethod
    def visitKNode1(self, node: KNode1) -> None:
        ...

    @abstractmethod
    def visitKNode2(self, node: KNode2) -> None:
        ...

    @abstractmethod
    def visitReservedNode(self, node: ReservedNode) -> None:
        ...


class PrintVisitor(IVisitor):
    def __init__(self, tree_widget: QTreeWidget):
        self.stack = []
        self.tree_widget = tree_widget

    def createQTreeWidgetItem(self, name: str) -> QTreeWidgetItem:
        item = QTreeWidgetItem([name])
        if self.stack:
            self.stack[-1].addChild(item)
        else:
            self.tree_widget.addTopLevelItem(item)
        return item

    def visitReservedNode(self, node: ReservedNode):
        self.createQTreeWidgetItem(node.name)

    def visitPNode(self, node: PNode) -> None:
        item = self.createQTreeWidgetItem(node.name)
        self.stack.append(item)
        node.O.accept(self)
        node.K.accept(self)
        self.stack.pop()

    def visitONode(self, node: ONode) -> None:
        item = self.createQTreeWidgetItem(node.name)
        self.stack.append(item)
        node.second_word.accept(self)
        node.equal.accept(self)
        node.C.accept(self)
        self.stack.pop()

    def visitCNode1(self, node: CNode1) -> None:
        item = self.createQTreeWidgetItem(node.name)
        self.stack.append(item)
        node.first_word1.accept(self)
        node.first_word2.accept(self)
        self.stack.pop()

    def visitCNode2(self, node: CNode2) -> None:
        item = self.createQTreeWidgetItem(node.name)
        self.stack.append(item)
        node.LeftParen.accept(self)
        node.O.accept(self)
        node.RightParen.accept(self)
        self.stack.pop()

    def visitKNode1(self, node: KNode1) -> None:
        item = self.createQTreeWidgetItem(node.name)
        self.stack.append(item)
        node.comma.accept(self)
        node.O.accept(self)
        node.K.accept(self)
        self.stack.pop()

    def visitKNode2(self, node: KNode2) -> None:
        _ = self.createQTreeWidgetItem(node.name)
