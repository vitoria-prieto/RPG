import random
from abc import ABC, abstractmethod

class Personagem(ABC):
    def __init__(self, nome, vida, velocidade):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.velocidade = velocidade
        self.status = {} 
    
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
        self.dano = 1
    
    def atacar(self, alvo):
        return alvo.aplicar_dano(self.dano)
    
    def ataque_status(self, alvo):
        alvo.aplicar_status('glitter_mortal', 4)
        return 0
    
    def fuga(self):
        self.aplicar_status('bomba_de_glitter', 3)
        return 0
    
    def cristal_de_gelo(self, alvo):
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
    
    def balada_da_confusao(self, alvo):
        if random.randint(1, 10) <= 3:
            alvo.aplicar_status('balada_da_confusao', 2)
            return True
        return False


class Cozinheiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.classe = 'cozinheiro'
        self.velocidade = 7
    
    def ataque_status(self, alvo):
        dano = alvo.aplicar_dano(15)
        alvo.aplicar_status('queimadura', 2)
        return dano
    
    def fuga(self):
        self.status['panela'] = 1
        return 0
    
    def receita_da_mamae(self):
        cura = min(15, self.vida_maxima - self.vida)
        self.vida = min(self.vida_maxima, self.vida + 15)
        return cura


class Elfo(Personagem):
    def __init__(self, nome, classe):
        super().__init__(nome, vida=100, velocidade=12)
        self.classe = classe
    
    def atacar(self, alvo):
        return alvo.aplicar_dano(10)
    
    def ataque_status(self, alvo):
        alvo.aplicar_status('prisao', 2)
        return 0
    
    def fuga(self):
        self.aplicar_status('fuga', 1)
        return 0
    
    def se_transforma(self, alvo):
        return alvo.aplicar_dano(20)
    
    def arco_e_flecha(self, alvo):
        dano = 21 if random.randint(1, 10) <= 3 else 7
        return alvo.aplicar_dano(dano)
    
    def cristal_de_gelo(self, alvo):
        alvo.aplicar_status('cristal_de_gelo', 2)
        return 0


class Golem(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=200, velocidade=3)
        self.dano = 8
        self.defesa = 5
    
    def aplicar_dano(self, dano):
        dano_reduzido = max(0, dano - self.defesa)
        if 'pele_de_pedra' in self.status:
            dano_reduzido = max(0, dano_reduzido - 5)
        return super().aplicar_dano(dano_reduzido)
    
    def atacar(self, alvo):
        return alvo.aplicar_dano(12)
    
    def ataque_status(self, alvo):
        dano = alvo.aplicar_dano(15)
        alvo.aplicar_status('prisao', 1)
        return dano
    
    def fuga(self):
        self.aplicar_status('pele_de_pedra', 2)
        return 0
    
    def regeneracao(self):
        cura = min(20, self.vida_maxima - self.vida)
        self.vida = min(self.vida_maxima, self.vida + 20)
        return cura


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
    
    def drenar_vida(self, alvo):
        dano = alvo.aplicar_dano(15)
        cura = min(dano, self.vida_maxima - self.vida)
        self.vida = min(self.vida_maxima, self.vida + dano)
        return dano


class Assassino(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=90, velocidade=18)
        self.dano = 12
        self.chance_critico = 40
        self.multiplicador_critico = 2.5
    
    def _calcular_critico(self, dano_base):
        if random.randint(1, 100) <= self.chance_critico:
            return int(dano_base * self.multiplicador_critico)
        return dano_base
    
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
    
    def golpe_preciso(self, alvo):
        dano = int(self.dano * self.multiplicador_critico)
        return alvo.aplicar_dano(dano)


class Dragao(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=300, velocidade=10)
        self.dano = 35
        self.chance_critico = 20
        self.multiplicador_critico = 3.0
        self.defesa = 10
    
    def aplicar_dano(self, dano):
        dano_reduzido = max(0, dano - self.defesa)
        if 'escamas_de_ferro' in self.status:
            dano_reduzido = max(0, dano_reduzido - 15)
        return super().aplicar_dano(dano_reduzido)
    
    def _calcular_critico(self, dano_base):
        if random.randint(1, 100) <= self.chance_critico:
            return int(dano_base * self.multiplicador_critico)
        return dano_base
    
    def atacar(self, alvo):
        dano = self._calcular_critico(self.dano)
        return alvo.aplicar_dano(dano)
    
    def ataque_status(self, alvo):
        dano = self._calcular_critico(45)
        return alvo.aplicar_dano(dano)
    
    def fuga(self):
        self.aplicar_status('escamas_de_ferro', 3)
        return 0
    
    def sopro_de_fogo(self, alvos):
        danos = []
        for alvo in alvos:
            if alvo.vida > 0:
                danos.append((alvo.nome, alvo.aplicar_dano(40)))
        return danos
    
    def voo_rasante(self, alvo):
        dano = alvo.aplicar_dano(30)
        self.aplicar_status('fuga', 1)
        return dano
    
    def rugido_aterrorizante(self, alvos):
        confusos = []
        for alvo in alvos:
            if alvo.vida > 0 and random.randint(1, 100) <= 50:
                alvo.aplicar_status('balada_da_confusao', 2)
                confusos.append(alvo.nome)
        return confusos


