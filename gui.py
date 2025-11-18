import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPG Turn Based")
        self.geometry("300x200") 

       
        self.options_list = ["Fada", "Bardo", "Cozinheiro", "Elfo"]
        

        self.shared_data = {
            "username": tk.StringVar(),
            "selected_option": tk.StringVar()
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
        frame = self.frames[page]
        if hasattr(frame, "update_page"): 
            frame.update_page()
        frame.tkraise()

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ttk.Label(self, text="Nome do Personagem:").pack(pady=10)
        entry = ttk.Entry(self, textvariable=controller.shared_data["username"])
        entry.pack()

       
        ttk.Label(self, text="Selecione uma Classe:").pack(pady=(10, 0))
        
        combobox = ttk.Combobox(
            self,
            textvariable=controller.shared_data["selected_option"],
            values=controller.options_list,
            state="readonly"  
        )
        combobox.set(controller.options_list[0]) 
        combobox.pack(pady=5)
       

        ttk.Button(self, text="Continue",
                   command=lambda: controller.show_frame(WelcomePage)).pack(pady=10)


class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="Bem vindo!").pack(pady=10)
        ttk.Label(self, textvariable=controller.shared_data["username"]).pack()

        ttk.Label(self, text="Sua seleção:").pack(pady=(10, 0))
        ttk.Label(self, textvariable=controller.shared_data["selected_option"]).pack()

        
        self.skills_frame = ttk.Frame(self)
        self.skills_frame.pack(pady=10)

        ttk.Button(self, text="Voltar",
                   command=lambda: controller.show_frame(LoginPage)).pack(pady=10)

    def update_page(self):
        """Atualiza os botões toda vez que a página é mostrada."""
        
        for w in self.skills_frame.winfo_children():
            w.destroy()

        selecionado = self.controller.shared_data["selected_option"].get()

        classes = {
            "Fada": {
                "Ataque": "Bomba de Gliter Mortal",
                "Ataque Especial": "Magia de Gelo",
                "Fuga": "Bomba de Fumaça"
            },
            "Bardo": {
                "Ataque": "Balada da Confusao",
                "Ataque Especial": "Microfonada",
                "Fuga": "Musica da Cura"
            },
            "Cozinheiro": {
                "Ataque": "Batata Quente",
                "Ataque Especial": "Receita da Mamae",
                "Fuga": "Panela"
            },
            "Elfo": {
                "Ataque": "Arco e Flecha",
                "Ataque Especial": "Magia de Gelo",
                "Fuga": "Agilidade"
            },
        }

        skills = classes.get(selecionado, {})

        for nome in skills.values():
            
            ttk.Button(self.skills_frame, text=nome).pack()

        
        

      


if __name__ == "__main__":
    app = App()
    app.mainloop()