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

# ================= GERAÇÃO =================
def gerarArquivo(nome_arq, qtd):
    arq = open(nome_arq, 'w', encoding='utf-8')

    for i in range(qtd):
        arq.write(montarLog(i) + '\n')

    arq.close()
    print('Logs gerados!')

def montarLog(i):
    return f'[{gerarData(i)}] {gerarIp(i)} - {gerarMetodo()} - {gerarStatus(i)} - {gerarRecurso(i)} - {gerarTempo(i)}ms - {gerarTamanho()}B - {gerarProtocolo()} - {gerarAgente(i)} - /home'

def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds=i * 10)
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')

def gerarIp(i):
    if 20 <= i <= 50:
        return '203.120.45.7'

    r = random.randint(1,6)
    if r == 1: return '192.168.12.1'
    if r == 2: return '192.168.12.3'
    if r == 3: return '192.100.12.3'
    if r == 4: return '192.168.162.3'
    if r == 5: return '192.168.23.3'
    return '192.168.0.3'

def gerarMetodo():
    r = random.randint(1, 7)
    if r == 1: return 'GET'
    if r == 2: return 'POST'
    if r == 3: return 'PUT'
    if r == 4: return 'PATCH'
    if r == 5: return 'DELETE'
    if r == 6: return 'HEAD'
    return 'OPTIONS'

def gerarRecurso(i):
    if 10 <= i <= 20:
        return '/login'
    if i % 15 == 0:
        return '/admin'
    if i % 7 == 0:
        return '/backup'
    return '/home'

def gerarStatus(i):
    if 10 <= i <= 20:
        return 403
    if random.randint(1, 25) == 1:
        return 500
    if i % 12 == 0:
        return 404
    return 200

def gerarTempo(i):
    if 30 <= i <= 40:
        return 100 + i * 20
    return random.randint(50, 500)

def gerarTamanho():
    return random.randint(200, 2000)

