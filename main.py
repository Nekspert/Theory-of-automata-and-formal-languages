import tkinter as tk
from tkinter import ttk, scrolledtext
from LexicalAnalyzer import LexicalAnalyzer, LexAnException
from Transliterator import Transliterator
from SyntaxAnalyzer import SyntaxAnalyzer, SynAnException


class LexerApp:
    def __init__(self, root):
        self.root = root
        root.title('Лабораторная работа № 3 - Построение синтаксического дерева')

        root.geometry("1024x360")
        root.resizable(True, True)
        root.minsize(800, 600)

        # Вместо обычного root.pack используем панель
        self.main_pane = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Левая панель (ввод)
        self.input_frame = ttk.LabelFrame(self.main_pane, text='Исходный код')
        self.input_text = scrolledtext.ScrolledText(self.input_frame, width=40, height=20)
        self.input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.main_pane.add(self.input_frame, weight=1)

        # Кнопки
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(padx=10, pady=5)

        self.analyze_btn = ttk.Button(self.button_frame, text='Анализировать', command=self.analyze)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)

        # Область сообщений
        self.messages_frame = ttk.LabelFrame(root, text='Результаты')
        self.messages_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.messages = scrolledtext.ScrolledText(self.messages_frame, height=8, state='disabled')
        self.messages.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Правая панель (дерево)
        self.tree_frame = ttk.LabelFrame(self.main_pane, text='Синтаксическое дерево')
        self.tree_output = scrolledtext.ScrolledText(self.tree_frame, width=40, height=20, state='disabled')
        self.tree_output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.main_pane.add(self.tree_frame, weight=1)

    def add_message(self, text):
        self.messages.configure(state='normal')
        self.messages.insert(tk.END, text)
        self.messages.configure(state='disabled')
        self.messages.see(tk.END)

    def analyze(self):
        self.messages.configure(state='normal')
        self.messages.delete('1.0', tk.END)

        # Очистим перед выводом
        self.tree_output.configure(state='normal')
        self.tree_output.delete('1.0', tk.END)

        input_text = self.input_text.get('1.0', tk.END).strip()
        if not input_text:
            self.messages.insert(tk.END, "Ошибка: Входной текст пуст!\n")
            self.messages.configure(state='disabled')
            return

        try:
            transliterator = Transliterator(input_text.splitlines())
            lexer = LexicalAnalyzer(transliterator)
            syntax_analyzer = SyntaxAnalyzer(lexer)

            root_node = syntax_analyzer.ParseText()

            # Создание и запуск Visitor
            from Visitor import PrintVisitor
            visitor = PrintVisitor()
            root_node.accept(visitor)

            result = visitor.get_result()

            # Выводим в окно синтаксического дерева
            self.tree_output.insert(tk.END, result)
            self.tree_output.configure(state='disabled')

            self.add_message("Ошибок не обнаружено.\n")
        except LexAnException as e:
            error_msg = f"Лексическая ошибка: {e} (Строка {e.LineIndex + 1}, позиция {e.SymIndex + 1})\n"
            self.add_message(error_msg)
            self.highlight_lex_error(e.LineIndex, e.SymIndex)

        except SynAnException as e:
            error_msg = f"Синтаксическая ошибка: {e} (Строка {e.LineIndex + 1}, позиция {e.SymIndex + 1})\n"
            self.add_message(error_msg)
            self.highlight_syn_error(e.LineIndex, e.SymIndex, lexer)

        except Exception as e:
            self.add_message(f"Критическая ошибка: {str(e)}\n")

        finally:
            self.messages.configure(state='disabled')
            self.messages.see(tk.END)

    def highlight_lex_error(self, line: int, pos: int):
        """Подсветка ошибки в тексте"""
        start = f"{line + 1}.{pos}"
        self.input_text.tag_add('error', start, f"{start}+1c")
        self.input_text.tag_config('error', background='red')
        self.input_text.mark_set(tk.INSERT, start)
        self.input_text.focus()

    def highlight_syn_error(self, line: int, pos: int, lexer: LexicalAnalyzer):
        """Подсветка ошибки в тексте"""
        start = f"{line + 1}.{pos - len(lexer.token.Value) - 1}"
        self.input_text.tag_add('error', start, f"{start}+1c")
        self.input_text.tag_config('error', background='red')
        self.input_text.mark_set(tk.INSERT, start)
        self.input_text.focus()


if __name__ == '__main__':
    root = tk.Tk()
    app = LexerApp(root)
    root.mainloop()
