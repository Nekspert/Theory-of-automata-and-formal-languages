import tkinter as tk
from tkinter import ttk, scrolledtext  # Добавьте этот импорт
from LexicalAnalyzer import LexicalAnalyzer, LexAnException
from Transliterator import Transliterator
from SyntaxAnalyzer import SyntaxAnalyzer, SynAnException


class LexerApp:
    def __init__(self, root):
        self.root = root
        root.title('Лабораторная работа № 2 - Синтаксический анализатор')

        root.geometry("1024x360")
        root.resizable(True, True)
        root.minsize(800, 600)

        # Ввод текста
        self.input_frame = ttk.LabelFrame(root, text='Исходный код')
        self.input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_text = scrolledtext.ScrolledText(self.input_frame, width=80, height=20)
        self.input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

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

    def analyze(self):
        self.messages.configure(state='normal')
        self.messages.delete('1.0', tk.END)

        input_text = self.input_text.get('1.0', tk.END).strip()
        if not input_text:
            self.messages.insert(tk.END, "Ошибка: Входной текст пуст!\n")
            self.messages.configure(state='disabled')
            return

        try:
            transliterator = Transliterator(input_text.splitlines())
            lexer = LexicalAnalyzer(transliterator)
            syntax_analyzer = SyntaxAnalyzer(lexer)

            syntax_analyzer.ParseText()

            self.messages.insert(tk.END, "Ошибок не обнаружено.\n")

        except LexAnException as e:
            error_msg = f"Лексическая ошибка: {e} (Строка {e.LineIndex + 1}, позиция {e.SymIndex + 1})\n"
            self.messages.insert(tk.END, error_msg)
            self.highlight_lex_error(e.LineIndex, e.SymIndex)

        except SynAnException as e:
            error_msg = f"Синтаксическая ошибка: {e} (Строка {e.LineIndex + 1}, позиция {e.SymIndex + 1})\n"
            self.messages.insert(tk.END, error_msg)
            self.highlight_syn_error(e.LineIndex, e.SymIndex, lexer)

        except Exception as e:
            self.messages.insert(tk.END, f"Критическая ошибка: {str(e)}\n")

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
