import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPG Turn Based")
        self.geometry("400x300") # Aumentei um pouco a altura

        # --- NOVO ---
        # Lista de opções para o dropdown
        self.options_list = ["Fada", "Bardo", "Cozinheiro", "Elfo"]
        # --- FIM NOVO ---

        self.shared_data = {
            "username": tk.StringVar(),
            "selected_option": tk.StringVar() # --- NOVO ---
        }

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, WelcomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        self.frames[page].tkraise()


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ttk.Label(self, text="Nome do Personagem:").pack(pady=10)
        entry = ttk.Entry(self, textvariable=controller.shared_data["username"])
        entry.pack()

        # --- NOVO CÓDIGO DO DROPDOWN ---
        ttk.Label(self, text="Selecione uma Classe:").pack(pady=(10, 0))
        
        combobox = ttk.Combobox(
            self,
            textvariable=controller.shared_data["selected_option"],
            values=controller.options_list,
            state="readonly"  # Impede que o usuário digite no campo
        )
        combobox.set(controller.options_list[0]) # Define o valor padrão
        combobox.pack(pady=5)
        # --- FIM NOVO CÓDIGO ---

        ttk.Button(self, text="Continue",
                   command=lambda: controller.show_frame(WelcomePage)).pack(pady=10)


class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ttk.Label(self, text="Bem vindo!").pack(pady=10)
        ttk.Label(self, textvariable=controller.shared_data["username"]).pack()

        # --- NOVO CÓDIGO PARA MOSTRAR A SELEÇÃO ---
        ttk.Label(self, text="Sua seleção:").pack(pady=(10, 0))
        ttk.Label(self, textvariable=controller.shared_data["selected_option"]).pack()
        # --- FIM NOVO CÓDIGO ---

        ttk.Button(self, text="Voltar",
                   command=lambda: controller.show_frame(LoginPage)).pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()