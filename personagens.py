import random
from abc import ABC, abstractmethod

class Personagem(ABC):
    def __init__(self, nome, vida, velocidade):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.velocidade = velocidade
        self.status = {} 
        self.nome_ataque = ""
    
    def __str__(self):
        status_str = ", ".join([f"{k}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return (f"{self.__class__.__name__}: {self.nome} | "
                f"Vida: {self.vida}/{self.vida_maxima} | "
                f"Velocidade: {self.velocidade} | "
                f"Status: {status_str}")
    
    def aplicar_dano(self, dano):
        if 'bomba_de_glitter' in self.status:
            return 0
        
        if 'panela' in self.status:
            dano = max(0, dano - 10)
            self.status.pop('panela')
        
        dano_aplicado = min(dano, self.vida)
        self.vida = max(0, self.vida - dano)
        return dano_aplicado
            
    def aplicar_status(self, nome_status, duracao):
        self.status[nome_status] = duracao
        
    def atualizar_status(self):
        to_remove = []
        eventos = []
        
        for status, dur in list(self.status.items()):
            if status == 'glitter_mortal':
                dano = self.aplicar_dano(15)
                eventos.append(f"{self.nome} sofre {dano} de glitter mortal")
            elif status == 'musica_da_cura':
                cura = min(16, self.vida_maxima - self.vida)
                self.vida = min(self.vida_maxima, self.vida + 16)
                eventos.append(f"{self.nome} regenera {cura} HP")
            elif status == 'microfonada':
                dano = self.aplicar_dano(15)
                eventos.append(f"{self.nome} sofre {dano} de microfonada")
            elif status == 'sangramento':
                dano = self.aplicar_dano(5)
                eventos.append(f"{self.nome} sangra {dano} HP")
            elif status == 'queimadura':
                dano = self.aplicar_dano(5)
                eventos.append(f"{self.nome} queima {dano} HP")

            if status in self.status: 
                self.status[status] -= 1
                if self.status[status] <= 0:
                    to_remove.append(status)

        for status in to_remove:
            if status in self.status:
                self.status.pop(status)
        
        return eventos
    
    def esta_congelado(self):
        return 'cristal_de_gelo' in self.status
    
    def esta_preso(self):
        return 'prisao' in self.status
    
    def esta_fugindo(self):
        return 'fuga' in self.status
    
    def esta_confuso(self):
        return 'balada_da_confusao' in self.status

    def pode_agir(self):
        return not (self.esta_congelado() or self.esta_preso() or self.esta_fugindo())

    def get_impedimento(self):
        if self.esta_congelado():
            return "congelado"
        elif self.esta_preso():
            return "preso"
        elif self.esta_fugindo():
            return "em fuga"
        return None

    @abstractmethod
    def atacar(self, alvo):
        pass
    
    @abstractmethod
    def ataque_status(self, alvo):
        pass
    
    @abstractmethod
    def fuga(self):
        pass


class Fada(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=65, velocidade=15)
        self.nome_ataque = 'glitter_mortal'

    
    
    def atacar(self, alvo):
        
        alvo.aplicar_status('glitter_mortal', 4)
        return 0
    
    def fuga(self):
        self.aplicar_status('bomba_de_glitter', 3)
        return 0
    
    def ataque_status(self, alvo):
        alvo.aplicar_status('cristal_de_gelo', 2)
        return 0


class Humano(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=100, velocidade=8)
    
    def atacar(self, alvo):
        return alvo.aplicar_dano(10)
    
    def ataque_status(self, alvo):
        return alvo.aplicar_dano(20)
    
    def fuga(self):
        cura = min(10, self.vida_maxima - self.vida)
        self.vida = min(self.vida_maxima, self.vida + 10)
        return cura


class Bardo(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.classe = 'bardo'
        self.velocidade = 10
    
    def ataque_status(self, alvo):
        alvo.aplicar_status('microfonada', 4)
        return 0
    
    def fuga(self):
        self.aplicar_status('musica_da_cura', 2)
        return 0
    
    def atacar(self, alvo):
        if random.randint(1, 10) <= 3:
            alvo.aplicar_status('balada_da_confusao', 2)
            return True
        return False


class Cozinheiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.classe = 'cozinheiro'
        self.velocidade = 7
    
    def atacar(self, alvo):
        dano = alvo.aplicar_dano(15)
        alvo.aplicar_status('queimadura', 2)
        return dano
    
    def fuga(self):
        self.status['panela'] = 1
        return 0
    
    def ataque_status(self):
        cura = min(15, self.vida_maxima - self.vida)
        self.vida = min(self.vida_maxima, self.vida + 15)
        return cura


class Elfo(Personagem):
    def __init__(self, nome, classe):
        super().__init__(nome, vida=100, velocidade=12)
        self.classe = classe

    def fuga(self):
        self.aplicar_status('fuga', 1)
        return 0

    def atacar(self, alvo):
        dano = 21 if random.randint(1, 10) <= 3 else 7
        return alvo.aplicar_dano(dano)
    
    def ataque_status(self, alvo):
        alvo.aplicar_status('cristal_de_gelo', 2)
        return 0


class Golem(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=200, velocidade=3)
        self.dano = 8
        self.defesa = 5

    
    def atacar(self, alvo):
        return alvo.aplicar_dano(12)
    
    def ataque_status(self, alvo):
        dano = alvo.aplicar_dano(15)
        alvo.aplicar_status('prisao', 1)
        return dano
    
    def fuga(self):
        self.aplicar_status('pele_de_pedra', 2)
        return 0
  


class Demonio(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=80, velocidade=14)
        self.dano = 25
    
    def atacar(self, alvo):
        dano = self.dano * 2 if 'furia' in self.status else self.dano
        return alvo.aplicar_dano(dano)
    
    def ataque_status(self, alvo):
        dano = alvo.aplicar_dano(30)
        alvo.aplicar_status('sangramento', 3)
        return dano
    
    def fuga(self):
        self.aplicar_status('furia', 2)
        return 0
    
    


class Assassino(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=90, velocidade=18)
        self.dano : int = 12
        self.chance_critico = 40
        self.multiplicador_critico = 2.5
    
    def _calcular_critico(self,dano : int):
        num = random.randint(1,100)

        if num < 25:
            self.dano *= 2
        return self.dano
    
    def atacar(self, alvo):
        dano = self._calcular_critico(self.dano)
        return alvo.aplicar_dano(dano)
    
    def ataque_status(self, alvo):
        dano = self._calcular_critico(18)
        dano_aplicado = alvo.aplicar_dano(dano)
        alvo.aplicar_status('sangramento', 3)
        return dano_aplicado
    
    def fuga(self):
        self.aplicar_status('fuga', 1)
        return 0



class Dragao(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=300, velocidade=10)
        self.dano = 35
        self.chance_critico = 20
        self.multiplicador_critico = 3.0
        self.defesa = 10
    
    def _calcular_critico(self,dano : int):
        num = random.randint(1,100)

        if num < 25:
            self.dano *= 2
        return self.dano    
    
    def atacar(self, alvo):
        dano = self._calcular_critico(self.dano)
        return alvo.aplicar_dano(dano)
    
    def ataque_status(self, alvo):
        dano = self._calcular_critico(45)
        return alvo.aplicar_dano(dano)
    
    def fuga(self):
        self.aplicar_status('escamas_de_ferro', 3)
        return 0
    


if __name__ == "__main__":
   pass