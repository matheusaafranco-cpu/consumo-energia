# ⚡ Calculadora de Consumo Elétrico Inteligente

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)

## 📌 Sobre o Projeto
A **Calculadora de Consumo Elétrico Inteligente** é uma aplicação desenvolvida em Python voltada para a conscientização energética, estimativa de consumo e previsão de custos de aparelhos eletrodomésticos.

O projeto foi projetado com forte rigor de software, incluindo validação contínua de dados de entrada, laços de repetição seguros, resiliência a falhas de rede (mecanismos de *fallback*) e organização modular para facilidade de manutenção.

---

## 🔀 Detalhamento e Comparativo das Versões

O sistema possui duas versões independentes que atendem a diferentes necessidades operacionais:

### ⚙️ 1. Versão Avançada (`app.py`)
Focada em precisão e automação via integração de serviços web.
* **Consulta Automática de Localização:** Consome a API pública do ViaCEP para converter o CEP informado pelo usuário no Estado (UF) e Cidade correspondentes.
* **Bandeira Tarifária em Tempo Real:** Consulta um dataset JSON público online para determinar a bandeira vigente no país (Verde, Amarela ou Vermelha) e o custo adicional cobrado por kWh.
* **Cálculo com Impostos:** Aplica uma alíquota estimada de tributos/impostos (~22%) sobre a tarifa base acrescida do valor da bandeira.
* **Interface Colorida (ANSI):** Exibe o nome da bandeira tarifária formatado em cores dinâmicas no terminal (Verde, Amarelo ou Vermelho) para melhor experiência visual.
* **Resiliência e Fallback:** Possui tratamento de contexto SSL e fallback automatizado: caso ocorra queda de conexão, CEP inexistente ou falha na API, o sistema assume uma tarifa padrão (R$ 0,75/kWh) e bandeira Amarela sem interromper a execução.

### 🍃 2. Versão Simples (`app_simples.py`)
Focada em leveza, velocidade de execução e independência de rede.
* **Execução 100% Offline:** Não realiza nenhuma chamada HTTP/API, garantindo funcionamento instantâneo em qualquer máquina sem internet.
* **Dicionário Interno de Tarifas:** Consulta a tarifa do estado através de um mapeamento interno por sigla de UF (com cobertura para os 26 estados + DF).
* **Interface Direta:** Apresentação em formato de texto padrão de terminal, mantendo o consumo de recursos minimalista.
* **Entrada por UF:** O usuário digita diretamente a sigla do seu Estado (ex.: `SP`, `RJ`, `MG`).

---

### 📊 Tabela Comparativa

| Recurso / Funcionalidade | Versão Avançada (`app.py`) | Versão Simples (`app_simples.py`) |
| :--- | :---: | :---: |
| **Entrada de Localização** | CEP de 8 dígitos | Sigla do Estado (UF) |
| **Consulta de UF / Cidade** | Automática via API ViaCEP | Manual via Dicionário |
| **Bandeira Tarifária** | Dinâmica via JSON online | Padrão / Estática |
| **Cálculo de Impostos** | Sim (Fator 1.22) | Não (Apenas Tarifa Base) |
| **Destaque Visual** | Cores ANSI no terminal | Texto padrão |
| **Dependência de Internet** | Sim (com suporte a fallback) | Não (100% Offline) |
| **Tratamento de SSL/Rede** | Implementado | Não aplicável |

---

## 📐 Fórmulas Utilizadas

### 1. Consumo Mensal (kWh)
**Consumo Mensal (kWh)** = [Potência (W) × Horas/Dia × 30] / 1000

### 2. Tarifa Final com Impostos (R$/kWh) — *Aplicado no `app.py`*
**Tarifa Final** = (Tarifa Base UF + Adicional Bandeira) × 1,22

### 3. Custo Estimado Mensal (R$)
**Custo Estimado (R$)** = Consumo Mensal (kWh) × Tarifa Final (R$/kWh)

---

## ✨ Funcionalidades e Validações do Sistema

Ambas as versões contam com mecanismos avançados de tratamento de entradas de dados:

* **Validação de Números:** Impede a digitação de textos ou caracteres especiais onde são esperados valores numéricos.
* **Trava de Limite Diário (24h):** O tempo de uso diário é limitado a no máximo **24 horas**. Se o usuário digitar um valor superior, o sistema rejeita a entrada e exibe a mensagem:  
  `❌ Tempo inválido! O dia possui no máximo 24 horas.`
* **Validação Estrita do Menu Final:** A confirmação para continuar ou sair do programa aceita estritamente as entradas **'S'** ou **'N'**. Respostas como "Sim", "Não" ou números disparam mensagem de erro e repetem a pergunta.
* **Ajuste de CEP Automático:** A versão avançada aceita CEPs digitados sem o zero inicial, corrigindo automaticamente o formato para 8 dígitos (`zfill(8)`).

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3
* **Módulos Nativos do Python:** 
  * `json`: Leitura e decodificação de dados estruturados em JSON.
  * `urllib.request`: Realização de requisições HTTP para APIs externas.
  * `ssl`: Criação de contextos seguros para conexões HTTPS no Windows/Linux.

---

## 🚀 Como Executar o Programa

### Pré-requisitos
* Python 3 instalado no computador.
* Git instalado para clonagem do repositório.

### Passo a Passo

1. **Clone este repositório:**
   ```bash
   git clone [https://github.com/matheusaafranco-cpu/consumo-energia.git](https://github.com/matheusaafranco-cpu/consumo-energia.git)