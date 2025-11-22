# Membros
Esse projeto foi criado por:
 - Thiago Ribeiro do Val Medeiros
 - Vitória Rafaela Prieto da Silva
 - Hauany Aparecida da Silva Lima Bueno

# RPG Turn Based ⚔️

Um jogo de RPG em turnos desenvolvido em Python, utilizando a biblioteca `tkinter` para a interface gráfica e princípios de Programação Orientada a Objetos (POO) para a lógica de combate e personagens.

## 📋 Sobre o Projeto

O jogo consiste em uma batalha de 5 rounds. O jogador escolhe um herói e enfrenta inimigos gerados aleatoriamente até chegar ao chefe final, o Dragão. O sistema conta com mecânicas de status (congelamento, queimadura, sangramento), habilidades especiais e buffs/debuffs.

## 🚀 Como Executar

### Pré-requisitos

  * Python 3.x instalado.
  * Biblioteca `tkinter` (geralmente já vem instalada com o Python).

### Passo a Passo

1.  Certifique-se de que todos os arquivos (`main.py`, `gui.py`, `personagens.py`) estejam na mesma pasta.
2.  Abra o terminal na pasta do projeto.
3.  Execute o comando:

<!-- end list -->

```bash
python main.py
```

## 📂 Estrutura do Projeto

  * **`main.py`**: O controlador principal. Gerencia o fluxo do jogo (início, turnos, fim de jogo) e conecta a lógica (`personagens.py`) com a interface (`gui.py`).
  * **`gui.py`**: Contém as classes da interface gráfica (`App`, `LoginPage`, `BattlePage`). Responsável por exibir a vida, botões de ação e o log de batalha.
  * **`personagens.py`**: Contém a lógica de negócio. Define a classe base `Personagem`, os status (`Enum`) e as classes específicas de heróis e inimigos.

## 🧙‍♂️ Classes de Personagens

O jogador pode escolher entre 4 classes, cada uma com atributos e habilidades únicas:

### 1\. Fada 🧚‍♀️

Focada em controle e dano por tempo (DoT).

  * **HP:** 65 | **Velocidade:** 15.
  * **Habilidades:**
      * *Ataque:* **Bomba de Glitter** (Aplica efeito mortal).
      * *Especial:* **Magia de Gelo** (Congela o inimigo, impedindo ação).
      * *Fuga:* **Fumaça Mágica** (Torna-se imune a dano temporariamente).

### 2\. Bardo 🎵

Classe equilibrada que causa confusão e possui cura.

  * **HP:** 100 | **Velocidade:** 10.
  * **Habilidades:**
      * *Ataque:* **Balada da Confusão** (Chance de confundir o alvo).
      * *Especial:* **Microfonada** (Causa dano contínuo).
      * *Fuga:* **Música da Cura** (Regenera vida).

### 3\. Cozinheiro 🍳

Tanque com alta capacidade de cura e defesa.

  * **HP:** 100 | **Velocidade:** 7.
  * **Habilidades:**
      * *Ataque:* **Batata Quente** (Causa dano e queimadura).
      * *Especial:* **Banquete** (Cura a si mesmo).
      * *Fuga:* **Defesa de Panela** (Reduz o dano recebido).

### 4\. Elfo 🏹

Focado em dano crítico e agilidade.

  * **HP:** 100 | **Velocidade:** 12.
  * **Habilidades:**
      * *Ataque:* **Arco e Flecha** (Chance de dano crítico alto).
      * *Especial:* **Flecha de Gelo** (Congela o inimigo).
      * *Fuga:* **Agilidade Élfica** (Cura e esquiva).

## 👹 Inimigos

Os inimigos são sorteados a cada rodada, culminando em um chefe final.

1.  **Golem:** Alta vida (200 HP), causa prisão (stun) e possui defesa passiva.
2.  **Demônio:** Dano base alto, entra em estado de **Fúria** (dobra o ataque) e causa sangramento.
3.  **Assassino:** Alta chance de crítico, muito veloz e causa sangramento.
4.  **Dragão (Chefe):** Encontrado na última rodada. HP massivo (300), ataques críticos poderosos e defesa reforçada.

## ⚡ Sistema de Status

O jogo possui um sistema complexo de efeitos:

  * **Impedimento:** *Cristal de Gelo, Prisão, Fuga* (Personagem não pode agir).
  * **Dano por Turno (DoT):** *Queimadura, Sangramento, Glitter Mortal, Microfonada*.
  * **Buffs:** *Fúria* (Aumenta dano), *Música da Cura* (Regeneração), *Panela* (Redução de dano).
