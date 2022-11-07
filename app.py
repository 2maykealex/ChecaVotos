from tseFunctions import TseFunctions
tse = TseFunctions()

ufs = ['ac', 'al','ap','am','ba','ce','df','es','zz','go','ma','mt','ms','mg','pr','pb','pa','pe','pi','rj','rn','rs','ro','rr','sc','se','sp','to',]
turnosUrls = ['https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e544;uf=ESTADO/dados-de-urna/boletim-de-urna',
              'https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e545;uf=ESTADO/dados-de-urna/boletim-de-urna']

turnos=['e544', 'e544']

for t, turnoUrl in enumerate(turnosUrls):
    if (t == 0): #pular para o segunto turno
        continue

    for uf in ufs:
        print('\n---- {} TURNO ----'.format(t+1))
        url = turnoUrl.replace('=ESTADO/', '={}/'.format(uf))
        tse.acessTse(url)
        tse.uf_atual = '{}'.format(uf)
        tse.turno_atual = '{}'.format(turnos[t])
        tse.selecionaLocal()
        print('botao')