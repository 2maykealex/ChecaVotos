import pandas as pd
from sys import exc_info
from decouple import config
from time import sleep, strftime
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
        self.cabecalho = []
        self.registros = {}
        df = None
        dfIncremental = None
        # self.ufs = ['Acre – AC', 'Alagoas – AL', 'Amapá – AP', 'Amazonas – AM', 'Bahia – BA', 'Ceará – CE', 'Distrito Federal – DF', 'Espírito Santo – ES', 'Exterior – ZZ', 'Goiás – GO', 'Maranhão – MA', 'Mato Grosso – MT', 'Mato Grosso do Sul – MS', 'Minas Gerais – MG', 'Paraná – PR', 'Paraíba – PB', 'Pará – PA', 'Pernambuco – PE', 'Piauí – PI', 'Rio de Janeiro – RJ', 'Rio Grande do Norte – RN', 'Rio Grande do Sul – RS', 'Rondônia – RO', 'Roraima – RR', 'Santa Catarina – SC', 'Sergipe – SE', 'São Paulo – SP', 'Tocantins – TO']

    def acessTse(self, url):
        try:
            if (not(self.driver)):
                modSilent= config('MODSILENT')
                print("\nINICIANDO WebDriver")
                self.driver = self.selenium.iniciaWebdriver(webDriverNumero = self.webDriverNumero, modSilent=modSilent)

            self.driver.get(url)
            print('LOGIN REALIZADO NO INTEGRA')
            return True

        except Exception as err:
            exception_type, exception_object, exception_traceback = exc_info()
            line_number = exception_traceback.tb_lineno
            print('---> ERRO NA LINHA {}: {} >>>'.format(line_number, err))
            return False

    def selecionaLocal(self):
        selectedLocal = False
        self.countCity  = 0
        try:
            while True:
                try:
                    sleep(1)
                    self.driver.find_elements(self.By.CLASS_NAME, 'leading-tight')[1].click()
                    sleep(1)
                    cidades = self.driver.find_elements(self.By.TAG_NAME, 'mat-option')
                    if (self.countCity > len(cidades)):
                        self.countCity  = 0
                        break

                    cidades[self.countCity].click()
                    self.countCity = self.countCity + 1
                    self.driver.find_element(self.By.CLASS_NAME, 'button-block').click()
                    selectedLocal = self.selecionaZona()
                except:
                    pass

                if (selectedLocal):
                    return True
        except:
            return False

    def selecionaZona(self):
        self.countZona = 0
        selectedZona = False
        try:
            while True:
                try:
                    sleep(1)
                    self.driver.find_elements(self.By.TAG_NAME, 'mat-form-field')[0].click()
                    zonas = self.driver.find_elements(self.By.CLASS_NAME, 'mat-active')
                    if (self.countZona > len(zonas)):
                        self.countZona  = 0
                        break

                    zonas[self.countZona].click()
                    self.selecionaSecao()
                except:
                    pass

                if (selectedZona):
                    return True
        except:
            return False

    def selecionaSecao(self):
        self.countSecao = 1
        selectedSecao = False
        try:
            while True:
                try:
                    sleep(1)
                    self.driver.find_elements(self.By.TAG_NAME, 'mat-form-field')[1].click()
                    secoes = self.driver.find_element(self.By.CLASS_NAME, 'cdk-overlay-container').find_elements(self.By.CLASS_NAME, 'mat-option')
                    if (self.countSecao > len(secoes)):
                        self.countSecao  = 0
                        return True

                    secoes[self.countSecao].click()
                    self.countSecao = self.countSecao + 1
                    self.driver.find_element(self.By.TAG_NAME, 'button').click()
                    self.getDataUrna()
                except:
                    break

        except:
            return False

    def getDataUrna(self):
        try:
            dicionario = {}

            self.cabecalho = []
            self.cabecalho.append('UF')
            self.cabecalho.append('CIDADE')

            totalGeral = []
            localidade = self.driver.find_element(self.By.TAG_NAME, 'app-selecionar-localidade2').text.split(', ')

            dicionario.update({'UF':[localidade[1]]})
            dicionario.update({'CIDADE':[localidade[0]]})

            totalGeral.append(localidade[1])
            totalGeral.append(localidade[0].upper())

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

            # for item, tot in enumerate(totais):
            #     if (item % 2):
            #         totalGeral.append(tot)
            #     else:
            #         self.cabecalho.append(tot.upper())

            k = None
            for item in range(len(dados)):
                if (item % 2): #se é ímpar
                    dicionario.update({k: [dados[item]]})
                else:
                    k = '{}'.format(dados[item])

                totalGeral.append(dados[item])
            try:
                totalGeral.remove('')
            except:
                pass

            # registro = {}
            # for item in range(len(totalGeral)):
            #     registro.update({self.cabecalho[item]: totalGeral[item]})

            if (self.counter == 1):
                self.df = pd.DataFrame(dicionario)
                # self.df = pd.Series(totalGeral, columns=self.cabecalho)
                # self.df = pd.Series()
            else:
                self.df2 = None
                self.df2 = pd.DataFrame(dicionario)
                self.df3 = pd.concat([self.df, self.df2], ignore_index=True)

            # else:
            #     self.dfIncremental = pd.Series (totalGeral)
            #     pd.DataFrame(totalGeral, columns=list(self.cabecalho))
            #     self.df
            #     self.df1 = pd.concat([self.df, self.dfIncremental])
            #     # for item, cab in enumerate(self.cabecalho):
            #     #     self.df[cab].add(totalGeral[item])

            self.counter = self.counter + 1
            return True

        except:
            return False