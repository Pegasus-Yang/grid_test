"""
@Author:Pegasus-Yang
@Time: 2020/6/7 下午3:43
"""
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


class TestGrid:
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_a(self):
        self.driver.get('https://www.baidu.com')
        self.driver.implicitly_wait(5)
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, '#kw').send_keys('selenium')
        self.driver.find_element(By.CSS_SELECTOR, '#su').click()
        sleep(3)
        self.driver.get_screenshot_as_file('selenium_baidu.png')
        sleep(1)
        self.driver.quit()

    def test_b(self):
        self.driver.get('https://www.baidu.com')
        self.driver.implicitly_wait(5)
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, '#kw').send_keys('appium')
        self.driver.find_element(By.CSS_SELECTOR, '#su').click()
        sleep(3)
        self. driver.get_screenshot_as_file('appium_baidu.png')
        sleep(1)
        self.driver.quit()

    def test_c(self):
        self.driver.get('https://www.baidu.com')
        self.driver.implicitly_wait(5)
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, '#kw').send_keys('hogwarts')
        self.driver.find_element(By.CSS_SELECTOR, '#su').click()
        sleep(3)
        self.driver.get_screenshot_as_file('hogwarts_baidu.png')
        sleep(1)
        self.driver.quit()
