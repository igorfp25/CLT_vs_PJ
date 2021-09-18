# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 18:10:59 2021

@author: Igorferr

Este arquivo contém as funções que calculam os descontos/impostos para PJ enquadrado na categoria Simples Nacional .
As aliquotas e faixas devem ser ajustadas de acordo com eventuais alterações da legislação trabalhista.
"""

# ---------------CÁLCULO Pro-Labore COM Base no Fator R ----------#
def ProLabore_FatorR(receitaBruta: float, fatorR: float) -> float:
    """
    Calcula o valor do Pro-Labore com baseno fator R desejado
    :param: receitaBruta , fatorR
    :return: proLabore
    """

    proLabore = receitaBruta * fatorR

    proLabore = round(proLabore, 2)
    return proLabore


# ----------------------------------------------------------------#

# ---------------CÁLCULO DAS Simples Nacional Anexo III----------#
def DAS_SimplesNacionalIII(faturamentoAnual: float) -> float:
    """
    Calcula o total de imposto da DAS par Pessoa Física sob o regime do Simples Nacional, referente ao anexo III.
    Tabela de 2021
    :param faturamentoAnual:
    :return: valorDASSimples
    """

    LimiteSimplesNacional = 4800000.00  # Limite do faturamento anual para enquadramento no Simples Nacional.
    if faturamentoAnual > LimiteSimplesNacional:  # Verifica se o valor do Faturamento informado está dentro do limite pérmitido.
        raise ValueError("O faturamento anual informado não é válido. "
                         "O valor está acima do limite para enquadramento no Simples Nacional.")

    # Início Faixa Salarial : [Aliquota de imposto, Valor a deduzir]
    # Deve estar em ordem decrescente
    FaixasDASSimplesIII = {3600000.00: [0.33, 648000.00],  # 33%
                           1800000.00: [0.21, 125640.00],  # 21%
                           720000.00: [0.16, 35640.00],  # 16%
                           360000.00: [0.135, 17640.00],  # 13.5%
                           180000.00: [0.112, 9360.00],  # 11.2%
                           0: [0.06, 0]}  # 6.0%

    valorDASSimples = 0

    for faixa, aliquotas in FaixasDASSimplesIII.items():
        if faturamentoAnual > faixa:
            valorDASSimples = faturamentoAnual * aliquotas[0] - aliquotas[1]
            break

    valorDASSimples = round(valorDASSimples, 2)
    return valorDASSimples


# ----------------------------------------------------------------#
