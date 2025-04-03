import tkinter as tk
from tkinter import ttk, scrolledtext
from Transliterator import Transliterator
from LexicalAnalyzer import LexicalAnalyzer, LexAnException, TokenKind


class LexerApp:
    def __init__(self, root):
        self.root = root
        root.title('Лабораторная работа № 1 - Разработка лексического анализатора')

        self.input_frame = ttk.LabelFrame(root, text='Input Text')
        self.input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_text = scrolledtext.ScrolledText(self.input_frame, width=60, height=15)
        self.input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(padx=10, pady=5)

        self.analyze_btn = ttk.Button(self.button_frame, text='Analyze', command=self.analyze)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)

        self.results_frame = ttk.LabelFrame(root, text='Recognized Tokens')
        self.results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.results_frame,
                                 columns=('№', 'Token', 'Type of Token', 'Line Index', 'Symbol index'),
                                 show='headings')
        self.tree.heading('№', text='№')
        self.tree.heading('Token', text='Token')
        self.tree.heading('Type of Token', text='Type of Token')
        self.tree.heading('Line Index', text='Line Index')
        self.tree.heading('Symbol index', text='Symbol index')
        self.tree.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Messages Area
        self.messages_frame = ttk.LabelFrame(root, text='Messages')
        self.messages_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.messages = scrolledtext.ScrolledText(self.messages_frame, height=5, state='disabled')
        self.messages.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def analyze(self):
        self.tree.delete(*self.tree.get_children())
        self.messages.configure(state='normal')
        self.messages.delete('1.0', tk.END)
        self.messages.configure(state='disabled')

        input_text = self.input_text.get('1.0', tk.END)
        input_lines = input_text.splitlines()

        transliterator = Transliterator(input_lines)
        lex_analyzer = LexicalAnalyzer(transliterator)

        token_count = 0

        try:
            while True:
                lex_analyzer.RecognizeNextToken()
                token = lex_analyzer.token

                token_count += 1
                self.tree.insert('', tk.END, values=(
                    token_count,
                    token.Value,
                    token.Type.name,
                    token.LineIndex + 1,
                    token.SymStartIndex + 1
                ))

                if token.Type == TokenKind.EndOfText:
                    break

            self.show_message('Analysis completed successfully. No errors found.')

        except LexAnException as ex:
            self.show_message(f'Error (Line {ex.LineIndex + 1}, Position {ex.SymIndex + 1}): {ex}')
            self.highlight_error(ex.LineIndex, ex.SymIndex)

    def show_message(self, message):
        self.messages.configure(state='normal')
        self.messages.insert(tk.END, message + '\n')
        self.messages.configure(state='disabled')
        self.messages.see(tk.END)

    def highlight_error(self, line_index, sym_index):
        pos = f'{line_index + 1}.{sym_index}'
        self.input_text.mark_set(tk.INSERT, pos)
        self.input_text.tag_add(tk.SEL, pos, f'{pos}+1c')
        self.input_text.focus_set()


if __name__ == '__main__':
    root = tk.Tk()
    app = LexerApp(root)
    root.mainloop()
