from math import sqrt
import os
import time
from tkinter import *
from tkinter import messagebox
from typing import Literal, Tuple
import tkinter.ttk as ttk
from threading import Thread

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class V:
    T = TINY = DESC = 0
    M = MEDIUM = PARAGRAPH = 1
    B = BIG = TITLE = 2

    N, Z, Q = 7, 8, 2
    B  = BOLD = True
    NB = NOTBOLD = False
    I  = ITALIC = True
    NI = NOTITALIC = False

    DAS = [N, Q, Z]
def newfont(
        font: Literal[0], 
        size: Literal[0, 1, 2] = 0, 
        bold: Literal[0, 1] = 0, 
        italic: Literal[0, 1] = 0
    ) -> Tuple[str, int, str, str] | Tuple[str, int, str] | Tuple[str, int]:
    _font = ["JetBrains Mono"]
    _size = [8, 16, 20]
    _bold = "bold" if bool(bold) else None
    _italic = "italic" if bool(italic) else None
    return (_font[font], _size[size]) if (
        (_bold is None) and (_italic is None)
    ) else (_font[font], _size[size], _bold) if (
        (_italic is None) and (not _bold is None)
    ) else (_font[font], _size[size], _bold, _italic) if (
        (not _italic is None) and (not _bold is None) 
    ) else (_font[font], _size[size])

