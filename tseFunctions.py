import pandas as pd
from time import sleep
from sys import exc_info
from decouple import config
from datetime import datetime
from selenium_functions import SeleniumFunctions
class TseFunctions(object):

    def __init__(self, webDriverNumero=1):
        self.selenium = SeleniumFunctions()
        self.waitInstance = self.selenium.waitInstance
        self.webDriverNumero = webDriverNumero
        self.By = self.selenium.By
        self.driver = None
        self.ufCounter = 1
        self.countState = 0
        self.countCity  = 0
        self.countZona  = 0
        self.countSecao = 1
        self.counter = 1
        self.counterGeral = 0
        self.cabecalho = []
        self.registros = {}

        self.turno_atual = ''
        self.uf_atual = ''
        self.cidade_atual = ''
        self.zona_atual = ''
        self.secao_atual = ''
        self.url_atual = ''

        self.zonas  = []
        self.secoes = []
        df = None

    def acessTse(self, url):
        try:
            if (not(self.driver)):
                modSilent= config('MODSILENT')
                self.driver = self.selenium.iniciaWebdriver(webDriverNumero = self.webDriverNumero, modSilent=modSilent)
                print('LOGIN REALIZADO NO INTEGRA')

            self.driver.get(url)
            return True

        except Exception as err:
            exception_type, exception_object, exception_traceback = exc_info()
            line_number = exception_traceback.tb_lineno
            print('---> ERRO NA LINHA {}: {} >>>'.format(line_number, err))
            return False

    def selecionaLocal(self):
        self.countCity  = 0
        print('=============== INICIANDO O ESTADO: {} ==============='.format(self.uf_atual.upper()))
        try:
            while True:
                try:
                    sleep(1)
                    self.driver.find_elements(self.By.CLASS_NAME, 'leading-tight')[1].click()
                    sleep(1)
                    cidades = self.driver.find_elements(self.By.TAG_NAME, 'mat-option')
                    cidades[self.countCity].click()

                    self.driver.find_element(self.By.CLASS_NAME, 'button-block').click()
                    self.obtemZonasSecoesCidade()
                    self.countZona = self.countZona + 1
                    self.obterDadosUrna()
                    self.countSecao = self.countSecao + 1
                    self.acessaViaUrl()

                    self.counter = 1
                    self.countZona = 0
                    self.countSecao = 1
                    self.countCity = self.countCity + 1
                    if (self.countCity > len(cidades)):
                        print('=============== ENCERRADO O ESTADO: {} ==============='.format(self.uf_atual.upper()))
                        self.countCity  = 0
                        break

                    now = datetime.now().strftime('%Y-%m-%d %H:%M')
                    now = now.replace(' ','__').replace('-','_').replace(':','_')
                    self.df.to_excel('logs\\{}-{}-{}.xlsx'.format(now, self.uf_atual.upper(), self.cidade_atual), index=False)
                except:
                    pass
        except:
            return False

    def obtemZonasSecoesCidade(self):
        while True:
            try:
                sleep(1)
                self.driver.find_elements(self.By.TAG_NAME, 'mat-form-field')[0].click()
                sleep(.2)
                zonas = self.driver.find_elements(self.By.CLASS_NAME, 'mat-active')
                for zona in zonas:
                    self.zonas.append('{}'.format(zona.text.replace('Zona ','')))
                self.zona_atual = zonas[self.countZona].text.replace('Zona ','')
                zonas[self.countZona].click()

                self.driver.find_elements(self.By.TAG_NAME, 'mat-form-field')[1].click()
                sleep(.2)
                secoes = self.driver.find_element(self.By.CLASS_NAME, 'cdk-overlay-container').find_elements(self.By.CLASS_NAME, 'mat-option')
                for secao in secoes:
                    if (secao.text.replace('Seção ','') == 'Seção'):
                        continue
                    self.secoes.append('{}'.format(secao.text.replace('Seção ','')))
                self.secao_atual = secoes[self.countSecao].text.replace('Seção ','')
                secoes[self.countSecao].click()

                self.driver.find_element(self.By.TAG_NAME, 'button').click() #botão pesquisa
                sleep(1)

                self.url_atual = self.driver.current_url
                break

            except:
                pass

    def acessaViaUrl(self):
        for zona in self.zonas:
            for secao in self.secoes:
                urlreal = ''
                urlreal = '{};zn={};se={}/dados-de-urna/boletim-de-urna'.format(self.url_atual.split(';zn')[0], zona, secao)
                self.acessTse(urlreal)
                sleep(.3)
                self.obterDadosUrna()
                self.countSecao = self.countSecao + 1

            self.countZona = self.countZona + 1

    def obterDadosUrna(self):
        try:
            dicionario = {}
            self.cabecalho = []
            self.cabecalho.append('UF')
            self.cabecalho.append('CIDADE')

            localidade = self.driver.find_element(self.By.TAG_NAME, 'app-selecionar-localidade2').text.split(', ')
            dicionario.update({'UF':[localidade[1]]})
            dicionario.update({'CIDADE':[localidade[0]]})
            self.cidade_atual = localidade[0].upper()
            while True:
                try:
                    sleep(1)
                    identificacao = self.driver.find_elements(self.By.CLASS_NAME, 'identificacao')[0]
                    identificacao = identificacao.find_element(self.By.CLASS_NAME, 'grid-cols-4')
                    identificacao = identificacao.text.split('\n')

                    k = None
                    for item, ident in enumerate(identificacao):
                        if (item % 2):
                            dicionario.update({k:[ident]})
                        else:
                            k = ident.upper()

                    break
                except:
                    pass

            #dados votação
            while True:
                try:
                    sleep(1)
                    dados = self.driver.find_elements(self.By.CLASS_NAME, 'cargo-fixo')[-1].find_element(self.By.XPATH, "parent::div")
                    dados = dados.text.split('\n')
                    break
                except:
                    pass

            remover = ['Presidente', 'Candidato', 'Votação']
            dadosInicio = ''
            for dado in dados:
                if (dado in remover):
                    continue
                if (not(dadosInicio)):
                    dadosInicio = '{}\n'.format(dado)
                else:
                    dadosInicio = '{}{}\n'.format(dadosInicio, dado)

            dados = dadosInicio.split('Eleitores Aptos')
            totais = dados[1].split('\n')
            totais.remove('')
            totais.remove('')
            totais.insert(0, 'Eleitores Aptos')
            dados = dados[0].split('\n')
            dados.remove('')

            k = None
            for item in range(len(dados)):
                if (item % 2): #se é ímpar
                    dicionario.update({k: [dados[item]]})
                else:
                    k = '{}'.format(dados[item])

            if (self.counter == 1):
                self.df = pd.DataFrame(dicionario)
            else:
                self.df2 = None
                self.df2 = pd.DataFrame(dicionario)
                self.df = pd.concat([self.df, self.df2], ignore_index=True)#.replace(np.nan, 0)

            self.counter = self.counter + 1
            self.counterGeral = self.counterGeral + 1
            print('{} - {} - {} - {}(f-{}) - {}(f-{})'.format(self.counterGeral, self.uf_atual, self.cidade_atual, self.zona_atual, len(self.zonas)-self.countZona, self.secao_atual, len(self.secoes)-self.countSecao).upper())
            return True

        except:
            return False