if __name__ == "__main__":
    print("="*60)
    print("TESTE DE TODAS AS CLASSES E METODOS")
    print("="*60)
    
    # ==================== TESTE FADA ====================
    print("\n--- TESTE FADA ---")
    fada = Fada("Sininho")
    alvo = Humano("Dummy")
    
    print(f"Ataque basico: {fada.atacar(alvo)} de dano")
    fada.ataque_status(alvo)
    print(f"Glitter mortal aplicado: {alvo.status}")
    fada.fuga()
    print(f"Bomba de glitter ativa: {fada.status}")
    fada.cristal_de_gelo(alvo)
    print(f"Alvo congelado: {alvo.esta_congelado()}")
    print(f"Estado final: {alvo}")
    
    # ==================== TESTE HUMANO ====================
    print("\n--- TESTE HUMANO ---")
    humano = Humano("Guerreiro")
    alvo = Fada("Dummy2")
    
    print(f"Ataque basico: {humano.atacar(alvo)} de dano")
    print(f"Ataque status: {humano.ataque_status(alvo)} de dano")
    humano.vida = 50
    print(f"Fuga (cura): {humano.fuga()} HP restaurados")
    print(f"Estado final: {humano}")
    
    # ==================== TESTE BARDO ====================
    print("\n--- TESTE BARDO ---")
    bardo = Bardo("Mozart")
    alvo = Cozinheiro("Dummy3")
    
    print(f"Ataque basico: {bardo.atacar(alvo)} de dano")
    bardo.ataque_status(alvo)
    print(f"Microfonada aplicada: {alvo.status}")
    bardo.vida = 50
    bardo.fuga()
    print(f"Musica da cura ativa: {bardo.status}")
    confusao = bardo.balada_da_confusao(alvo)
    print(f"Balada da confusao: {'Sucesso' if confusao else 'Falhou'}")
    print(f"Estado final: {alvo}")
    
    # ==================== TESTE COZINHEIRO ====================
    print("\n--- TESTE COZINHEIRO ---")
    cozinheiro = Cozinheiro("Gordon")
    alvo = Bardo("Dummy4")
    
    print(f"Ataque basico: {cozinheiro.atacar(alvo)} de dano")
    print(f"Ataque status: {cozinheiro.ataque_status(alvo)} de dano + queimadura")
    cozinheiro.fuga()
    print(f"Panela ativa: {cozinheiro.status}")
    cozinheiro.vida = 50
    print(f"Receita da mamae: {cozinheiro.receita_da_mamae()} HP curados")
    print(f"Estado final: {alvo}")
    
    # ==================== TESTE ELFO DRUIDA ====================
    print("\n--- TESTE ELFO DRUIDA ---")
    druida = Elfo("Groot", "druida")
    alvo = Humano("Dummy5")
    
    print(f"Ataque basico: {druida.atacar(alvo)} de dano")
    druida.ataque_status(alvo)
    print(f"Prisao aplicada: {alvo.esta_preso()}")
    druida.fuga()
    print(f"Fuga ativa: {druida.esta_fugindo()}")
    print(f"Se transforma: {druida.se_transforma(alvo)} de dano")
    print(f"Estado final: {alvo}")
    
    # ==================== TESTE ELFO ARQUEIRO ====================
    print("\n--- TESTE ELFO ARQUEIRO ---")
    arqueiro = Elfo("Legolas", "arqueiro")
    alvo = Golem("Dummy6")
    
    print(f"Ataque basico: {arqueiro.atacar(alvo)} de dano")
    arqueiro.ataque_status(alvo)
    print(f"Prisao aplicada: {alvo.esta_preso()}")
    print(f"Arco e flecha: {arqueiro.arco_e_flecha(alvo)} de dano")
    arqueiro.cristal_de_gelo(alvo)
    print(f"Congelado: {alvo.esta_congelado()}")
    print(f"Estado final: {alvo}")
    
    # ==================== TESTE GOLEM ====================
    print("\n--- TESTE GOLEM ---")
    golem = Golem("Rochoso")
    alvo = Demonio("Dummy7")
    
    print(f"Ataque basico: {golem.atacar(alvo)} de dano")
    print(f"Ataque status: {golem.ataque_status(alvo)} de dano + prisao")
    golem.fuga()
    print(f"Pele de pedra ativa: {golem.status}")
    dano_recebido = golem.aplicar_dano(20)
    print(f"Golem recebe 20 de dano (defesa 5): {dano_recebido} real")
    golem.vida = 150
    print(f"Regeneracao: {golem.regeneracao()} HP curados")
    print(f"Estado final: {golem}")
    
    # ==================== TESTE DEMONIO ====================
    print("\n--- TESTE DEMONIO ---")
    demonio = Demonio("Infernus")
    alvo = Dragao("Dummy8")
    
    print(f"Ataque basico: {demonio.atacar(alvo)} de dano")
    demonio.fuga()
    print(f"Furia ativa: {demonio.status}")
    print(f"Ataque com furia: {demonio.atacar(alvo)} de dano")
    print(f"Ataque status: {demonio.ataque_status(alvo)} de dano + sangramento")
    demonio.vida = 50
    print(f"Drenar vida: {demonio.drenar_vida(alvo)} de dano")
    print(f"Estado final: Demonio={demonio.vida}, Alvo={alvo.vida}")
    
    # ==================== TESTE ASSASSINO ====================
    print("\n--- TESTE ASSASSINO ---")
    assassino = Assassino("Sombra")
    
    print("Testando ataques (40% chance de critico):")
    danos = [assassino.atacar(Humano(f"Teste{i}")) for i in range(3)]
    print(f"  Danos causados: {danos}")
    
    alvo = Fada("Dummy9")
    print(f"Ataque status: {assassino.ataque_status(alvo)} de dano + sangramento")
    assassino.fuga()
    print(f"Furtividade: {assassino.esta_fugindo()}")
    alvo2 = Humano("DummyGolpe")
    print(f"Golpe preciso: {assassino.golpe_preciso(alvo2)} de dano (critico garantido)")
    print(f"Estado final: {alvo}")
    
    # ==================== TESTE DRAGAO ====================
    print("\n--- TESTE DRAGAO ---")
    dragao = Dragao("Ancalagon")
    
    print("Testando ataques (20% chance de critico):")
    danos = [dragao.atacar(Humano(f"TesteDrag{i}")) for i in range(3)]
    print(f"  Danos causados: {danos}")
    
    alvo = Humano("Dummy10")
    print(f"Ataque status (mordida): {dragao.ataque_status(alvo)} de dano")
    dragao.fuga()
    print(f"Escamas de ferro ativa: {dragao.status}")
    
    dano_recebido = dragao.aplicar_dano(30)
    print(f"Dragao recebe 30 de dano (defesa 10+15): {dano_recebido} real")
    
    alvos_aoe = [Humano("AOE1"), Humano("AOE2"), Humano("AOE3")]
    danos_aoe = dragao.sopro_de_fogo(alvos_aoe)
    print(f"Sopro de fogo AOE: {danos_aoe}")
    
    alvo_voo = Humano("DummyVoo")
    print(f"Voo rasante: {dragao.voo_rasante(alvo_voo)} de dano")
    
    alvos_rugido = [Humano("Rug1"), Humano("Rug2"), Humano("Rug3")]
    confusos = dragao.rugido_aterrorizante(alvos_rugido)
    print(f"Rugido confundiu: {confusos if confusos else 'Ninguem'}")
    
    # ==================== TESTE ATUALIZAR STATUS ====================
    print("\n--- TESTE ATUALIZAR STATUS ---")
    teste = Humano("TesteStatus")
    teste.aplicar_status('sangramento', 2)
    teste.aplicar_status('musica_da_cura', 2)
    
    print(f"Status inicial: {teste.status}, Vida: {teste.vida}")
    eventos1 = teste.atualizar_status()
    print(f"Turno 1: {eventos1}, Vida: {teste.vida}")
    eventos2 = teste.atualizar_status()
    print(f"Turno 2: {eventos2}, Vida: {teste.vida}")
    
    print("\n" + "="*60)
    print("TODOS OS TESTES CONCLUIDOS")
    print("="*60)