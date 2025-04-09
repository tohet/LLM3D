from utils import *
from datetime import datetime


class CookieMaker:
    def __init__(self, headless, implicitlyWait):
        self.headless = headless
        self.implicitlyWait = implicitlyWait
        # self.driver = driverInit(headless=headless, implicitlyWait=implicitlyWait)
        self.register_url = "https://blendswap.com/register"

    def register(self, username, email, password):
        self.driver.get(self.register_url)
        username_xpath = """//*[@id="username"]"""
        email_xpath = """//*[@id="email"]"""
        password_xpath = """//*[@id="password"]"""
        confirm_xpath = """//*[@id="password_confirm"]"""
        xpath(self.driver, username_xpath).clear()
        xpath(self.driver, username_xpath).send_keys(username)
        xpath(self.driver, email_xpath).clear()
        xpath(self.driver, email_xpath).send_keys(email)
        xpath(self.driver, password_xpath).clear()
        xpath(self.driver, password_xpath).send_keys(password)
        xpath(self.driver, confirm_xpath).clear()
        xpath(self.driver, confirm_xpath).send_keys(password)
        register_btn_xpath = """/html/body/div/div/div/div/div/form/button"""
        xpath(self.driver, register_btn_xpath).click()

    def getEmail(self):
        current_datetime = datetime.now()
        email = ("derp"+str(current_datetime.date()).replace('-', '') + 'dumb'
                 + str(current_datetime.time()).replace(':', '').replace('.', '')
                 + '@amail.com')
        return email

    def logout(self):
        self.driver.get("https://blendswap.com/logout")

    def getCookie(self):
        username = 'downloader'
        password = '123456789'
        # print('logout...')
        # self.logout()
        self.driver = driverInit(headless=self.headless, implicitlyWait=self.implicitlyWait)
        email = self.getEmail()
        print('Email:', email)
        print('Register...')
        self.register(username=username, email=email, password=password)
        print('getCookie...')
        cookie = self.driver.get_cookies()[0]
        return cookie['value']


if __name__ == '__main__':
    cookieMaker = CookieMaker(headless=True, implicitlyWait=1.2)
    cookieList = []
    for i in range(1000):
        try:
            cookie = cookieMaker.getCookie()
            print(cookie)
            print(type(cookie))
            print("Cookie Num: " + str(i))
            cookieList.append(cookie)
            with open('cookie.txt', 'a') as file:
                file.write(cookie)
                file.write('\n')
        except:
            a = 1
