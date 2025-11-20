import tkinter as tk
from tkinter import ttk
from personagens import Fada, Bardo, Cozinheiro, Elfo

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPG Turn Based")
        self.geometry("600x550") 
        
        self.shared_data = {
            "username": tk.StringVar(),
            "selected_option": tk.StringVar(value="Fada")
        }

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        self.classes_map = {
            "Fada": Fada,
            "Bardo": Bardo,
            "Cozinheiro": Cozinheiro,
            "Elfo": Elfo
        }

        # Apenas LoginPage é criada no início. BattlePage é recriada a cada jogo.
        frame = LoginPage(self.container, self)
        self.frames[LoginPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        
        # Estilização simples para centralizar
        frame_centro = ttk.Frame(self)
        frame_centro.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame_centro, text="RPG BATTLE", font=("Arial", 20, "bold")).pack(pady=20)

        ttk.Label(frame_centro, text="Nome do Herói:", font=("Arial", 12)).pack(pady=5)
        ttk.Entry(frame_centro, textvariable=controller.shared_data["username"], width=25).pack(pady=5)

        ttk.Label(frame_centro, text="Escolha sua Classe:", font=("Arial", 12)).pack(pady=(20, 5))
        
        # Dropdown
        cb = ttk.Combobox(frame_centro, textvariable=controller.shared_data["selected_option"], 
                         values=list(controller.classes_map.keys()), state="readonly")
        cb.pack(pady=5)
        cb.current(0)
       
        # Este botão será configurado no main.py para iniciar o jogo
        self.btn_iniciar = ttk.Button(frame_centro, text="INICIAR BATALHA", width=20)
        self.btn_iniciar.pack(pady=30)


class BattlePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Topo: Rounds ---
        self.round_label = ttk.Label(self, text="Round 1", font=("Arial", 14, "bold"))
        self.round_label.pack(pady=10)
        
        # --- Área de Status (HP/Infos) ---
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill="x", padx=20, pady=5)
        
        # Jogador
        self.frm_jogador = ttk.LabelFrame(stats_frame, text="Você")
        self.frm_jogador.pack(side="left", fill="both", expand=True, padx=5)
        self.lbl_jogador_hp = ttk.Label(self.frm_jogador, text="HP: 100/100")
        self.lbl_jogador_hp.pack()
        self.lbl_jogador_status = ttk.Label(self.frm_jogador, text="Status: -")
        self.lbl_jogador_status.pack()

        # Inimigo
        self.frm_inimigo = ttk.LabelFrame(stats_frame, text="Oponente")
        self.frm_inimigo.pack(side="right", fill="both", expand=True, padx=5)
        self.lbl_inimigo_hp = ttk.Label(self.frm_inimigo, text="HP: ???")
        self.lbl_inimigo_hp.pack()
        self.lbl_inimigo_status = ttk.Label(self.frm_inimigo, text="Status: -")
        self.lbl_inimigo_status.pack()

        # --- Log de Batalha ---
        self.log_text = tk.Text(self, height=12, state="disabled", wrap="word", bg="#f0f0f0")
        self.log_text.pack(padx=20, pady=10, fill="both", expand=True)
        
        # --- Área de Ações (Botões Dinâmicos) ---
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(pady=15, padx=10, fill="x")
        
        # Configuração do Grid para centralizar
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)

        # Coluna 0: Ataque Básico
        ttk.Label(self.btn_frame, text="ATAQUE BÁSICO", font=("Arial", 8, "bold"), foreground="gray").grid(row=0, column=0)
        self.btn_atk = ttk.Button(self.btn_frame, text="Ataque") # Texto será mudado dinamicamente
        self.btn_atk.grid(row=1, column=0, padx=5, sticky="ew")

        # Coluna 1: Especial
        ttk.Label(self.btn_frame, text="ESPECIAL (Status)", font=("Arial", 8, "bold"), foreground="blue").grid(row=0, column=1)
        self.btn_esp = ttk.Button(self.btn_frame, text="Especial")
        self.btn_esp.grid(row=1, column=1, padx=5, sticky="ew")

        # Coluna 2: Fuga/Defesa
        ttk.Label(self.btn_frame, text="FUGA / DEFESA", font=("Arial", 8, "bold"), foreground="green").grid(row=0, column=2)
        self.btn_fug = ttk.Button(self.btn_frame, text="Fuga")
        self.btn_fug.grid(row=1, column=2, padx=5, sticky="ew")

    def configurar_habilidades(self, habilidades: dict):
        """Recebe o dicionário de habilidades do personagem e atualiza os botões"""
        # Ex: habilidades = {"Ataque": "Batata Quente", "Especial": "Banquete", ...}
        self.btn_atk.config(text=habilidades.get("Ataque", "Atacar"))
        self.btn_esp.config(text=habilidades.get("Especial", "Especial"))
        self.btn_fug.config(text=habilidades.get("Fuga", "Defender"))

    def atualizar_interface(self, rodada, max_rodadas, jogador, inimigo):
        self.round_label.config(text=f"Round {rodada}/{max_rodadas}")
        
        st_jog = ", ".join([f"{k.value}" for k in jogador.status]) or "Normal"
        st_ini = ", ".join([f"{k.value}" for k in inimigo.status]) or "Normal"

        self.frm_jogador.config(text=f"{jogador.nome} ({jogador.__class__.__name__})")
        self.lbl_jogador_hp.config(text=f"HP: {jogador.vida}/{jogador.vida_maxima}")
        self.lbl_jogador_status.config(text=f"Status: {st_jog}")

        self.frm_inimigo.config(text=f"{inimigo.nome} ({inimigo.__class__.__name__})")
        self.lbl_inimigo_hp.config(text=f"HP: {inimigo.vida}/{inimigo.vida_maxima}")
        self.lbl_inimigo_status.config(text=f"Status: {st_ini}")

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def toggle_botoes(self, estado="normal"):
        self.btn_atk.config(state=estado)
        self.btn_esp.config(state=estado)
        self.btn_fug.config(state=estado)