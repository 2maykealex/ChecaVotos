from tseFunctions import TseFunctions
from decouple import config

tse = TseFunctions()
turnos=['e544', 'e544']
ufs = ['ac', 'al','ap','am','ba','ce','df','es','zz','go','ma','mt','ms','mg','pr','pb','pa','pe','pi','rj','rn','rs','ro','rr','sc','se','sp','to',]
turnosUrls = ['https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e544;uf=ESTADO/dados-de-urna/boletim-de-urna',
              'https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e545;uf=ESTADO/dados-de-urna/boletim-de-urna']

estadosOk = (config('ESTADOS')).split(',')
municipio = int(config('MUNICIPIO'))
turno = config('TURNO')
try:
    turno = int(turno)
except:
    turno = 0

tse = TseFunctions()
tse.countCity = municipio

for t, turnoUrl in enumerate(turnosUrls):
    if (t != int(turno)):
        continue

    for uf in ufs:
        if uf in estadosOk:
            continue

        print('\n---- {} TURNO ----'.format(t+1))
        url = turnoUrl.replace('=ESTADO/', '={}/'.format(uf))
        tse.acessTse(url)
        tse.totCity  = 0
        tse.uf_atual = '{}'.format(uf)
        tse.turno_atual = '{}'.format(turnos[t])
        tse.selecionaLocal()