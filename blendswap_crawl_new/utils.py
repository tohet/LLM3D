import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.common.by import By

implicitlyWait = 10


def xpath(dr, val) -> selenium.webdriver.remote.webelement.WebElement:
    """
    driver.find_element_by_xpath
    """
    return dr.find_element(by=By.XPATH, value=val)


def driverInit(path='.\\', headless=False, implicitlyWait=5):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--enable-print-browser')
    if headless:
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {
        'download.default_directory': r'{}'.format(path)
    }
    chrome_options.add_argument('--kiosk-printing')
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """})
    driver.implicitly_wait(implicitlyWait)
    driver.set_window_size(900, 720)
    return driver


def login(dr, userName, password):
    dr.get("https://blendswap.com/login")
    xpath(dr, """//*[@id="email"]""").clear()
    xpath(dr, """//*[@id="email"]""").send_keys(userName)
    xpath(dr, """//*[@id="password"]""").clear()
    xpath(dr, """//*[@id="password"]""").send_keys(password)
    xpath(dr, """/html/body/div/div/div/div[2]/div/form/button""").click()


def getInnerHtml(dr, element):
    """
    :param dr:
    :param element:
    :return:
    """
    return dr.execute_script("return arguments[0].innerHTML;", element)
