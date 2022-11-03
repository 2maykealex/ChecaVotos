from tseFunctions import TseFunctions
tse = TseFunctions()

ufs = ['ac', 'al','ap','am','ba','ce','df','es','zz','go','ma','mt','ms','mg','pr','pb','pa','pe','pi','rj','rn','rs','ro','rr','sc','se','sp','to',]
turnosUrls = ['https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e544;uf=ESTADO/dados-de-urna/boletim-de-urna',
              'https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e545;uf=ESTADO/dados-de-urna/boletim-de-urna']

for t, turnoUrl in enumerate(turnosUrls):
    for uf in ufs:
        print('\n---- {} TURNO ----'.format(t+1))
        url = turnoUrl.replace('=ESTADO/', '={}/'.format(uf))
        tse.acessTse(url)
        tse.selecionaLocal()
        print('botao')