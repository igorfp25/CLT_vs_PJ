# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 21:17:59 2021

@author: Igorferr

Este arquivo contém as funções que calculam os descontos e benfícios de um empregado CLT.
As aliquotas e faixas devem ser ajustadas de acordo com eventuais alterações da legislação trabalhista.
"""


# ---------------CÁLCULO INSS-------------------------------------#
def INSS(salarioMensal: float) -> float:
    """
    Calcula INSS para 2021
    :param salarioMensal: 
    :return: valorINSS
    """
    # alíquotas : valor máximo da faixa salarial
    AliquotasFaixas = {0.075: 1100.00,  # 7.5%
                       0.09: 2203.48,  # 9%
                       0.12: 3305.22,  # 12%
                       0.14: 6433.57}  # 14%

    Base = 0  # valor base de cada faixa
    valorINSS = 0  # valor a ser calculado

    for Aliquota, Faixa in AliquotasFaixas.items():
        Limite = min(salarioMensal, Faixa)  # Valor limite para o cálculo do INSS dentro de cada faixa
        Delta = max(Limite - Base, 0)  # O valor tributável dentro de cada faixa
        valorINSS += Delta * Aliquota  # Valor tributável x Aliquota da faixa
        Base = Faixa  # Define a base da proxima faixa como o fim da faixa anterior

    valorINSS = round(valorINSS, 2)

    return valorINSS


# ----------------------------------------------------------------#

# ---------------CÁLCULO IRPF-------------------------------------#
def IR_Mensal(salarioBase: float, numeroDependentes=0) -> float:
    """
    Calcula Imposto de Renda para 2021
    :param salarioBase: (já aplicado desconto de INSS)
    :return: valorIR
    """

    # Início Faixa Salarial : [Aliquota de imposto, Valor a deduzir]
    # Deve estar em ordem decrescente
    FaixasIR = {4664.68: [0.275, 869.36],  # 27.5%
                3751.05: [0.225, 636.13],  # 22.5%
                2826.65: [0.15, 354.80],  # 15%
                1903.98: [0.075, 142.80],  # 7.5%
                0: [0, 0]}  # Isento
    DeducaoPorDependente = 189.59  # Valor a deduzir por dependentes

    valorIR = 0
    salarioBase -= (DeducaoPorDependente * numeroDependentes)  # Desconto para dependentes
    salarioBase = max(salarioBase, 0)  # caso seja negativo, considerar como zero

    for faixa, aliquotas in FaixasIR.items():
        if salarioBase > faixa:
            valorIR = salarioBase * aliquotas[0] - aliquotas[1]
            break

    valorIR = round(valorIR, 2)
    return valorIR


# ----------------------------------------------------------------#

# ---------------CÁLCULO IRPF SIMPLIFICADO------------------------#
def IR_Mensal_Simplificado(salarioBruto: float) -> float:
    """
    Calcula Imposto de Renda para 2021
    :param salarioBruto: (sem desconto)
    :return: valorIRSimp
    """

    # Início Faixa Salarial : [Aliquota de imposto, Valor a deduzir]
    FaixasIR = {4664.68: [0.275, 869.36],  # 27.5%
                3751.05: [0.225, 636.13],  # 22.5%
                2826.65: [0.15, 354.80],  # 15%
                1903.98: [0.075, 142.80],  # 7.5%
                0: [0, 0]}  # Isento

    valorIRSimp = 0

    salarioBase = salarioBruto * (1 - 0.2)  # Desconto de 20% sobre o valor tributável

    for faixa, aliquotas in FaixasIR.items():
        if salarioBase > faixa:
            valorIRSimp = salarioBase * aliquotas[0] - aliquotas[1]
            break

    valorIRSimp = round(valorIRSimp, 2)

    return valorIRSimp


# ----------------------------------------------------------------#

# ---------------CÁLCULO FGTS-------------------------------------#
def FGTS(salarioBruto: float, numeroDeMeses: int = 12, incluirMulta: bool = False,
         incluirRendimento: bool = False) -> float:
    """
    Calcula o valor do FGTS recebido durante determinado periodo de tempo.
    É possível selecionar se deseja incluir os valor dos rendimentos ou somente os aportes.
    Está incluso o recebimento do FGTS referente às duas parcelas do 13o salário (a primeira no mês 6 e a segunda no mês 11)
    Também está incluso o recebimento do FGTS referente à 1/3 de Férias
    :param salarioBruto, numeroDeMeses, incluirMulta, incluirRendimento
    :return: saldoFGTS
    """

    RendimentoAnual = 0.03  # Rendimento FGTS 3% a.a

    # Incluir rendimento do FGTS no cálculo?
    if incluirRendimento:
        RendimentoMensal = pow(1 + RendimentoAnual, 1 / 12) - 1  # Cálculo do rendimento mensal
    else:
        RendimentoMensal = 0

    AportesMensais = salarioBruto * 0.08  # Valor depositado na conta do FGTS mensalmente
    saldoFGTS = 0  # Saldo inicial

    for mes in range(numeroDeMeses):
        if mes == 6:  # Primeira Parcela do 13o Salário (data aproximada)
            saldoFGTS = saldoFGTS * (1 + RendimentoMensal) + 1.5 * AportesMensais
        elif mes == 11:  # Segunda Parcela do 13o Salário + 1/3 de Ferias
            saldoFGTS = saldoFGTS * (1 + RendimentoMensal) + 1.8 * AportesMensais
        else:
            saldoFGTS = saldoFGTS * (1 + RendimentoMensal) + AportesMensais

    if incluirMulta:
        saldoFGTS += AportesMensais * numeroDeMeses * 0.4  # 40% de multa por demissão sem justa causa

    saldoFGTS = round(saldoFGTS, 2)
    return saldoFGTS


# ----------------------------------------------------------------#

# ---------------CÁLCULO SALÁRIO FÉRIAS---------------------------#
def Salario_Ferias_Bruto(salarioMensal: float) -> float:
    """
    Calcula Salário de Férias Bruto
    :param salarioMensal:
    :return: salarioFeriasBruto
    """
    salarioFeriasBruto = salarioMensal * (1 + 1 / 3)

    salarioFeriasBruto = round(salarioFeriasBruto, 2)
    return salarioFeriasBruto

# ----------------------------------------------------------------#

# ---------------IRPF SOBRE PLR (Anual)---------------------------#
def IR_PLR(plr: float) -> float:
    """
    Calcula o Imposto de Renda sobre a PLR ou Bonus Anual
    :param plr:
    :return: valorIRPLR
    """
    PLRFaixasIR = {16380.38: [0.275, 3051.53],  # 27.5%
                   13167.01: [0.225, 2232.51],  # 22.5%
                   9922.29: [0.15, 1244.99],  # 15%
                   6677.56: [0.075, 500.82],  # 7.5%
                   0: [0, 0]}  # Isento

    valorIRPLR = 0

    for faixa, aliquotas in PLRFaixasIR.items():
        if plr > faixa:
            valorIRPLR = plr * aliquotas[0] - aliquotas[1]
            break

    valorIRPLR = round(valorIRPLR, 2)

    return valorIRPLR

# ----------------------------------------------------------------#