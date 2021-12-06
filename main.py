from selenium import webdriver
from fake_useragent import UserAgent
import csv
import requests
import os
import time
import random


#useragent = UserAgent()

optinos = webdriver.FirefoxOptions()
#optinos.set_preference('general.useragent.override', useragent.random) #Рандомный юзер-агент
optinos.set_preference('dom.webdriver.enabled', False)
optinos.set_preference('dom.webnotifications.enaled', False)
optinos.set_preference('media.volume_scale', '0.0')
#optinos.headless = True # Фоновый режим

class Avito:

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='D:\pythonProject\kekw\geckodriver',options=optinos)

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def main(self, url, pages):
        for i in range(1, pages+1):
            url = f'{url}&p={i}'
            self.browser.get(url)
            self.parser(self.browser.find_elements_by_xpath("//div[@data-marker='item-photo']"))
        self.close_browser()

    def parser(self, items):
        browser = self.browser
        try:
            for i in range(2): #len(items)
                items[i].click()
                browser.implicitly_wait(5)
                browser.switch_to.window(browser.window_handles[1])

                title = browser.find_element_by_class_name('title-info-title').text
                print('Взял название')
                time.sleep(3)
                price = browser.find_element_by_class_name('item-price').text
                print('Взял цену')
                time.sleep(3)
                #print('Название: ' + title + ' ' + 'Цена: ' + price + ' ')
                #name = browser.find_element_by_class_name('item-view-actions').find_element_by_class_name('seller-info-value').text
                print('Взял имя продовца')
                time.sleep(3)
                #desc = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[4]/div[1]/div[2]/div[4]').text
                print('Взял описание')
                time.sleep(3)
                self.save_images(title)
                time.sleep(2)
                self.save_csv(title, price) #name

                browser.switch_to.window(browser.window_handles[0])
                browser.implicitly_wait(5)  # .send_keys(Keys.CONTROL + 'a')
        except Exception as ex:
            print(ex)
            self.close_browser()

    def save_images(self, title):
        browser = self.browser
        browser.implicitly_wait(5)
        urls_images = browser.find_elements_by_class_name("gallery-img-frame")
        browser.implicitly_wait(5)
        if title.find('/'): title = title.replace('/',' ')
        else: pass
        if os.path.exists(f'{title}'): print('Папка создана')
        else: os.mkdir(title)
        time.sleep(3)

        for img in urls_images:
            img = img.get_attribute('data-url')
            name_img = img.split('.')
            get_img = requests.get(img)
            with open(f"{title}/{name_img[0].replace('https://','')}.jpg", 'wb') as img_file:
                img_file.write(get_img.content)
                print('Картинка скачена!')
                time.sleep(1)
        browser.close()

    def save_csv(self, title, price,): #name
        data_base = [title,f'{price} rub', ] #name
        try:
            with open('data.csv', 'a+',  newline='') as file:
                writer = csv.writer(file, delimiter=';')
                #writer.writerow(['title', 'price', 'name', 'discription', 'number'])
                writer.writerow(data_base)
        except Exception as ex:
            print(ex)
            self.close_browser()

url = input('Введите url Avito: ')
pages = int(input('Введите количество страниц: '))
my_bot = Avito()
my_bot.main(url,pages)