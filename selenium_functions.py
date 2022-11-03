from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from os import path as osPath
from platform import system as SO

class SeleniumFunctions(object):

    def __init__(self):
        self.Keys = Keys
        self.By = By

    def select(self, element):
        return Select(element)

    def waitInstance(self, driver, object, poll, type, form = 'xpath'):
        timeOut = 4 #segundos
        count = 0
        element = None
        while (count < 3):
            try:
                if type == 'click':
                    if form == 'xpath':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.XPATH, object)))
                        # return element
                    elif form == 'id':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.ID, object)))
                    elif form == 'class':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.CLASS_NAME, object)))
                        # return element
                elif type == 'show':
                    if form == 'xpath':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.XPATH, object)))
                        # return element
                    elif form == 'id':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.ID, object)))
                    elif form == 'class':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.CLASS_NAME, object)))
                # print('=============> {} - O Elemento "{}" foi encontrado!'.format(count, object).lower())
                return element
            except:
                count = count + 1
                # print('=============> {} - Elemento "{}" ainda não foi encontrado!'.format(count, object).lower())

        return False

    def iniciaWebdriver(self, modSilent = False, monitor = 2, webDriverNumero=1, downloads_path='', wbDriver='chrome'):
        sistemaOperacional = SO()
        chromepath=None

        if (wbDriver=='chrome'):
            chromeDriveFile = '/arquivos_necessarios/chromedriver{}'.format(webDriverNumero)
            if (sistemaOperacional == 'Windows'):
                # acessando diretório do webdriver do chrome no WINDOWS
                dirpath = osPath.dirname(osPath.realpath(__file__))
                chromepath = dirpath + chromeDriveFile.replace('/','\\') + '.exe'.format(webDriverNumero)
            elif (sistemaOperacional == 'Linux'):
                # acessando diretório do webdriver do chrome no LINUX
                dirpath = '/usr/bin'
                chromepath = dirpath + chromeDriveFile

            chromeInstallation = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            if (not(osPath.isfile(chromeInstallation))):
                chromeInstallation = chromeInstallation.replace('Program Files', 'Program Files (x86)')

            import json
            from os import path
            from pathlib import Path
            downloads_path = str('{}\\DOWNLOADS\\{}'.format(path.dirname(path.realpath(__file__)), downloads_path))
            Path(downloads_path).mkdir(parents=True, exist_ok=True)

            settings = {"recentDestinations": [{"id": "Save as PDF",
                                                "origin": "local",
                                                "account": ""}],
                        "selectedDestinationId": "Save as PDF", "version": 2}

            prefs = {"download.default_directory": "{}".format(downloads_path),
                    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                    'savefile.default_directory': "{}".format(downloads_path),
                    "enabled": False,
                    "name": "Chrome PDF Viewer",
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.cookies": 2,
                    "profile.geolocation": 2,
                    "profile.managed_default_content_settings.images": 2}

            options = webdriver.ChromeOptions()
            options.binary_location = chromeInstallation
            options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument('--kiosk-printing')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')

            options.add_argument('--hide-scrollbars')
            options.add_argument("--log-level=3")
            options.add_argument('--window-size=1150,800')  #horizontal / vertical

            options.add_experimental_option("prefs",prefs)

            # options.add_argument("--disable-popup-blocking")
            # options.add_argument("--disable-extensions")
            # options.add_argument("disable-infobars")

            if (modSilent == True):  # Modo Silencioso: O Navegador fica oculto
                options.add_argument('--headless')

            driver = webdriver.Chrome(executable_path = chromepath, chrome_options = options)

        elif (wbDriver=='ie'):
            drivePath = '{}\\arquivos_necessarios\\iedriver1.exe'.format(osPath.dirname(osPath.realpath(__file__)))
            driver = webdriver.Ie(executable_path = drivePath)

        monitor = 1
        pos = 0
        col = 0

        driver.set_window_position(pos, col)   # ATIVA A EXECUÇÃO NO SEGUNDO MONITOR
        return driver