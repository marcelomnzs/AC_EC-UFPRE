# Análise da Transição Crítica da Propagação do Sarampo em um Modelo SIR Espacial Usando Box-Counting

Este repositório contém a implementação computacional do trabalho **“Análise da Transição Crítica da Propagação do Sarampo em um Modelo SIR Espacial Usando Box-Counting”**, cujo objetivo é investigar a dinâmica espacial da propagação do sarampo por meio de um modelo epidemiológico SIR implementado como um autômato celular bidimensional, com análise da transição crítica utilizando dimensão fractal.

---

## 🎓 Contexto Acadêmico

Este projeto é um **entregável acadêmico** desenvolvido para avaliação das INdisciplinas:

- **Cellular Automata**
- **Epidemiology Computing**

do curso de **Bacharelado em Sistemas de Informação (BSI)** da  
**Universidade Federal Rural de Pernambuco (UFRPE)**.

A implementação serve como suporte computacional para o artigo científico associado, permitindo a reprodução dos experimentos descritos no trabalho.

---

## 🧠 Descrição do Modelo

- Modelo epidemiológico: **SIR (Suscetível–Infectado–Recuperado)**
- Espaço: **Grade bidimensional L × L**
- Abordagem: **Autômato celular com vizinhança de Moore**
- Dinâmica:
  - Transmissão local com probabilidade β
  - Recuperação com probabilidade γ
- Análise espacial:
  - Extração do padrão no pico da infecção
  - Estimativa da **dimensão fractal** via **Box-Counting**
- Objetivo principal:
  - Identificar a transição crítica entre regimes subcrítico, crítico e supercrítico
  - Relacionar o limiar epidêmico a fenômenos de percolação

---

## 🛠️ Tecnologias Utilizadas

### Linguagem de Programação
- **Python 3**

### Bibliotecas Utilizadas
- `numpy` — operações numéricas e manipulação de matrizes
- `matplotlib` — visualização gráfica (séries temporais e padrões espaciais)
- `scipy` — ajuste linear para o cálculo da dimensão fractal
- `random` — geração de eventos estocásticos

---

## 📊 Funcionalidades da Implementação

- Simulação do modelo SIR espacial em autômato celular
- Visualização temporal das populações S, I e R
- Visualização espacial da grade (estado inicial, pico da infecção e estado final)
- Cálculo da dimensão fractal dos clusters infecciosos
- Experimento sistemático variando a taxa de transmissão β
- Geração do gráfico Dimensão Fractal × β

---

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
    
2. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt

3. Execute a simulação:
   ```bash
   python sir_spatial_boxcounting.py
