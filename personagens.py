import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Union

class Status(Enum):
    GLITTER_MORTAL = "glitter_mortal"
    MICROFONADA = "microfonada"
    SANGRAMENTO = "sangramento"
    QUEIMADURA = "queimadura"
    MUSICA_DA_CURA = "musica_da_cura"
    BOMBA_DE_GLITTER = "bomba_de_glitter"
    PANELA = "panela"
    CRISTAL_DE_GELO = "cristal_de_gelo"
    PRISAO = "prisao"
    FUGA = "fuga"
    BALADA_DA_CONFUSAO = "balada_da_confusao"
    PELE_DE_PEDRA = "pele_de_pedra"
    FURIA = "furia"
    ESCAMAS_DE_FERRO = "escamas_de_ferro"

class Personagem(ABC):
    def __init__(self, nome: str, vida: int, velocidade: int):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.velocidade = velocidade
        self.status: Dict[Status, int] = {} 
        self.dano_base = 0
        self.chance_critico = 0
        self.multiplicador_critico = 1.0
    
    @staticmethod
    @abstractmethod
    def obter_habilidades() -> Dict[str, str]:
        """Retorna nomes das habilidades para a UI"""
        pass

    def __str__(self):
        # Converte Enums para string legível na UI
        status_str = ", ".join([f"{k.value}({v})" for k, v in self.status.items()]) if self.status else "Nenhum"
        return (f"{self.__class__.__name__}: {self.nome} | "
                f"Vida: {self.vida}/{self.vida_maxima} | "
                f"Velocidade: {self.velocidade} | "
                f"Status: {status_str}")
    
    def aplicar_dano(self, dano: int) -> int:
        if Status.BOMBA_DE_GLITTER in self.status:
            return 0
        
        if Status.PANELA in self.status:
            dano = max(0, dano - 10)
            self.status.pop(Status.PANELA)
        
        dano_aplicado = min(dano, self.vida)
        self.vida = max(0, self.vida - dano)
        return dano_aplicado
            
    def aplicar_status(self, status: Status, duracao: int):
        self.status[status] = duracao
    
    def curar(self, quantidade: int) -> int:
        cura = min(quantidade, self.vida_maxima - self.vida)
        self.vida = min(self.vida_maxima, self.vida + quantidade)
        return cura
    
    def calcular_critico(self, dano: int) -> int:
        if random.randint(1, 100) <= self.chance_critico:
            return int(dano * self.multiplicador_critico)
        return dano
        
    def atualizar_status(self) -> List[str]:
        to_remove = []
        eventos = []
        
        # Mapeamento de Efeitos
        efeitos_status = {
            Status.GLITTER_MORTAL: (15, "sofre {dano} de glitter mortal"),
            Status.MICROFONADA: (15, "sofre {dano} de microfonada"),
            Status.SANGRAMENTO: (5, "sangra {dano} HP"),
            Status.QUEIMADURA: (5, "queima {dano} HP"),
            Status.MUSICA_DA_CURA: (-16, "regenera {dano} HP")
        }
        
        # Itera sobre uma cópia para evitar erro de modificação durante iteração
        for stat, dur in list(self.status.items()):
            if stat in efeitos_status:
                valor, msg = efeitos_status[stat]
                if valor > 0:
                    dano = self.aplicar_dano(valor)
                else:
                    dano = self.curar(abs(valor))
                eventos.append(f"{self.nome} {msg.format(dano=dano)}")

            if stat in self.status:
                self.status[stat] -= 1
                if self.status[stat] <= 0:
                    to_remove.append(stat)

        for stat in to_remove:
            self.status.pop(stat, None)
        
        return eventos
    
    def esta_impedido(self) -> bool:
        impedimentos = [Status.CRISTAL_DE_GELO, Status.PRISAO, Status.FUGA]
        return any(s in self.status for s in impedimentos)
    
    def get_nome_impedimento(self) -> Optional[str]:
        mapa = {
            Status.CRISTAL_DE_GELO: 'congelado',
            Status.PRISAO: 'preso',
            Status.FUGA: 'em fuga'
        }
        for s, msg in mapa.items():
            if s in self.status:
                return msg
        return None
    
    def esta_confuso(self):
        return Status.BALADA_DA_CONFUSAO in self.status

    @abstractmethod
    def atacar(self, alvo): pass
    
    @abstractmethod
    def ataque_status(self, alvo): pass
    
    @abstractmethod
    def fuga(self): pass


