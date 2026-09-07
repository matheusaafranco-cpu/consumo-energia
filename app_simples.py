# ==============================================================================
# 1. FUNÇÕES AUXILIARES E TRATAMENTO DE ENTRADAS
# ==============================================================================
def obter_numero_valido(mensagem, limite_max=None):
    """Garante que o usuário digite apenas números positivos e respeite limites."""
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
# 2. LÓGICA PRINCIPAL DO CÁLCULO DE CONSUMO
# ==============================================================================
def calcular_consumo_simples():
    """Executa a entrada de dados, consulta de tarifa e exibição dos resultados."""
    tarifas_estados = {
        'AC': 0.82, 'AL': 0.85, 'AM': 0.83, 'AP': 0.72, 'BA': 0.80,
        'CE': 0.79, 'DF': 0.73, 'ES': 0.74, 'GO': 0.75, 'MA': 0.77,
        'MG': 0.81, 'MS': 0.84, 'MT': 0.82, 'PA': 0.88, 'PB': 0.76,
        'PE': 0.78, 'PI': 0.80, 'PR': 0.70, 'RJ': 0.86, 'RN': 0.77,
        'RO': 0.79, 'RR': 0.68, 'RS': 0.72, 'SC': 0.65, 'SE': 0.78,
        'SP': 0.74, 'TO': 0.83
    }

    print("\n" + "-" * 60)
    aparelho = input("Nome do aparelho (ex.: Geladeira): ").strip() or "Aparelho"
    potencia = obter_numero_valido("Potência em Watts (W): ")
    horas_dia = obter_numero_valido("Uso diário em horas: ", limite_max=24)
    uf = input("Digite a sigla do Estado (ex.: SP, RJ, MG): ").strip().upper()

    tarifa = tarifas_estados.get(uf, 0.75)
    consumo_mensal = (potencia * horas_dia * 30) / 1000
    custo_estimado = consumo_mensal * tarifa

    print("\n" + "=" * 60)
    print(f"Aparelho: {aparelho}")
    print(f"Estado (UF): {uf}")
    print(f"Consumo estimado: {consumo_mensal:.2f} kWh/mês")
    print(f"Custo estimado: R$ {custo_estimado:.2f}/mês (Tarifa base: R$ {tarifa:.2f}/kWh)")
    print("=" * 60)

# ==============================================================================
# 3. INTERFACE DE EXECUÇÃO E LAÇO DE REPETIÇÃO
# ==============================================================================
def main():
    print("=" * 60)
    print("⚡ CALCULADORA DE CONSUMO ELÉTRICO (VERSÃO SIMPLES) ⚡")
    print("=" * 60)

    while True:
        calcular_consumo_simples()
        
        # Validação da resposta de continuação (Apenas S ou N)
        while True:
            continuar = input("\nDeseja calcular o consumo de outro aparelho? (S/N): ").strip().upper()
            if continuar in ['S', 'N']:
                break
            print("❌ Resposta inválida! Digite apenas 'S' para Sim ou 'N' para Não.")

        if continuar == 'N':
            print("\n👋 Obrigado por utilizar a Calculadora de Consumo Elétrico! Até logo.\n")
            break

# ==============================================================================
# 4. PONTO DE ENTRADA DO SCRIPT
# ==============================================================================
if __name__ == "__main__":
    main()