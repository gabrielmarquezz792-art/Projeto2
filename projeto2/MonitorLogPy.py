import random
import datetime

# ================= MENU =================
def menu():
    nome_arq = 'log.txt'
    while True:
        print('\nMENU')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e analisar')
        print('4 - SAIR')

        try:
            opc = int(input('Escolha: '))
        except:
            print('Entrada inválida')
            continue

        if opc == 1:
            qtd = int(input('Quantidade: '))
            gerarArquivo(nome_arq, qtd)

        elif opc == 2:
            analisarLogs(nome_arq)

        elif opc == 3:
            qtd = int(input('Quantidade: '))
            gerarArquivo(nome_arq, qtd)
            analisarLogs(nome_arq)

        elif opc == 4:
            print('Encerrado')
            break
        else:
            print('Opção inválida')


# ================= GERAÇÃO DE LOGS =================
def gerarArquivo(nome_arq, qtd):
    arq = open(nome_arq, 'w', encoding='utf-8')

    for i in range(qtd):
        arq.write(montarLog(i) + '\n')

    arq.close()
    print('Logs gerados!')


def montarLog(i):
    return f'[{gerarData(i)}] {gerarIp(i)} - {gerarMetodo()} - {gerarStatus(i)} - {gerarRecurso(i)} - {gerarTempo(i)}ms - {gerarTamanho()}B - HTTP/1.1 - {gerarAgente(i)} - /home'


def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds=i * 10)
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')


# IP fixo para gerar comportamento suspeito
def gerarIp(i):
    if 20 <= i <= 60:
        return '203.120.45.7'
    return f'192.168.0.{random.randint(1, 20)}'


def gerarMetodo():
    if random.randint(0, 1) == 0:
        return 'GET'
    return 'POST'


# gera rotas (inclui /login para força bruta)
def gerarRecurso(i):
    if 10 <= i <= 20:
        return '/login'
    if i % 15 == 0:
        return '/admin'
    if i % 7 == 0:
        return '/backup'
    return '/home'


# gera status (inclui padrões de erro)
def gerarStatus(i):
    if 10 <= i <= 20:
        return 403  # força bruta
    if 70 <= i <= 72:
        return 500  # falha crítica
    if i % 12 == 0:
        return 404
    return 200


# gera tempo (inclui lentidão)
def gerarTempo(i):
    if 30 <= i <= 40:
        return 900 + i * 10  # lento
    return random.randint(50, 500)


def gerarTamanho():
    return random.randint(200, 2000)


def gerarAgente(i):
    if i % 20 == 0:
        return 'GoogleBot'
    return 'Chrome'


# ================= ANÁLISE =================
def analisarLogs(nome_arq):
    try:
        arq = open(nome_arq, 'r', encoding='utf-8')
    except:
        print('Arquivo não encontrado')
        return

    # ===== CONTADORES GERAIS =====
    total = 0
    sucesso = 0
    erro = 0
    erro500 = 0

    somaTempo = 0
    maiorTempo = 0
    menorTempo = 999999

    rapido = 0
    normal = 0
    lento = 0

    # ===== DEGRADAÇÃO =====
    contLentoSeq = 0   # quantos lentos seguidos
    degradacao = 0     # eventos de degradação

    # ===== FORÇA BRUTA =====
    contLogin403 = 0
    forcaBruta = 0
    ultimoIPForca = ''

    # ===== FALHA CRÍTICA =====
    cont500 = 0
    falhaCritica = 0

    # ===== BOT =====
    ultimoIP = ''
    contIP = 0
    bot = 0
    ultimoBot = ''

    # ===== ROTAS =====
    rotas = 0
    rotasErro = 0

    linha = arq.readline()

    while linha != '':
        if linha == '\n':
            linha = arq.readline()
            continue

        total += 1
        i = 0

        # ===== PULAR DATA =====
        while linha[i] != ']':
            i += 1
        i += 2

        # ===== IP =====
        ip = ''
        while linha[i] != ' ':
            ip += linha[i]
            i += 1
        i += 3

        # ===== PULAR MÉTODO =====
        while linha[i] != ' ':
            i += 1
        i += 3

        # ===== STATUS =====
        status_txt = ''
        while linha[i] != ' ':
            status_txt += linha[i]
            i += 1
        status = int(status_txt)
        i += 3

        # ===== RECURSO =====
        recurso = ''
        while linha[i] != ' ':
            recurso += linha[i]
            i += 1
        i += 3

        # ===== TEMPO =====
        tempo_txt = ''
        while linha[i] != 'm':
            tempo_txt += linha[i]
            i += 1
        tempo = int(tempo_txt)

        # ===== TEMPO / PERFORMANCE =====
        somaTempo += tempo

        if tempo > maiorTempo:
            maiorTempo = tempo
        if tempo < menorTempo:
            menorTempo = tempo

        if tempo < 200:
            rapido += 1
            contLentoSeq = 0
        elif tempo < 800:
            normal += 1
            contLentoSeq = 0
        else:
            lento += 1
            contLentoSeq += 1

            # evento de degradação = 3 lentos seguidos
            if contLentoSeq == 3:
                degradacao += 1

        # ===== STATUS =====
        if status == 200:
            sucesso += 1
        else:
            erro += 1

        if status == 500:
            erro500 += 1

        # ===== FORÇA BRUTA =====
        if recurso == '/login' and status == 403:
            contLogin403 += 1
            if contLogin403 == 3:
                forcaBruta += 1
                ultimoIPForca = ip
        else:
            contLogin403 = 0

        # ===== FALHA CRÍTICA =====
        if status == 500:
            cont500 += 1
            if cont500 == 3:
                falhaCritica += 1
        else:
            cont500 = 0

        # ===== BOT =====
        if ip == ultimoIP:
            contIP += 1
            if contIP == 5:
                bot += 1
                ultimoBot = ip
        else:
            ultimoIP = ip
            contIP = 1

        # ===== ROTAS SENSÍVEIS =====
        if recurso == '/admin' or recurso == '/backup':
            rotas += 1
            if status != 200:
                rotasErro += 1

        linha = arq.readline()

    arq.close()

    # ===== RESULTADOS =====
    disponibilidade = (sucesso / total) * 100
    mediaTempo = somaTempo / total

    if falhaCritica > 0 or disponibilidade < 70:
        estado = 'CRITICO'
    elif disponibilidade < 85:
        estado = 'INSTAVEL'
    elif disponibilidade < 95:
        estado = 'ATENCAO'
    else:
        estado = 'SAUDAVEL'

    # ===== RELATÓRIO =====
    print('\n===== RELATÓRIO =====')
    print('Total:', total)
    print('Sucesso:', sucesso)
    print('Erros:', erro)
    print('Erros 500:', erro500)
    print('Tempo médio:', mediaTempo)
    print('Maior tempo:', maiorTempo)
    print('Menor tempo:', menorTempo)
    print('Rápidos:', rapido)
    print('Normais:', normal)
    print('Lentos:', lento)
    print('Eventos de degradação:', degradacao)
    print('Força bruta:', forcaBruta)
    print('Último IP força bruta:', ultimoIPForca)
    print('Falha crítica:', falhaCritica)
    print('Bots:', bot)
    print('Último bot:', ultimoBot)
    print('Rotas sensíveis:', rotas)
    print('Falhas rotas:', rotasErro)
    print('Estado:', estado)


# ================= EXECUÇÃO =================
menu()  