class Fada(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=65, velocidade=15)
    
    @staticmethod
    def obter_habilidades():
        return {"Ataque": "Bomba de Glitter", "Especial": "Magia de Gelo", "Fuga": "Fumaça Mágica"}
    
    def atacar(self, alvo):
        alvo.aplicar_status(Status.GLITTER_MORTAL, 4)
        return 0
    
    def fuga(self):
        self.aplicar_status(Status.BOMBA_DE_GLITTER, 3)
        return 0
    
    def ataque_status(self, alvo):
        alvo.aplicar_status(Status.CRISTAL_DE_GELO, 2)
        return 0


class Humano(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=100, velocidade=8)
    
    def atacar(self, alvo):
        return alvo.aplicar_dano(10)
    
    def ataque_status(self, alvo):
        return alvo.aplicar_dano(20)
    
    def fuga(self):
        return self.curar(10)


class Bardo(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.velocidade = 10

    @staticmethod
    def obter_habilidades():
        return {"Ataque": "Balada da Confusão", "Especial": "Microfonada", "Fuga": "Música da Cura"}
    
    def ataque_status(self, alvo):
        alvo.aplicar_status(Status.MICROFONADA, 4)
        return 0
    
    def fuga(self):
        self.aplicar_status(Status.MUSICA_DA_CURA, 2)
        return 0
    
    def atacar(self, alvo):
        # Bardo tem chance de causar confusão no ataque básico
        if random.randint(1, 10) <= 3:
            alvo.aplicar_status(Status.BALADA_DA_CONFUSAO, 2)
            return 0 # Confusão não causa dano imediato neste design
        return alvo.aplicar_dano(8)


class Cozinheiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.velocidade = 7
    
    @staticmethod
    def obter_habilidades():
        return {"Ataque": "Batata Quente", "Especial": "Banquete (Cura)", "Fuga": "Defesa de Panela"}

    def atacar(self, alvo):
        dano = alvo.aplicar_dano(15)
        alvo.aplicar_status(Status.QUEIMADURA, 2)
        return dano
    
    def fuga(self):
        self.aplicar_status(Status.PANELA, 1)
        return 0
    
    def ataque_status(self, alvo=None): # Alvo é opcional pois cura a si mesmo
        return self.curar(15)


class Elfo(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=100, velocidade=12)
    
    @staticmethod
    def obter_habilidades():
        return {"Ataque": "Arco e Flecha", "Especial": "Flecha de Gelo", "Fuga": "Agilidade Élfica"}

    def fuga(self):
        return self.curar(10)

    def atacar(self, alvo):
        dano = 21 if random.randint(1, 10) <= 3 else 7
        return alvo.aplicar_dano(dano)
    
    def ataque_status(self, alvo):
        alvo.aplicar_status(Status.CRISTAL_DE_GELO, 2)
        return 0


# Inimigos (Simplificados para brevidade, mas seguem a lógica)
class Golem(Personagem):
    def __init__(self, nome): super().__init__(nome, 200, 3)
    @staticmethod
    def obter_habilidades(): return {}
    def atacar(self, alvo): return alvo.aplicar_dano(12)
    def ataque_status(self, alvo): 
        d = alvo.aplicar_dano(15)
        alvo.aplicar_status(Status.PRISAO, 1)
        return d
    def fuga(self): self.aplicar_status(Status.PELE_DE_PEDRA, 2); return 0

class Demonio(Personagem):
    def __init__(self, nome): super().__init__(nome, 80, 14); self.dano_base = 25
    @staticmethod
    def obter_habilidades(): return {}
    def atacar(self, alvo): 
        d = self.dano_base * 2 if Status.FURIA in self.status else self.dano_base
        return alvo.aplicar_dano(d)
    def ataque_status(self, alvo):
        d = alvo.aplicar_dano(30)
        alvo.aplicar_status(Status.SANGRAMENTO, 3)
        return d
    def fuga(self): self.aplicar_status(Status.FURIA, 2); return 0

class Assassino(Personagem):
    def __init__(self, nome): 
        super().__init__(nome, 90, 18)
        self.chance_critico = 25; self.multiplicador_critico = 2.0
    @staticmethod
    def obter_habilidades(): return {}
    def atacar(self, alvo): return alvo.aplicar_dano(self.calcular_critico(12))
    def ataque_status(self, alvo): 
        d = alvo.aplicar_dano(self.calcular_critico(18))
        alvo.aplicar_status(Status.SANGRAMENTO, 3); return d
    def fuga(self): return self.curar(15)

class Dragao(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 300, 10)
        self.chance_critico = 25; self.multiplicador_critico = 2.0
    @staticmethod
    def obter_habilidades(): return {}
    def atacar(self, alvo): return alvo.aplicar_dano(self.calcular_critico(35))
    def ataque_status(self, alvo): return alvo.aplicar_dano(self.calcular_critico(45))
    def fuga(self): self.aplicar_status(Status.ESCAMAS_DE_FERRO, 3); return 0