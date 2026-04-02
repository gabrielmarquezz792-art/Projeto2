import random
import datetime

def menu():
    nome_arq = 'log.txt'
    while True:
        print('MENU\n')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - gerar e Analisar logs')
        print('4 - SAIR')
        opc = int(input('Escolha uma opção: '))
        if opc == 1:
            try:
                qtd = int(input('Quantidade de logs (registros): '))
                gerarArquivo(nome_arq, qtd)
            except:
                print('Entrada inválida.')
        elif opc ==2:
            analisarLogs(nome_arq)
        elif opc == 3:
            try:
                qtd = int(input('Quantidade de logs (registros): '))
                gerarArquivo(nome_arq, qtd)
                analisarLogs(nome_arq)
            except:
                print('Entrada inválida.')
        elif opc == 4:
            print('Até mais')
            break
        else:
            print('Opção inválida')

def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w', encoding='UTF-8') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
    print('Log gerado')

def montarLog(i):
    data = gerarData(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    protocolo = gerarProtocolo(i)
    tamanho = gerarTamanho(i)
    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho} - {protocolo} - {agente} - /home'

def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds= i * random.randint(5,20) )
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')

def gerarIp(i):
    r = random.randint(1,6)
    if i >= 20 and i <= 50:
        return '203.120.45.7'
    
    if r == 1:
        return '192.168.12.1'
    if r == 2:
        return '192.168.12.3'
    if r == 3:
        return '192.100.12.3'
    if r == 4:
        return '192.168.162.3'
    if r == 5:
        return '192.168.23.3'
    if r == 6:
        return '192.168.0.3'
    