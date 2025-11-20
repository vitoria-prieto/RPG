import tkinter as tk
from tkinter import messagebox
import random
from gui import App, BattlePage, LoginPage # Removida a WelcomePage
from personagens import Demonio, Assassino, Golem, Dragao

class RPGController:
    def __init__(self):
        self.app = App()
        
        # Conectar o botão da LoginPage diretamente ao método de início
        login_page = self.app.frames[LoginPage]
        login_page.btn_iniciar.config(command=self.iniciar_jogo)
        
        self.jogador = None
        self.inimigo = None
        self.rodada = 1
        self.max_rodadas = 5
        self.view_batalha = None
        
    def iniciar_jogo(self):
        # 1. Coletar dados da LoginPage
        nome = self.app.shared_data["username"].get() or "Herói Anônimo"
        classe_nome = self.app.shared_data["selected_option"].get()
        classe_obj = self.app.classes_map[classe_nome]
        
        # 2. Instanciar Modelo (Personagem)
        self.jogador = classe_obj(nome)
        self.rodada = 1
        self.gerar_inimigo()
        
        # 3. Criar a BattlePage
        if BattlePage in self.app.frames:
            self.app.frames[BattlePage].destroy()
            
        self.view_batalha = BattlePage(self.app.container, self.app)
        self.app.frames[BattlePage] = self.view_batalha
        self.view_batalha.grid(row=0, column=0, sticky="nsew")
        
        # 4. CONFIGURAÇÃO DINÂMICA DOS BOTÕES
        # Aqui pegamos as habilidades da classe e atualizamos os textos dos botões
        skills = self.jogador.obter_habilidades()
        self.view_batalha.configurar_habilidades(skills)

        # 5. Configurar Ações dos Botões
        self.view_batalha.btn_atk.config(command=lambda: self.turno_jogador("atacar"))
        self.view_batalha.btn_esp.config(command=lambda: self.turno_jogador("especial"))
        self.view_batalha.btn_fug.config(command=lambda: self.turno_jogador("fuga"))
        
        # 6. Mostrar a tela de batalha
        self.app.show_frame(BattlePage)
        self.atualizar_view()
        self.view_batalha.log(f"=== BATALHA INICIADA: {self.inimigo.nome} apareceu! ===")

    def gerar_inimigo(self):
        if self.rodada < self.max_rodadas:
            InimigoClass = random.choice([Demonio, Assassino, Golem])
            self.inimigo = InimigoClass(f"Monstro {self.rodada}")
        else:
            self.inimigo = Dragao("Dragão Supremo")

    def atualizar_view(self):
        self.view_batalha.atualizar_interface(
            self.rodada, self.max_rodadas, self.jogador, self.inimigo
        )

    def processar_efeitos_status(self, personagem):
        eventos = personagem.atualizar_status()
        for ev in eventos:
            self.view_batalha.log(f"[EFEITO] {ev}")

    def turno_jogador(self, acao):
        """Fase 1: Ação do Jogador"""
        self.view_batalha.toggle_botoes("disabled")
        
        if self.jogador.esta_impedido():
             self.view_batalha.log(f"{self.jogador.nome} está {self.jogador.get_nome_impedimento()} e não pode agir!")
        else:
            dano = 0
            msg = ""
            # Captura o nome da habilidade usada para deixar o log mais bonito
            habilidades = self.jogador.obter_habilidades()
            
            if acao == "atacar":
                dano = self.jogador.atacar(self.inimigo)
                nome_skill = habilidades.get("Ataque")
                msg = f"usou {nome_skill} causando {dano} dano!"
            elif acao == "especial":
                dano = self.jogador.ataque_status(self.inimigo)
                nome_skill = habilidades.get("Especial")
                msg = f"usou {nome_skill}! ({dano} dano)"
            elif acao == "fuga":
                self.jogador.fuga()
                nome_skill = habilidades.get("Fuga")
                msg = f"usou {nome_skill}!"
            
            self.view_batalha.log(f"Você {msg}")

        self.atualizar_view()

        if self.inimigo.vida <= 0:
            self.finalizar_rodada(vitoria=True)
            return

        self.app.after(1500, self.turno_inimigo)

    def turno_inimigo(self):
        """Fase 2: Ação do Inimigo"""
        self.processar_efeitos_status(self.jogador)
        self.processar_efeitos_status(self.inimigo)
        self.atualizar_view()

        if self.verificar_fim_jogo(): return

        if not self.inimigo.esta_impedido():
            rolagem = random.randint(1, 10)
            msg = ""
            if rolagem <= 7:
                dano = self.inimigo.atacar(self.jogador)
                msg = f"atacou você causando {dano} dano!"
            elif rolagem <= 9:
                dano = self.inimigo.ataque_status(self.jogador)
                msg = f"usou habilidade vil! ({dano} dano)"
            else:
                self.inimigo.fuga()
                msg = "fortaleceu a defesa!"
            
            self.view_batalha.log(f"{self.inimigo.nome} {msg}")
        else:
            self.view_batalha.log(f"{self.inimigo.nome} está {self.inimigo.get_nome_impedimento()}!")

        self.atualizar_view()
        
        if self.verificar_fim_jogo(): return
        
        self.view_batalha.toggle_botoes("normal")
        self.view_batalha.log("-" * 40)

    def verificar_fim_jogo(self):
        if self.jogador.vida <= 0:
            self.finalizar_jogo(vitoria=False)
            return True
        if self.inimigo.vida <= 0:
            self.finalizar_rodada(vitoria=True)
            return True
        return False

    def finalizar_rodada(self, vitoria):
        if self.rodada >= self.max_rodadas:
            self.finalizar_jogo(vitoria=True)
        else:
            messagebox.showinfo("Vitória!", f"Você derrotou {self.inimigo.nome}!")
            self.rodada += 1
            self.gerar_inimigo()
            self.view_batalha.log(f"\n=== ROUND {self.rodada}: {self.inimigo.nome} ===")
            self.atualizar_view()
            self.view_batalha.toggle_botoes("normal")

    def finalizar_jogo(self, vitoria):
        if vitoria:
            messagebox.showinfo("FIM", "PARABÉNS! Você venceu o jogo!")
        else:
            messagebox.showerror("GAME OVER", "Seu herói caiu em combate...")
        self.app.show_frame(LoginPage)

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    controller = RPGController()
    controller.run()