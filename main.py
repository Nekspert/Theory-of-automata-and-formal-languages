import traceback

from PyQt6 import QtWidgets
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QStyleFactory
from PyQt6.QtWidgets import QTreeWidget

from Generator import GeneratorVisitor
from LexicalAnalyzer import LexAnException, LexicalAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer, SynAnException
from SyntaxTree import *
from Transliterator import Transliterator
from Visitor import PrintVisitor


class FormMain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Лабораторная работа №5 - Разработка Генератора")
        self.setGeometry(100, 100, 1000, 800)

    def init_ui(self):
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.topLayout = QtWidgets.QVBoxLayout()
        self.middleLayout = QtWidgets.QHBoxLayout()
        self.inputTextLayout = QtWidgets.QVBoxLayout()
        self.syntaxTreeLayout = QtWidgets.QVBoxLayout()
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.info_label = QtWidgets.QLabel(
            f"Слова первого типа: (111)*000(001)*\n"
            f"Слова второго типа: (a|b|c|d)+ не должно заканчиваться символами bd\n"
            f"Комментарий: # однострочный комментарий (как в PHP)\n\n"
            f"КС-грамматика:\n"
            f"П → ОК\n"
            f"К → ,ОК | ε\n"
            f"О → <2> = С\n"
            f"С → <1> <1> | (О)\n")
        self.input_text_label = QtWidgets.QLabel("Входной текст:")
        self.input_text = QtWidgets.QPlainTextEdit()
        self.analyze_button = QtWidgets.QPushButton("Анализировать текст")
        self.messages_label = QtWidgets.QLabel("Сообщения:")
        self.messages = QtWidgets.QPlainTextEdit()
        self.messages.setReadOnly(True)
        self.messages.setMaximumHeight(100)
        self.messages.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.ast_tree_label = QtWidgets.QLabel("Синтаксическое дерево:")
        self.ast_tree = QTreeWidget()
        self.generator_label = QtWidgets.QLabel("Результат Генератора:")
        self.generator_output = QtWidgets.QPlainTextEdit()
        self.generator_output.setReadOnly(True)

        self.ast_tree.setHeaderHidden(True)
        self.ast_tree.setRootIsDecorated(True)
        self.ast_tree.setItemsExpandable(True)
        self.ast_tree.setStyle(QStyleFactory.create("windows"))
        self.topLayout.addWidget(self.info_label)
        self.inputTextLayout.addWidget(self.input_text_label)
        self.inputTextLayout.addWidget(self.input_text)
        self.middleLayout.addLayout(self.inputTextLayout)

        self.syntaxTreeLayout.addWidget(self.ast_tree_label)
        self.syntaxTreeLayout.addWidget(self.ast_tree)
        self.syntaxTreeLayout.addWidget(self.generator_label)
        self.syntaxTreeLayout.addWidget(self.generator_output)

        self.middleLayout.addLayout(self.syntaxTreeLayout)
        self.bottomLayout.addWidget(self.analyze_button)
        self.bottomLayout.addWidget(self.messages_label)
        self.bottomLayout.addWidget(self.messages)
        self.mainLayout.addLayout(self.topLayout, stretch=0)
        self.mainLayout.addLayout(self.middleLayout, stretch=5)
        self.mainLayout.addLayout(self.bottomLayout, stretch=1)
        self.setLayout(self.mainLayout)
        self.analyze_button.clicked.connect(self.button_analyze_click)

    def button_analyze_click(self):
        self.messages.clear()
        self.ast_tree.clear()
        self.generator_output.clear()

        try:
            transliterator = Transliterator(self.input_text.toPlainText().splitlines())
            lexer = LexicalAnalyzer(transliterator)
            syntax_analyzer = SyntaxAnalyzer(lexer)

            root_node: PNode = syntax_analyzer.ParseText()
            pv = PrintVisitor(self.ast_tree)
            pv.visitPNode(root_node)
            self.ast_tree.expandAll()

            gv = GeneratorVisitor()
            gv.visitPNode(root_node)
            for line in gv.outputText:
                self.generator_output.appendPlainText(line)

            self.messages.appendPlainText("Текст правильный")
        except LexAnException as e:
            self.messages.appendPlainText(
                f"Лексическая ошибка: {e} (Строка {e.LineIndex + 1}, позиция {e.SymIndex + 1})\n")
            self.locate_cursor_at_error_position(e.LineIndex, e.SymIndex)


        except SynAnException as e:
            self.messages.appendPlainText(
                f"Синтаксическая ошибка: {e} (Строка {e.LineIndex + 1}, позиция {e.SymIndex + 1})\n")
            self.locate_cursor_at_error_position(e.LineIndex, e.SymIndex, lexer)

        except Exception:
            print(traceback.format_exc())

    def locate_cursor_at_error_position(self, line_index, sym_index, lexer=None):
        try:
            cursor = self.input_text.textCursor()
            pos = sum(len(line) + 1 for line in self.input_text.toPlainText().splitlines()[:line_index]) + sym_index

            if lexer:
                pos -= len(lexer.token.Value)

            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)

            self.input_text.setTextCursor(cursor)
            self.input_text.setFocus()

        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = FormMain()
    window.show()
    app.exec()
