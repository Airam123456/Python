from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pyautogui
import time

def descargar():
    f = open('links.txt', 'r')
    mensaje = f.read()
    f.close()

    #Variable para controlar cuanto espera entre proceso y proceso
    espera  = 5

    web = webdriver.Firefox()
    web.get(mensaje)
    time.sleep(20)

    web.find_element(By.CSS_SELECTOR, 'span.icon-download').click()
    time.sleep(espera)

    #Aceptar cookies
    web.find_element(By.CSS_SELECTOR, '#didomi-notice-agree-button').click()
    time.sleep(espera)

    #Hacer clcik derecho para descargar
    clickDerecho = web.find_element(By.CSS_SELECTOR, '#dlink')
    actions = ActionChains(web)
    actions.context_click(clickDerecho).perform()

    #Nos movemos por el menu contextual y descargamos el podcast
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(10)
    pyautogui.press('enter')
    time.sleep(60)

    web.quit()
