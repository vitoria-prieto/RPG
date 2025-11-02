import random

class Personagem:
    def __init__(self, nome, vida):
        self.nome = nome
        self.vida = vida
        self.status = {} 
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return f"Personagem: {self.nome} | Vida: {self.vida} | Status: {status_str}"
    
    def aplicar_dano(self, dano):
        # Se tiver status de glitter a vida é igual
        if 'bomba_de_glitter' in self.status:
            self.vida = self.vida
        # Se panela estiver on, reduz dano em 10
        if 'panela' in self.status:
            dano -= 10
            # Se dano for menor que 0, dano igual a 0
            if dano < 0:
                dano = 0     
            # tira o status panela caso exista.
            self.status.pop('panela')
        # tira da vida o dano depois de aplicar redução de dano da panela
        self.vida -= dano

        # Se vida for menos ou igual a Zero resulta em derrota
        if self.vida < 0:
            self.vida = 0
            
            

    # metodo de aplicar status effect
    def aplicar_status(self, nome_status, duracao):

        # gera no dicionario a key do nome_status e o value duração
        self.status[nome_status] = duracao
        
    # Printa tela os atributos dos personagens 
    def atualizar_status(self):

        to_remove = []
        # para cada status e duração no dicionario retornado em tuplas
        for status, dur in list(self.status.items()):

            if status == 'glitter_mortal':
                self.aplicar_dano(15)

            elif status == 'musica_da_cura':
                self.vida += 16

                
            elif status == 'microfonada':
                self.aplicar_dano(15)

            if status in self.status: 
                # retira uma duração do status
                self.status[status] -= 1

                # inclui na lista para remoção de status
                if self.status[status] <= 0:
                    to_remove.append(status)

        # Retira status na lista
        for status in to_remove:
            if status in self.status:
                self.status.pop(status)
    
    # adiciona status no objeto
    def esta_congelado(self):
        return 'cristal_de_gelo' in self.status
    
    def esta_preso(self):
        return 'prissao' in self.status
    
    def esta_fugindo(self):
        return 'fuga' in self.status
    
    def esta_confuso(self):
        return 'balada_da_confusao' in self.status


    # opcional
    def mostrar_status(self):
        print(f"{self.nome} - Vida: {self.vida} - Status: {self.status}")



# Personagem Fada = Vida : 65 | dano : 1 [ bomba de gliter, Cristal de gelo, gliter mortal, atacar]

class Fada(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 65)
        self.dano = 1
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return (f"🧚 Fada: {self.nome}\n"
                f"   Vida: {self.vida}/65 | Dano: {self.dano}\n"
                f"   Status: {status_str}\n"
                f"   Habilidades: Bomba de Glitter, Cristal de Gelo, Glitter Mortal, Atacar")
    
    def bomba_de_glitter(self):
        self.aplicar_status('bomba_de_glitter', 3)
    
    def cristal_de_gelo(self, alvo):
        alvo.aplicar_status('cristal_de_gelo', 2)
        
    
    def glitter_mortal(self, alvo):
        alvo.aplicar_status('glitter_mortal', 4)
        
    # se estiver congelado não pode atacar
    def atacar(self, alvo):
        if alvo.esta_congelado():
            return
        self.aplicar_dano(self.dano)

# Personagem Humano 

class Humano(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 100)
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return (f"👤 Humano: {self.nome}\n"
                f"   Vida: {self.vida}/100\n"
                f"   Status: {status_str}\n"
                f"   Habilidades: Atacar (10 de dano)")
        


# Humano   
    def atacar(self, alvo):
        dano = 10 
        alvo.aplicar_dano(dano)