def gerarProtocolo():
    r = random.randint(0, 2)
    if r == 0: return 'HTTP/1.0'
    if r == 1: return 'HTTP/1.1'
    return 'HTTP/2.0'

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

    total = sucesso = erro = erro500 = 0
    status200 = status403 = status404 = status500 = 0

    somaTempo = 0
    maiorTempo = 0
    menorTempo = 1000000

    rapido = normal = lento = 0

    tempoAnterior = -1
    contAumento = 0
    degradacao = 0

    contLogin403 = 0
    forcaBruta = 0
    ultimoIPForca = ''

    cont500 = 0
    falhaCritica = 0

    ultimoIP = ''
    contIP = 0
    bot = 0
    ultimoBot = ''

    rotas = rotasErro = 0
    adminErro = 0

    home = login = admin = backup = 0

    # IP MAIS ATIVO
    ip1 = ip2 = ip3 = ip4 = ip5 = ip6 = ''
    c1 = c2 = c3 = c4 = c5 = c6 = 0

    # IP COM MAIS ERROS
    e1 = e2 = e3 = e4 = e5 = e6 = 0

    linha = arq.readline()

    while linha != '':
        if linha == '\n':
            linha = arq.readline()
            continue

        total += 1
        i = 0

        while linha[i] != ']': i += 1
        i += 2

        ip = ''
        while linha[i] != ' ':
            ip += linha[i]
            i += 1
        i += 3

        # CONTAR IP
        if ip == ip1: c1 += 1
        elif ip == ip2: c2 += 1
        elif ip == ip3: c3 += 1
        elif ip == ip4: c4 += 1
        elif ip == ip5: c5 += 1
        elif ip == ip6: c6 += 1
        elif ip1 == '': ip1 = ip; c1 = 1
        elif ip2 == '': ip2 = ip; c2 = 1
        elif ip3 == '': ip3 = ip; c3 = 1
        elif ip4 == '': ip4 = ip; c4 = 1
        elif ip5 == '': ip5 = ip; c5 = 1
        elif ip6 == '': ip6 = ip; c6 = 1

        while linha[i] != ' ': i += 1
        i += 3

        status_txt = ''
        while linha[i] != ' ':
            status_txt += linha[i]
            i += 1
        status = int(status_txt)
        i += 3

        recurso = ''
        while linha[i] != ' ':
            recurso += linha[i]
            i += 1
        i += 3

        tempo_txt = ''
        while linha[i] != 'm':
            tempo_txt += linha[i]
            i += 1
        tempo = int(tempo_txt)

        somaTempo += tempo
        if tempo > maiorTempo: maiorTempo = tempo
        if tempo < menorTempo: menorTempo = tempo

        if tempo < 200: rapido += 1
        elif tempo < 800: normal += 1
        else: lento += 1

        # DEGRADAÇÃO
        if tempoAnterior != -1:
            if tempo > tempoAnterior:
                contAumento += 1
                if contAumento == 3:
                    degradacao += 1
            else:
                contAumento = 0
        tempoAnterior = tempo

        # STATUS
        if status == 200:
            sucesso += 1
            status200 += 1
        elif status == 403:
            status403 += 1
            erro += 1
        elif status == 404:
            status404 += 1
            erro += 1
        elif status == 500:
            status500 += 1
            erro += 1
            erro500 += 1

        # ERRO POR IP
        if status != 200:
            if ip == ip1: e1 += 1
            elif ip == ip2: e2 += 1
            elif ip == ip3: e3 += 1
            elif ip == ip4: e4 += 1
            elif ip == ip5: e5 += 1
            elif ip == ip6: e6 += 1

        # FORÇA BRUTA
        if recurso == '/login' and status == 403:
            contLogin403 += 1
            if contLogin403 == 3:
                forcaBruta += 1
                ultimoIPForca = ip
        else:
            contLogin403 = 0

        # FALHA CRÍTICA
        if status == 500:
            cont500 += 1
            if cont500 == 3:
                falhaCritica += 1
        else:
            cont500 = 0

        # BOT
        if ip == ultimoIP:
            contIP += 1
            if contIP == 5:
                bot += 1
                ultimoBot = ip
        else:
            ultimoIP = ip
            contIP = 1

        # ROTAS
        if recurso == '/admin' or recurso == '/backup':
            rotas += 1
            if status != 200:
                rotasErro += 1

        if recurso == '/admin' and status != 200:
            adminErro += 1

        # RECURSOS
        if recurso == '/home': home += 1
        if recurso == '/login': login += 1
        if recurso == '/admin': admin += 1
        if recurso == '/backup': backup += 1

        linha = arq.readline()

    arq.close()

    disponibilidade = (sucesso / total) * 100
    taxaErro = (erro / total) * 100
    mediaTempo = somaTempo / total

    # RECURSO MAIS ACESSADO
    recursoMais = '/home'
    maior = home
    if login > maior: recursoMais = '/login'; maior = login
    if admin > maior: recursoMais = '/admin'; maior = admin
    if backup > maior: recursoMais = '/backup'

    # IP MAIS ATIVO
    ipMaisAtivo = ip1
    maior = c1
    if c2 > maior: ipMaisAtivo = ip2; maior = c2
    if c3 > maior: ipMaisAtivo = ip3; maior = c3
    if c4 > maior: ipMaisAtivo = ip4; maior = c4
    if c5 > maior: ipMaisAtivo = ip5; maior = c5
    if c6 > maior: ipMaisAtivo = ip6

    # IP COM MAIS ERROS
    ipMaisErro = ip1
    maiorErro = e1
    if e2 > maiorErro: ipMaisErro = ip2; maiorErro = e2
    if e3 > maiorErro: ipMaisErro = ip3; maiorErro = e3
    if e4 > maiorErro: ipMaisErro = ip4; maiorErro = e4
    if e5 > maiorErro: ipMaisErro = ip5; maiorErro = e5
    if e6 > maiorErro: ipMaisErro = ip6

    # ESTADO
    if falhaCritica > 0 or disponibilidade < 70:
        estado = 'CRITICO'
    elif disponibilidade < 85 or lento > (total * 0.3):
        estado = 'INSTAVEL'
    elif disponibilidade < 95 or bot > 0:
        estado = 'ATENCAO'
    else:
        estado = 'SAUDAVEL'

    # RELATÓRIO
    print('\n===== RELATÓRIO =====')
    print('Total:', total)
    print('Sucesso:', sucesso)
    print('Erros:', erro)
    print('Erros críticos:', erro500)
    print(f'Disponibilidade: {disponibilidade:.3f}%')
    print(f'Taxa de erro: {taxaErro:.3f}%')
    print(f'Tempo médio: {mediaTempo:.3f}')
    print('Maior tempo:', maiorTempo)
    print('Menor tempo:', menorTempo)
    print('Rápidos:', rapido)
    print('Normais:', normal)
    print('Lentos:', lento)
    print('Status 200:', status200)
    print('Status 403:', status403)
    print('Status 404:', status404)
    print('Status 500:', status500)
    print('Recurso mais acessado:', recursoMais)
    print('IP mais ativo:', ipMaisAtivo)
    print('IP com mais erros:', ipMaisErro)
    print('Força bruta:', forcaBruta)
    print('Último IP força bruta:', ultimoIPForca)
    print('Acessos indevidos /admin:', adminErro)
    print('Eventos de degradação:', degradacao)
    print('Falha crítica:', falhaCritica)
    print('Bots:', bot)
    print('Último bot:', ultimoBot)
    print('Rotas sensíveis:', rotas)
    print('Falhas rotas sensíveis:', rotasErro)
    print('Estado:', estado)

# ================= EXECUÇÃO =================
menu()
