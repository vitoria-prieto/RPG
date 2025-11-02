import random

class Personagem:
    def __init__(self, nome, vida):
        self.nome = nome
        self.vida = vida
        self.status = {} 
    
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
            raise Exception("Personagem morreu")
            

    # metodo de aplicar status effect
    def aplicar_status(self, nome_status, duracao):

        # gera no dicionario a key do nome_status e o value duração
        self.status[nome_status] = duracao
        
    # Printa tela os atributos dos personagens 
    def atualizar_status(self):

        to_remove = []
        # para cada status e duração no dicionario retornado em tuplas
        for status, dur in self.status.items():

            if status == 'glitter_mortal':
                self.aplicar_dano(15)

            elif status == 'musica_da_cura':
                self.vida += 16

                
            elif status == 'microfonada':
                self.aplicar_dano(15)
                
            # retira uma duração do status    
            self.status[status] -= 1

            # inclui na lista para remoção de status
            if self.status[status] <= 0:
                to_remove.append(status)

        # Retira status na lista
        for status in to_remove:
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
    def __init__(self, nome, classe):
        super().__init__(nome, 100)
        
        self.classe = classe
        self.protecao_panela = False


#  Classe Bardo (Humano)
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
    def batata_quente(self, alvo):
        alvo.aplicar_dano(10)
        
    
    def receita_da_mamae(self):
        self.vida += 15
        
    
    def panela(self):
        self.status['panela'] = 1
        

# Humano   
    def atacar(self, alvo):
        dano = 10 
        alvo.aplicar_dano(dano)


class Elfo(Personagem):
    def __init__(self, nome, classe):
        super().__init__(nome, 100)
        self.classe = classe
    
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
    fada = Fada("Luna")
    humano = Humano("Carlos", "bardo")
    elfo = Elfo("Elandril", "arqueiro")
    
    for i in range (26):
        try:
            fada.bomba_de_glitter()
        except Exception as E:
            print(E)
        try:
            humano.balada_da_confusao(fada)
            humano.balada_da_confusao(fada)
            humano.balada_da_confusao(fada)
            humano.balada_da_confusao(fada)
        except Exception as E:
            print(E)
        try:
            elfo.arco_e_flecha(humano)
        except Exception as E:
            print(E)
        
        fada.atualizar_status()
        humano.atualizar_status()
        elfo.atualizar_status()

        print(f"\nRodada {i}:\n")
        fada.mostrar_status()
        humano.mostrar_status()
        elfo.mostrar_status()
    
    print(f"\n\n\n\n\n")
    fada.mostrar_status()
    humano.mostrar_status()
    elfo.mostrar_status()