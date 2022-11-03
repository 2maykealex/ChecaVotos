import basic_functions
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
        self.states = []
        self.cities = []
        self.countState = 0
        self.countCity  = 0
        self.countZona  = 0
        self.countSecao = 1
        # self.ufs = ['Acre – AC', 'Alagoas – AL', 'Amapá – AP', 'Amazonas – AM', 'Bahia – BA', 'Ceará – CE', 'Distrito Federal – DF', 'Espírito Santo – ES', 'Exterior – ZZ', 'Goiás – GO', 'Maranhão – MA', 'Mato Grosso – MT', 'Mato Grosso do Sul – MS', 'Minas Gerais – MG', 'Paraná – PR', 'Paraíba – PB', 'Pará – PA', 'Pernambuco – PE', 'Piauí – PI', 'Rio de Janeiro – RJ', 'Rio Grande do Norte – RN', 'Rio Grande do Sul – RS', 'Rondônia – RO', 'Roraima – RR', 'Santa Catarina – SC', 'Sergipe – SE', 'São Paulo – SP', 'Tocantins – TO']

    def logSistema(self, messageSystem, reg=0):
        hoje = "%s" % (strftime("%d-%m-%Y"))
        hoje = hoje.replace('-', '/')
        hora = strftime("%H:%M:%S")
        basic_functions.createLog(self.systemLogFile, 'REG {}; {} {};{}\n'.format(reg, hoje, hora, messageSystem.upper().strip()), printOut=False)

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
            print('{}\n ERRO EM {} na linha {} >>>'.format(self.fileName, err, line_number))
            return False

    def selecionaLocal(self):
        selectedLocal = False
        while True:
            try:
                sleep(1)
                self.driver.find_elements(self.By.CLASS_NAME, 'leading-tight')[1].click()
                while True:
                    try:
                        sleep(1)
                        cidades = self.driver.find_elements(self.By.TAG_NAME, 'mat-option')
                        cidades[self.countCity].click()
                        self.countCity = self.countCity + 1
                        # self.driver.find_element(self.By.CLASS_NAME, 'buttons-last-slot').click()
                        self.driver.find_element(self.By.CLASS_NAME, 'button-block').click()
                        self.selecionaZona()
                        selectedLocal = True
                        break
                    except:
                        pass
                break
            except:
                pass

            if (selectedLocal):
                break

    def selecionaZona(self):
        self.countZona = 0
        selectedZona = False
        while True:
            try:
                sleep(1)
                self.driver.find_elements(self.By.TAG_NAME, 'mat-form-field')[0].click()
                while True:
                    try:
                        sleep(1)
                        self.driver.find_elements(self.By.CLASS_NAME, 'mat-active')[self.countZona].click()
                        self.countZona = self.countZona + 1
                        selectedZona = True
                        self.selecionaSecao()
                        break
                    except:
                        pass
            except:
                pass

            if (selectedZona):
                break

    def selecionaSecao(self):
        self.countSecao = 1
        selectedSecao = False
        while True:
            try:
                sleep(1)
                self.driver.find_elements(self.By.TAG_NAME, 'mat-form-field')[1].click()
                secoes = self.driver.find_element(self.By.CLASS_NAME, 'cdk-overlay-container').find_elements(self.By.CLASS_NAME, 'mat-option')
                secoes[self.countSecao].click()
                self.countSecao = self.countSecao + 1
                self.driver.find_element(self.By.TAG_NAME, 'button').click()
                self.getDataUrna()
                # selectedSecao = True
                #...
                # break
            except:
                break

            if (selectedSecao):
                break

    def getDataUrna(self):
        totalGeral = []
        localidade = self.driver.find_element(self.By.TAG_NAME, 'app-selecionar-localidade2').text.split(', ')
        totalGeral.append('UF')
        totalGeral.append(localidade[1])
        totalGeral.append('CIDADE')
        totalGeral.append(localidade[0].upper())

        while True:
            try:
                sleep(1)
                identificacao = self.driver.find_elements(self.By.CLASS_NAME, 'identificacao')[0]
                identificacao = identificacao.find_element(self.By.CLASS_NAME, 'grid-cols-4')
                identificacao = identificacao.text.split('\n')
                totalGeral.extend(identificacao)
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
        dados  = dados[0].split('\n')
        dados.remove('')

        for item in reversed(range(14)):
            if (item % 2): #se é ímpar
                dados.insert(item, 'VOTOS')
            else:
                dados.insert(item, 'CANDIDATO')

        totalGeral.extend(totais)
        totalGeral.extend(dados)

        try:
            totalGeral.remove('')
        except:
            pass

        print('ok')

