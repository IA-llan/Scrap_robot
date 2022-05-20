import time
import pyautogui
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from atividade_avaliativa import driver
from datetime import datetime


def arrecadacao_mensal(ano):
    global soap
    dict_valores = {}
    delay = 1
    mes = 1
    i = 0
    for i in range(3):
        nova_data = f'01/{mes}/{ano}'

        atualiza_data_inicio(nova_data)

        if mes == 12:
            data_final = f'01/01/{ano + 1}'
            atualiza_data_final(data_final)
        else:
            data_final = f'01/{mes + 1}/{ano}'
            atualiza_data_final(data_final)

        desfoca_atualiza()

        total_imposto = total_imposto_reais()
        imposto_numerico = total_imposto_numerico(total_imposto)
        data_mes = soup.find(id='counterDateEstado').text

        time.sleep(delay)

        dict_valores[f'{mes}/{ano}'] = round(float(imposto_numerico) / 1000000000, 2)

        print(data_mes, ":", total_imposto)

        mes += 1

    print(dict_valores)
    plot_graph(dict_valores.keys(), dict_valores.values(), ano, 0)


def delete_line(n):
    i = 0
    for i in range(n):
        pyautogui.press('delete')


def arrecadacao_total_mes(ano_inicio, ano_final):
    global soap
    anos = ano_final - ano_inicio
    mes = 1

    for j in range(anos-1):

        dict_valores = {}
        for i in range(12):
            nova_data = f'01/{mes}/{ano_inicio}'
            atualiza_data_inicio(nova_data)

            if mes == 12:
                data_final = f'01/01/{ano_inicio + 1}'
                atualiza_data_final(data_final)
                desfoca_atualiza()
                total_imposto = total_imposto_reais()
                imposto_numerico = total_imposto_numerico(total_imposto)
                data_mes = soup.find(id='counterDateEstado').text
                print(data_mes, ":", total_imposto)
                dict_valores[f'{mes}/{ano_inicio}'] = round(float(imposto_numerico) / 1000000000, 2)
                break
            else:
                data_final = f'01/{mes + 1}/{ano_inicio}'
                atualiza_data_final(data_final)

            desfoca_atualiza()

            total_imposto = total_imposto_reais()
            imposto_numerico = total_imposto_numerico(total_imposto)
            data_mes = soup.find(id='counterDateEstado').text

            print(data_mes, ":", total_imposto)

            dict_valores[f'{mes}/{ano_inicio}'] = round(float(imposto_numerico) / 1000000000, 2)
            mes += 1
        mes = 1
        plot_graph(dict_valores.keys(), dict_valores.values(), ano_inicio, j)
        ano_inicio += 1
        print(dict_valores)


def refresh_html():
    global soup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")


def plot_graph(x, y, ano, index):
    figura = plt.figure(index, figsize=(20, 3))
    plt.suptitle(f"Arrecadação anual {ano}")
    plt.ylabel("Valor arrecadado(Bilhões)")
    plt.xlabel("Meses")
    plt.scatter(x, y)
    plt.plot(x, y, label='Arrecadado')
    bars = plt.bar(x, y, width=0.5)
    for bar in bars:
        altura_barra = bar.get_height()
        plt.text(bar.get_x() + .15, altura_barra + 1.5, altura_barra, fontweight='bold', fontsize='x-large')
    plt.legend()

    figura.show()


def daily_check():
    global soap
    data_atual = datetime.today().strftime('%m-%d')
    dia = int(data_atual.split('-')[1])
    mes = int(data_atual.split('-')[0])
    dict_valores = {}

    for i in range(mes):
        data_inicial = f'01/{i + 1}/2022'
        atualiza_data_inicio(data_inicial)

        if i + 1 == mes:
            data_final = f'{dia}/{mes}/2022'
            atualiza_data_final(data_final)
            desfoca_atualiza()
            total_imposto = total_imposto_reais()
            imposto_numerico = total_imposto_numerico(total_imposto)
            data_mes = soup.find(id='counterDateEstado').text
            print(data_mes, ":", total_imposto)
            dict_valores[f'{dia}/{i + 1}/2022'] = round(float(imposto_numerico) / 1000000000, 2)
            break
        else:
            data_final = f'01/{i + 2}/2022'
            atualiza_data_final(data_final)

        desfoca_atualiza()

        total_imposto = total_imposto_reais()
        imposto_numerico = total_imposto_numerico(total_imposto)
        data_mes = soup.find(id='counterDateEstado').text
        print(data_mes, ":", total_imposto)
        dict_valores[f'{i + 1}/2022'] = round(float(imposto_numerico) / 1000000000, 2)

    print(dict_valores)
    plot_graph(dict_valores.keys(), dict_valores.values(), '2022', 0)


def atualiza_data_inicio(nova_data):
    driver.find_element_by_xpath('//*[@id="contadorestado_dataInicial"]').click()
    delete_line(10)
    pyautogui.write(nova_data)
    time.sleep(1)


def atualiza_data_final(final_data):
    driver.find_element_by_xpath('//*[@id="contadorestado_dataFinal"]').click()
    delete_line(10)
    pyautogui.write(final_data)
    time.sleep(1)


def total_imposto_reais() -> str:
    total_imposto = soup.find(id="counterUF").text
    total_imposto_formatado = total_imposto.replace("Bilhões", "R$").replace("Milhões", ".").replace("Mil",
                                                                                                     ".").replace(
        "Reais", ".").replace("Centavos", ",")
    return total_imposto_formatado


def total_imposto_numerico(total_imposto):
    imposto_numerico = total_imposto.replace("R$", "").replace(".", "").replace(",", ".")
    return imposto_numerico


def desfoca_atualiza():
    pyautogui.press('enter')
    driver.find_element_by_xpath('//*[@id="arrecadacaoEstados"]/div[2]/p').click()
    time.sleep(1)
    refresh_html()
    time.sleep(1)