#  Classe Bardo (Humano)
class Bardo(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.classe = 'bardo'
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return (f"🎵 Bardo: {self.nome}\n"
                f"   Vida: {self.vida}/100 | Classe: {self.classe}\n"
                f"   Status: {status_str}\n"
                f"   Habilidades: Balada da Confusão (30% chance), Música da Cura (+32 HP), "
                f"Microfonada (60 dano over time), Atacar (10 de dano)")
    
    def balada_da_confusao(self, alvo):
        # Escolhe um numero entre 1 a 10 
        chance = random.randint(1,10)
        
        # Se for menor que 3 aplica balada da confusão
        if chance <= 3:
            alvo.aplicar_status('balada_da_confusao', 2)
        else:
            pass
    
    def musica_da_cura(self):
        self.aplicar_status('musica_da_cura', 2)
    

    def microfonada(self, alvo):
        alvo.aplicar_status('microfonada', 4)
        


 # Classe Cozinheiro(Humano):   
class Cozinheiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.classe = 'cozinheiro'
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return (f"👨‍🍳 Cozinheiro: {self.nome}\n"
                f"   Vida: {self.vida}/100 | Classe: {self.classe}\n"
                f"   Status: {status_str}\n"
                f"   Habilidades: Batata Quente (10 de dano), Receita da Mamãe (+15 HP), "
                f"Panela (-10 dano recebido 1x), Atacar (10 de dano)")
    
    def batata_quente(self, alvo):
        alvo.aplicar_dano(10)
        
    
    def receita_da_mamae(self):
        self.vida += 15
        
    
    def panela(self):
        self.status['panela'] = 1
        




class Elfo(Personagem):
    def __init__(self, nome, classe):
        super().__init__(nome, 100)
        self.classe = classe
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        
        if self.classe == "druida":
            habilidades = "Se Transforma (20 de dano), Fuga (1 turno), Prisão (2 turnos), Atacar (10 de dano)"
        elif self.classe == "arqueiro":
            habilidades = "Arco e Flecha (7 ou 21 crítico), Agilidade (fuga 1 turno), Cristal de Gelo (congela 2 turnos), Atacar (10 de dano)"
        else:
            habilidades = "Nenhuma habilidade específica"
        
        return (f"🧝 Elfo: {self.nome}\n"
                f"   Vida: {self.vida}/100 | Classe: {self.classe}\n"
                f"   Status: {status_str}\n"
                f"   Habilidades: {habilidades}")
    
    #Classe Druida
    def se_transforma(self, alvo):
        dano = 20
        alvo.aplicar_dano(dano)
    
    def fuga(self):
        self.aplicar_status('fuga', 1)
        
    
    def prissao(self, alvo):
        alvo.aplicar_status('prisao', 2)
        

    #Classe Arqueiro
    def arco_e_flecha(self, alvo):
        chance_critico = random.randint(1,10)
        if chance_critico <= 3:
            dano = 21
            
        else:
            dano = 7
            alvo.aplicar_dano(dano)
    
    def agilidade(self):
        self.aplicar_status('fuga', 1)
        
    def cristal_de_gelo(self, alvo):
        alvo.aplicar_status('cristal_de_gelo', 2)


if __name__ == "__main__":
##script de teste classe e combate


    # Criar personagens
    fada = Fada("Tinker Bell")
    bardo = Bardo("Músico Maluco")
    cozinheiro = Cozinheiro("Chef Ramsay")
    druida = Elfo("Groot", "druida")
    arqueiro = Elfo("Legolas", "arqueiro")
    
    personagens = [fada, bardo, cozinheiro, druida, arqueiro]
    
    print("=== INÍCIO DA BATALHA ===\n")
    
    # 25 rodadas ou até sobrar apenas 1
    for rodada in range(1, 26):
        print(f"\n{'='*50}")
        print(f"RODADA {rodada}")
        print(f"{'='*50}\n")
        
        # Filtrar personagens vivos
        vivos = [p for p in personagens if p.vida > 0]
        
        # Verificar condição de vitória
        if len(vivos) <= 1:
            print("\n🏆 FIM DA BATALHA! 🏆")
            if len(vivos) == 1:
                print(f"\nVencedor: {vivos[0].nome} com {vivos[0].vida} de vida!")
            else:
                print("\nTodos foram derrotados!")
            break
        
        # Cada personagem vivo ataca
        for atacante in vivos[:]:
            if atacante.vida <= 0:
                continue
                
            # Verificar se está congelado ou preso
            if atacante.esta_congelado():
                print(f"❄️  {atacante.nome} está congelado e não pode agir!")
                continue
            
            if atacante.esta_preso():
                print(f"🪢 {atacante.nome} está preso e não pode agir!")
                continue
                
            if atacante.esta_fugindo():
                print(f"💨 {atacante.nome} está em fuga e não pode atacar!")
                atacante.atualizar_status()
                continue
            
            # Escolher alvo aleatório (diferente do atacante)
            alvos_possiveis = [p for p in vivos if p != atacante and p.vida > 0]
            if not alvos_possiveis:
                break
                
            alvo = random.choice(alvos_possiveis)
            
            # Se estiver confuso, pode atacar aliado ou inimigo
            if atacante.esta_confuso():
                alvo = random.choice([p for p in vivos if p != atacante])
                print(f"😵 {atacante.nome} está confuso!")
            
            try:
                # FADA
                if isinstance(atacante, Fada):
                    acao = random.choice(['bomba_glitter', 'cristal_gelo', 'glitter_mortal', 'atacar'])
                    
                    if acao == 'bomba_glitter':
                        print(f"✨ {atacante.nome} usa Bomba de Glitter!")
                        atacante.bomba_de_glitter()
                    elif acao == 'cristal_gelo':
                        print(f"❄️  {atacante.nome} congela {alvo.nome} com Cristal de Gelo!")
                        atacante.cristal_de_gelo(alvo)
                    elif acao == 'glitter_mortal':
                        print(f"💀 {atacante.nome} aplica Glitter Mortal em {alvo.nome}!")
                        atacante.glitter_mortal(alvo)
                    else:
                        print(f"👊 {atacante.nome} ataca {alvo.nome}!")
                        alvo.aplicar_dano(atacante.dano)
                
                # HUMANO
                elif isinstance(atacante, Bardo):
                    acao = random.choice(['balada', 'musica_cura', 'microfonada', 'atacar'])
                    
                    if acao == 'balada':
                        print(f"🎵 {atacante.nome} toca Balada da Confusão em {alvo.nome}!")
                        atacante.balada_da_confusao(alvo)
                    elif acao == 'musica_cura':
                        print(f"🎶 {atacante.nome} usa Música da Cura!")
                        atacante.musica_da_cura()
                    elif acao == 'microfonada':
                        print(f"🎤 {atacante.nome} dá uma Microfonada em {alvo.nome}!")
                        atacante.microfonada(alvo)
                    else:
                        print(f"👊 {atacante.nome} ataca {alvo.nome}!")
                        atacante.atacar(alvo)
                
                elif isinstance(atacante, Cozinheiro):
                    acao = random.choice(['batata_quente', 'receita_mamae', 'panela', 'atacar'])
                    
                    if acao == 'batata_quente':
                        print(f"🔥 {atacante.nome} joga Batata Quente em {alvo.nome}!")
                        atacante.batata_quente(alvo)
                    elif acao == 'receita_mamae':
                        print(f"🍲 {atacante.nome} usa Receita da Mamãe!")
                        atacante.receita_da_mamae()
                    elif acao == 'panela':
                        print(f"🍳 {atacante.nome} equipa a Panela!")
                        atacante.panela()
                    else:
                        print(f"👊 {atacante.nome} ataca {alvo.nome}!")
                        atacante.atacar(alvo)
                
                # ELFO
                elif isinstance(atacante, Elfo):
                    if atacante.classe == "druida":
                        acao = random.choice(['transforma', 'fuga', 'prisao', 'atacar'])
                        
                        if acao == 'transforma':
                            print(f"🐻 {atacante.nome} se transforma e ataca {alvo.nome}!")
                            atacante.se_transforma(alvo)
                        elif acao == 'fuga':
                            print(f"💨 {atacante.nome} usa Fuga!")
                            atacante.fuga()
                        elif acao == 'prisao':
                            print(f"🪢 {atacante.nome} prende {alvo.nome}!")
                            atacante.prissao(alvo)
                        else:
                            print(f"👊 {atacante.nome} ataca {alvo.nome} (dano padrão 10)!")
                            alvo.aplicar_dano(10)
                    
                    elif atacante.classe == "arqueiro":
                        acao = random.choice(['arco_flecha', 'agilidade', 'cristal_gelo', 'atacar'])
                        
                        if acao == 'arco_flecha':
                            print(f"🏹 {atacante.nome} atira flecha em {alvo.nome}!")
                            atacante.arco_e_flecha(alvo)
                        elif acao == 'agilidade':
                            print(f"⚡ {atacante.nome} usa Agilidade!")
                            atacante.agilidade()
                        elif acao == 'cristal_gelo':
                            print(f"❄️  {atacante.nome} congela {alvo.nome}!")
                            atacante.cristal_de_gelo(alvo)
                        else:
                            print(f"👊 {atacante.nome} ataca {alvo.nome} (dano padrão 10)!")
                            alvo.aplicar_dano(10)
                
            except Exception as e:
                print(f"💀 {alvo.nome} foi derrotado!")
        
        # Atualizar status de todos os personagens vivos
        print("\n--- Atualizando Status ---")
        for p in vivos:
            if p.vida > 0:
                p.atualizar_status()
                p.mostrar_status()
        
        # Mostrar estado final da rodada
        print("\n--- Estado Final da Rodada ---")
        for p in personagens:
            if p.vida > 0:
                print(f"✅ {p.nome}: {p.vida} HP")
            else:
                print(f"❌ {p.nome}: MORTO")
    
        # Se chegou em 25 rodadas
        if rodada == 25:
            print("\n\n🏁 25 RODADAS COMPLETADAS! 🏁")
            sobreviventes = [p for p in personagens if p.vida > 0]
            if sobreviventes:
                print("\n🏆 Sobreviventes:")
                for s in sobreviventes:
                    print(f"  - {s.nome}: {s.vida} HP")
                vencedor = max(sobreviventes, key=lambda x: x.vida)
                print(f"\n👑 Maior HP: {vencedor.nome} com {vencedor.vida} de vida!")

    print("\n=== FIM DA BATALHA ===")

    print(fada)
    print(bardo)
    print(cozinheiro)   