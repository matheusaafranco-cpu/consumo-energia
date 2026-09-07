import json
import urllib.request
import ssl

# ==============================================================================
# CÓDIGOS DE COR ANSI PARA O TERMINAL
# ==============================================================================
COR_VERDE = "\033[92m"
COR_AMARELA = "\033[93m"
COR_VERMELHA = "\033[91m"
COR_RESET = "\033[0m"

# ==============================================================================
# 1. INTEGRAÇÕES COM APIs EXTERNAS
# ==============================================================================

def formatar_bandeira_com_cor(nome_bandeira):
    """Aplica cores ANSI baseadas no nome da bandeira tarifária."""
    nome_lower = nome_bandeira.lower()
    
    if "verde" in nome_lower:
        return f"{COR_VERDE}{nome_bandeira}{COR_RESET}"
    elif "amarela" in nome_lower:
        return f"{COR_AMARELA}{nome_bandeira}{COR_RESET}"
    elif "vermelha" in nome_lower:
        return f"{COR_VERMELHA}{nome_bandeira}{COR_RESET}"
    
    return nome_bandeira


def consultar_api_cep(cep):
    """Obtém o Estado (UF) e Cidade a partir do CEP informado via API do ViaCEP."""
    cep_limpo = cep.replace("-", "").replace(".", "").strip().zfill(8)
    
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return None, None

    try:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        contexto_ssl = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, timeout=5, context=contexto_ssl) as resp:
            dados = json.loads(resp.read().decode('utf-8'))
            if dados.get("erro") is True:
                return None, None
            if "uf" in dados:
                return dados["uf"], dados.get("localidade", "Cidade")
    except Exception:
        pass

    return None, None


def consultar_bandeira_automatica():
    """Retorna a bandeira tarifária vigente e o valor adicional por kWh."""
    try:
        url = "https://raw.githubusercontent.com/muralis-tech/datasets/main/bandeira_vigente.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        contexto_ssl = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, timeout=3, context=contexto_ssl) as resp:
            dados = json.loads(resp.read().decode('utf-8'))
            return dados.get("bandeira", "Amarela"), float(dados.get("adicional", 0.01885))
    except Exception:
        pass

    return "Amarela", 0.01885


def consultar_api_tarifa(uf):
    """Retorna a tarifa base estimada (sem impostos) por Estado (UF)."""
    tarifas_locais = {
        'SP': 0.74, 'RJ': 0.86, 'MG': 0.81, 'RS': 0.72, 'PR': 0.70,
        'BA': 0.80, 'PE': 0.78, 'CE': 0.79, 'SC': 0.65, 'GO': 0.75
    }
    return tarifas_locais.get(uf, 0.75)

# ==============================================================================
# 2. FUNÇÕES AUXILIARES E VALIDAÇÃO DE ENTRADAS
# ==============================================================================

def obter_numero_valido(mensagem, limite_max=None):
    """Garante que o usuário digite apenas números válidos e respeite limites."""
    while True:
        try:
            valor = float(input(mensagem).replace(',', '.'))
            if valor < 0:
                print("❌ Digite um valor maior ou igual a zero.")
                continue
            if limite_max is not None and valor > limite_max:
                print(f"❌ Tempo inválido! O dia possui no máximo {limite_max} horas.")
                continue
            return valor
        except ValueError:
            print("❌ Entrada inválida! Digite apenas números.")

# ==============================================================================
# 3. LÓGICA PRINCIPAL DO CÁLCULO DE CONSUMO
# ==============================================================================

def calcular_consumo():
    """Executa a coleta de dados, requisições de API, cálculos e exibição."""
    print("\n" + "-" * 60)
    
    # --------------------------------------------------------------------------
    # 3.1. Entrada de Dados do Usuário
    # --------------------------------------------------------------------------
    aparelho = input("Nome do aparelho (ex.: Geladeira): ").strip() or "Aparelho"
    potencia = obter_numero_valido("Potência do aparelho em Watts (W): ")
    horas_dia = obter_numero_valido("Tempo médio de uso diário em horas: ", limite_max=24)
    cep = input("Digite o CEP para buscar a localização (ex.: 08710000): ").strip()

    # --------------------------------------------------------------------------
    # 3.2. Consulta e Processamento de Dados via API
    # --------------------------------------------------------------------------
    print("\n🔍 Consultando APIs de localização e bandeira tarifária...")
    uf, cidade = consultar_api_cep(cep)
    nome_bandeira, adicional_bandeira = consultar_bandeira_automatica()

    # Aplica a cor na bandeira
    bandeira_colorida = formatar_bandeira_com_cor(nome_bandeira)

    if uf:
        tarifa_base = consultar_api_tarifa(uf)
        fonte_dados = f"API ViaCEP ({cidade}/{uf}) | Bandeira: {bandeira_colorida}"
    else:
        tarifa_base = 0.75
        fonte_dados = f"CEP Não Encontrado | Bandeira: {bandeira_colorida}"

    # --------------------------------------------------------------------------
    # 3.3. Fórmulas de Consumo, Impostos e Custo
    # --------------------------------------------------------------------------
    fator_impostos = 1.22
    tarifa_final = (tarifa_base + adicional_bandeira) * fator_impostos

    consumo_mensal = (potencia * horas_dia * 30) / 1000
    custo_estimado = consumo_mensal * tarifa_final

    # --------------------------------------------------------------------------
    # 3.4. Exibição Formatada dos Resultados
    # --------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"Aparelho: {aparelho}")
    print(f"Fonte dos Dados: {fonte_dados}")
    print(f"Consumo estimado: {consumo_mensal:.2f} kWh/mês")
    print(f"Tarifa Base (UF): R$ {tarifa_base:.2f}/kWh")
    print(f"Custo estimado: R$ {custo_estimado:.2f}/mês (Tarifa Final c/ Impostos: R$ {tarifa_final:.2f}/kWh)")
    print("=" * 60)

# ==============================================================================
# 4. INTERFACE DE EXECUÇÃO E LAÇO DE REPETIÇÃO
# ==============================================================================

def main():
    print("=" * 60)
    print("⚡ CALCULADORA DE CONSUMO ELÉTRICO INTELIGENTE ⚡")
    print("=" * 60)

    while True:
        calcular_consumo()
        
        while True:
            continuar = input("\nDeseja calcular o consumo de outro aparelho? (S/N): ").strip().upper()
            if continuar in ['S', 'N']:
                break
            print("❌ Resposta inválida! Digite apenas 'S' para Sim ou 'N' para Não.")

        if continuar == 'N':
            print("\n👋 Obrigado por utilizar a Calculadora de Consumo Elétrico! Até logo.\n")
            break

# ==============================================================================
# 5. PONTO DE ENTRADA DO SCRIPT
# ==============================================================================

if __name__ == "__main__":
    main()