class ESG(Tk):
    def __init__(self):
        self.busy_tasks: list[Thread] = []
        self._stop_threads = False

        super().__init__()

        self.appicon = PhotoImage(
            file="appicon.png"
        )
        self.geometry()
        self.title("Equação de segundo grau")
        self.grid(5, 5, 150, 4)
        self.resizable(False, False)

        self.iconphoto(True, self.appicon)

        self.s = IntVar(self, 0)

        self.title_label = ttk.Label(
            self,
            text="Equação de Segundo Grau",
            font=newfont(0, V.BIG, V.BOLD),
            anchor="center",
            padding=(30, 10)
        )
        self.title_label.grid(row=0, column=0, columnspan=4, sticky="NSEW")
        self.caption_raw = "Insira as variáveis"
        self.caption = StringVar(self, self.caption_raw)
        self.subtitle_label = ttk.Label(
            self,
            textvariable=self.caption,
            font=newfont(0, V.MEDIUM, V.BOLD),
            anchor="center",
            padding=(30, 10)
        )
        self.subtitle_label.grid(row=1, column=0, columnspan=4, sticky="NSEW")
        # ax² + bx + c = 0

        # variables
        self.a = IntVar(self, 0)
        self.a.trace_add('write', lambda a, b, c: self.calculate)
        self.b = IntVar(self, 0)
        self.b.trace_add('write', lambda a, b, c: self.calculate)
        self.c = IntVar(self, 0)
        self.c.trace_add('write', lambda a, b, c: self.calculate)
        self.x1 = IntVar(self, 0)
        self.x2 = IntVar(self, 0)
        self.x1.trace_add("write", lambda a, b, c: self.out_x1.set(self.x1.get()/ 1000))
        self.out_x1 = StringVar(self, "0")
        self.x2.trace_add("write", lambda a, b, c: self.out_x2.set(self.x2.get()/ 1000))
        self.out_x2 = StringVar(self, "0")


        self.entry_a = Spinbox(
            self,
            width=3,
            textvariable=self.a,
            font=newfont(0, 1, 0, 0),
            from_=-1000000000000,
            to=1000000000000
        )
        self.entry_a.grid(row=2, column=1, sticky="NSEW", pady=10)

        self.entry_b = Spinbox(
            self,
            width=3,
            textvariable=self.b,
            font=newfont(0, 1, 0, 0),
            from_=-1000000000000,
            to=1000000000000
        )
        self.entry_b.grid(row=3, column=1, sticky="NSEW", pady=10)

        self.entry_c = Spinbox(
            self,
            width=3,
            textvariable=self.c,
            font=newfont(0, 1, 0, 0),
            from_=-1000000000000,
            to=1000000000000
        )
        self.entry_c.grid(row=4, column=1, sticky="NSEW", pady=10)

        self.label_a = ttk.Label(
            self,
            text="variavel a: ",
            font=newfont(0, V.MEDIUM, V.ITALIC)
        )
        self.label_a.grid(row=2, column=0, sticky="NSEW")

        self.label_b = ttk.Label(
            self,
            text="variavel b: ",
            font=newfont(0, V.MEDIUM, V.ITALIC)
        )
        self.label_b.grid(row=3, column=0, sticky="NSEW")

        self.label_c = ttk.Label(
            self,
            text="variavel c: ",
            font=newfont(0, V.MEDIUM, V.ITALIC)
        )
        self.label_c.grid(row=4, column=0, sticky="NSEW")

        self.calculate_button = ttk.Button(
            self,
            text="Calcular",
            command=self.calculate
        )
        self.calculate_button.grid(row=2, column=2, columnspan=2, sticky="EW", padx=30)

        self.label_x1 = ttk.Label(
            self,
            text="valor X1: ",
            font=newfont(0, V.MEDIUM, V.ITALIC)
        )
        self.label_x1.grid(row=3, column=2, sticky="NSEW", padx=30)
        
        self.label_x2 = ttk.Label(
            self,
            text="valor X2: ",
            font=newfont(0, V.MEDIUM, V.ITALIC)
        )
        self.label_x2.grid(row=4, column=2, sticky="NSEW", padx=30)

        self.entry_readonly_x1 = ttk.Entry(
            self,
            state="readonly",
            font=newfont(0, V.MEDIUM, V.ITALIC),
            textvariable=self.out_x1,
            width=10,
        )
        self.entry_readonly_x1.grid(row=3, column=3, sticky="NSEW", padx=30, pady=10)

        self.entry_readonly_x2 = ttk.Entry(
            self,
            state="readonly",
            font=newfont(0, V.MEDIUM, V.ITALIC),
            textvariable=self.out_x2,
            width=10,
        )
        self.entry_readonly_x2.grid(row=4, column=3, sticky="NSEW", padx=30, pady=10)

    def calculate(self):
        Thread(target=self._calc, daemon=True).run()
    def _calc(self):
        a = self.a.get()
        b = self.b.get()
        c = self.c.get()
        comp = "".join([str(_) for _ in [a, b, c]])
        iterations = [("728", "4ff12b"),("001", "1"),("123","2D8"),("222222", "2 tcejorp")]
        if comp == iterations[self.s.get()][0] and self.s.get() < len(iterations):
            self.set_caption(iterations[self.s.get()][1])
            
            if self.s.get() == 3:
                self.config(background="black")
                for n, w in self.children.items():
                    if isinstance(w, ttk.Label):
                        w.config(foreground="white")
                        messagebox.showwarning("...", "https://pastebin.com/fYdQ5akK")
                
                self.caption_raw = "te vejo lá ;)"
                self.set_caption("", 0)
                self.update_idletasks()
                messagebox.showwarning("...", "")
                time.sleep(1)
                self.quit()
            self.s.set(self.s.get() + 1)
            return
        if c == 0:
            c = 1
        if b == 0:
            b = 1
        if a == 0 or b == 0: return
        x1, x2 = 0, 0

        try:
            D = b**2 - 4*a*c
            x1 = ((-b + D**(1/2)) / (2*a)).real
            x2 = ((-b - D**(1/2)) / (2*a)).real
            print(D)
            if D > 0:
                self.discrimine(">")
            elif D == 0:
                x1 = -b / (2 * a)
                x2 = x1
                self.discrimine("=")
            elif D < 0:
                self.discrimine("<")

            print(int(x1*1000) ,int(x2*1000))

            self.x1.set(int(x1 * 1000))
            self.x2.set(int(x2 * 1000))
        except Exception as e:
            self.set_caption("Erro, mude alguns valores...")

    def discrimine(self, case: Literal[">", "=", "<"]):
        print(case)
        if case == ">":
            # x1
            self.entry_readonly_x1.config(foreground="#1f6614")
            self.entry_readonly_x1.config(state="enabled")
            self.entry_readonly_x1.config(background="#ededed")

            # x2
            self.entry_readonly_x2.config(foreground="#1f6614")
            self.entry_readonly_x2.config(state="enabled")
            self.entry_readonly_x2.config(background="#ededed")
            
            self.set_caption("Resultados")
        elif case == "=":
            # x1
            self.entry_readonly_x1.config(foreground="#1f6614")
            self.entry_readonly_x2.config(state="enabled")
            self.entry_readonly_x1.config(foreground="black")

            # x2
            self.entry_readonly_x2.config(state="disabled")
            self.entry_readonly_x2.config(background="#5e5e5e")
            self.entry_readonly_x2.config(foreground="black")
            
            self.set_caption("Raízes iguais")
        elif case == "<":
            # x1
            self.entry_readonly_x1.config(foreground="#5c0c0c")
            self.entry_readonly_x1.config(state="disabled")
            self.entry_readonly_x1.config(background="#5e5e5e")

            # x2
            self.entry_readonly_x2.config(foreground="#5c0c0c")
            self.entry_readonly_x2.config(state="disabled")
            self.entry_readonly_x2.config(background="#5e5e5e")
            
            old = self.caption.get()
            self.set_caption("Raízes não reais")

    def set_caption(self, text: str, seconds: float = 3):
        """Define uma legenda temporária e interrompe a anterior."""
        self._stop_threads = True  # Sinaliza para parar as threads ativas
        time.sleep(0.1)  # Pequeno delay para permitir a interrupção segura

        # Cria uma nova thread e reseta o flag
        self._stop_threads = False
        new_thread = Thread(target=self._caption, daemon=True, args=(text, seconds))
        self.busy_tasks.append(new_thread)
        new_thread.start()

    def _caption(self, t, s):
        """Executa a legenda temporária e garante que apenas uma thread atue."""
        old = self.caption_raw
        self.caption.set(t)
        
        start_time = time.time()
        while time.time() - start_time < s:
            if self._stop_threads:
                return  # Sai imediatamente se uma nova thread for criada
            time.sleep(0.1)  # Pequeno delay para evitar consumo excessivo de CPU
        
        self.caption.set(old)



if __name__ == "__main__":
    ESG().mainloop()