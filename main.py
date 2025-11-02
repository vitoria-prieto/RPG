from personagens import *

def main():
    fada = Fada("Luna")
    humano = Humano("Carlos", "bardo")
    elfo = Elfo("Elandril", "arqueiro")
    
    personagens = [fada, humano, elfo]
    rodada = 1

    while True:
        print(f"\n===== RODADA {rodada} =====")

        if not fada.esta_congelado() and fada.vida > 0:
            alvo = random.choice([humano, elfo])
            acao = random.choice(["glitter_mortal", "cristal_de_gelo", "bomba_de_glitter"])
            print(f"\nTurno de {fada.nome}:")
            if acao == "glitter_mortal":
                fada.glitter_mortal(alvo)
            elif acao == "cristal_de_gelo":
                fada.cristal_de_gelo(alvo)
            elif acao == "bomba_de_glitter":
                fada.bomba_de_glitter()
        
        if not humano.esta_congelado() and humano.vida > 0:
            alvo = random.choice([fada, elfo])
            acao = random.choice(["balada", "musica", "microfonada", "ataque", "panela"])
            print(f"\nTurno de {humano.nome}:")
            if acao == "balada":
                humano.balada_da_confusao(alvo)
            elif acao == "musica":
                humano.musica_da_cura()
            elif acao == "microfonada":
                humano.microfonada(alvo)
            elif acao == "panela":
                humano.panela()
            elif acao == "ataque":
                humano.atacar(alvo)
        
        if not elfo.esta_congelado() and elfo.vida > 0:
            alvo = random.choice([fada, humano])
            acao = random.choice(["arco", "fuga", "prisao", "transforma"])
            print(f"\nTurno de {elfo.nome}:")
            if acao == "arco":
                elfo.arco_e_flecha(alvo)
            elif acao == "fuga":
                elfo.fuga()
            elif acao == "prisao":
                elfo.prissao(alvo)
            elif acao == "transforma":
                elfo.se_transforma(alvo)

        print("\n-- Atualizando status dos personagens --")
        for p in personagens:
            if p.vida > 0:
                p.atualizar_status()
                p.mostrar_status()

        vivos = [p for p in personagens if p.vida > 0]
        if len(vivos) <= 1:
            print("\n===== FIM DE JOGO =====")
            if vivos:
                print(f"{vivos[0].nome} venceu!")
            else:
                print("Empate!")
            break

        rodada += 1



if __name__ == '__main__' :
    main()
    