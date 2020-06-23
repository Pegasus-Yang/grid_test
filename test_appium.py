"""
@Author:Pegasus-Yang
@Time: 2020/6/6 下午6:48
"""
import os
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy


class TestWeixin:
    def setup(self):
        caps = {}
        caps["platformName"] = "Android"
        caps["deviceName"] = "abc"
        caps["platformVersion"] = "6"
        caps['udid'] = os.getenv("udid", None)
        # caps["appPackage"] = "com.tencent.wework"
        # caps["appActivity"] = ".launch.WwMainActivity"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps['noReset'] = "true"
        # caps['skipServerInstallation'] = True
        # caps['skipDeviceInitialization'] = True
        # caps['dontStopAppOnReset'] = True
        self.driver = webdriver.Remote('http://192.168.50.33:4444/wd/hub', caps)
        self.driver.implicitly_wait(10)

    def teardown(self):
        self.driver.quit()

    def test_search(self):
        self.driver.find_element(MobileBy.ID, "com.xueqiu.android:id/home_search")