"""
@Author:Pegasus-Yang
@Time: 2020/5/30 上午9:42
"""
from time import sleep

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By


class TestGrid:
    selenium_grid_url = "http://127.0.0.1:4444/wd/hub"
    capabilities = DesiredCapabilities.CHROME.copy()

    def test_a(self):
        driver = Remote(command_executor=self.selenium_grid_url, desired_capabilities=self.capabilities)
        driver.get('https://www.baidu.com')
        driver.implicitly_wait(5)
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#kw').send_keys('selenium')
        driver.find_element(By.CSS_SELECTOR, '#su').click()
        sleep(3)
        driver.get_screenshot_as_file('selenium_baidu.png')
        sleep(1)
        driver.quit()

    def test_b(self):
        driver = Remote(command_executor=self.selenium_grid_url, desired_capabilities=self.capabilities)
        driver.get('https://www.baidu.com')
        driver.implicitly_wait(5)
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#kw').send_keys('appium')
        driver.find_element(By.CSS_SELECTOR, '#su').click()
        sleep(3)
        driver.get_screenshot_as_file('appium_baidu.png')
        sleep(1)
        driver.quit()

    def test_c(self):
        driver = Remote(command_executor=self.selenium_grid_url, desired_capabilities=self.capabilities)
        driver.get('https://www.baidu.com')
        driver.implicitly_wait(5)
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#kw').send_keys('hogwarts')
        driver.find_element(By.CSS_SELECTOR, '#su').click()
        sleep(3)
        driver.get_screenshot_as_file('hogwarts_baidu.png')
        sleep(1)
        driver.quit()
