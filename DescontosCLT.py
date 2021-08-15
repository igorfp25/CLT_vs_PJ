# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 21:17:59 2021

@author: Igorferr

Este arquivo contém as funções que calculam os descontos de um empregado CLT
"""


# ---------------CÁLCULO INSS-------------------------------------#
def INSS_CLT(salarioMensal: float):
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
def IR_CLT(salarioBase: float, numeroDependentes=0):
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
def IR_Simplificado_CLT(salarioBruto: float):
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
