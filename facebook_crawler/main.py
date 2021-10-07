from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pyotp
import time
import pickle
import os
import logging
import datetime

# Config logger
logging.basicConfig(filename=f'logging/{datetime.datetime.now().date()}.log', filemode='w', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')

path_cookie_file = './cookies'
accounts = ["100072676860931|TCnyAOVV68|NR6GR2OPLZT5GHZBFP23RDW3ZVH6JWIO",
            "100072703980545|TCUn53pE68|E5YD2TXHF4GG7WDTKA4F6YA64ZG4TJ4N",
            "100072726870283|TCiIMbGk68|F45T6MZWU464UP5R4B2YWUKBC34RBZ7E",
            "100057425583469|TCFiP7aa68|CFA7XEAQPXNOIS3HK2ARL5SWVQ35DAJR",
            "100072639573837|TCr5l4UN68|ISMM6MUPSR7QELVH6IKOA5PFUROJ34MR",
            "100072606813477|TC5QCK7t68|KTT5GBLO6NTFUUJOQ2QUKVZSOI2CEH6R",
            "100060182294775|TCnWdk3W68|24IO3FOHNFT5RI4YVOWWWX5Y7S2B2UN2",
            "100058520920704|TCBpf93X68|SDY2DQMLF6LAYODFCFBIS2SBWCCK5RVO",
            "100072531338942|TCk4sHDG68|7RKBYNXVE5JBVCOLNSVPCK7PR4TJHWCI",
            "100072436341048|TCTbELhO68|QDX2ECEKIBMZIARNH7MHXNQRFEVXSEXK",
            "100058719221472|TCfEcIY968|JZFVLFCJVEVYVI5DNYIS6XYOCNJGPJ7A",
            "100072721920358|TCrxHM7D68|DTYBKLKZEG52Y6F3XIH2W4M7IK4XTOZ5",
            "100072683280933|TCPr3TcT68|4EPBSW3LH43DWG5XU24YQDZZPYP4U45X",
            "100072401987194|TC5h7b7o68|IXSSWHL7U4Z2L3S4H4YANUBBD5EPL2CB",
            "100072391039372|TCkSwT9h68|5CD7MHU5V5OJA3MKR64ZTHG7MIRXJGBW]", ]


def get_otp(token):
    otp = pyotp.TOTP(token)
    return otp.now()


def save_cookie(driver, path):
    with open(path, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookie(driver, path):
    with open(path, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)


def is_fb_logged_in(browser):
    browser.get("https://facebook.com")
    if 'Facebook – log in or sign up' in browser.title:
        return False
    else:
        return True


def login_by_cookie(browser):
    load_cookie(browser, path_cookie_file)
    browser.refresh()


def login_by_username(account: str, browser):
    # browser_driver.execute_script("window.open('https://facebook.com');")
    # browser_driver.switch_to.window(browser_driver.window_handles[index])
    # browser.get("https://facebook.com")
    [id_account, password, token] = account.split('|')

    username_input = browser.find_element_by_id("email")
    username_input.send_keys(id_account)

    password_input = browser.find_element_by_id("pass")
    password_input.send_keys(password)

    password_input.send_keys(Keys.ENTER)

    otp = get_otp(token)

    otp_input = browser.find_element_by_id("approvals_code")
    # for first time login
    if otp_input:
        otp_input.send_keys(otp)
        otp_input.send_keys(Keys.ENTER)
        # Nho trinh du 1st
        try:
            browser.find_element_by_id("checkpointSubmitButton").send_keys(Keys.ENTER)

            # Xem lại lần đăng nhập gần đây
            browser.find_element_by_id("checkpointSubmitButton").send_keys(Keys.ENTER)

            # Day la toi
            browser.find_element_by_id("checkpointSubmitButton").send_keys(Keys.ENTER)

            # Nho trinh duyet 2nd
            browser.find_element_by_id("checkpointSubmitButton").send_keys(Keys.ENTER)
        except:
            logging.error(f"login_by_username fail with account {id_account}", exc_info=True)
            pass
            # browser.close()
        # save cookie
    save_cookie(browser, path_cookie_file)


def import_file_in_ads(browser):
    browser.get('https://facebook.com/pe')
    time.sleep(10)
    # close FB'ads
    try:
        try:
            browser.find_elements_by_css_selector("body > div:nth-child(61) > div > div > div > div > div > div > div > div> div > div> div")[0].click()
        except:
            pass
        browser.find_elements_by_css_selector("body > div > div > div > div > div > div > div > div > div > span > div")[0].click()
        time.sleep(3)
    except:
        pass

    # confirm facebook page
    try:
        browser.find_elements_by_css_selector('body > div > div > div > div > div > div > div> div > div> div > div:nth-child(2)> div >div:nth-child(2)>div:nth-child(2)>div>div>div>div>div>div:nth-child(2)>div>div>div>div>div>div>div>div>div>div>div:nth-child(2)>div:nth-child(1)>div:nth-child(2)>div>div:nth-child(2)>div:nth-child(2) >div>div>div>div:nth-child(3)')[0].click()
        time.sleep(3)
    except:
        ...

    # click btn create camp
    try:
        browser.find_elements_by_css_selector('body > div > div > div > div > div  > div > div > div  > div > div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > div > div  > div > div  > div > div:nth-child(2)> div  > div > div > div  > div > div > div  > div > div > div > div:nth-child(1) > div>div>div:nth-child(2)>div:nth-child(1)')[0].click()
    except:
        ...

    try:
        browser.find_elements_by_css_selector("body > div > div > div > div > div > div > div > div > div > span > div > div")[0].click()
        time.sleep(3)
        browser.find_elements_by_css_selector("body > div > div> div > div > div > div > div > div > div > span > div")[0].click()
    except:
        pass

    # add file
    try:
        # click icon Export & Import
        # when small screen
        try:
            # click btn "Khac"
            browser.find_elements_by_css_selector(
                "div > div > div > div:nth-child(1) > div >div>div>div>div>div:nth-child(1)>div:nth-child(5)")[
                1].click()
            # click btn export/import
            # browser.find_element_by_xpath(
            #     '//*[@id="facebook"]/body/div[5]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[12]').click()
            try:
                browser.find_elements_by_css_selector('body > div> div > div > div > div > div > div > div > div:nth-child(12)')[0].click()
            except:
                try:
                    browser.find_elements_by_css_selector('body > div> div > div > div > div > div > div > div > div:nth-child(11)')[0].click()
                except:
                    pass
        except:
            browser.find_elements_by_css_selector(
                "div > div > div > div:nth-child(1) > div >div>div>div>div>div>div:nth-child(6)>div:nth-child(4)")[
                0].click()

            # click ads
            browser.find_elements_by_css_selector(
                "body > div:nth-child(63) > div > div > div > div > div > div > div > div:nth-child(9)")[0].click()

        # import file
        time.sleep(3)
        browser.find_element_by_xpath("//input[@type='file']").send_keys(os.getcwd() + "/docs/export_20211004_1218.csv")

        # click btn "Nhap"
        time.sleep(1)
        browser.find_elements_by_css_selector("body > div > div > div > div > div > div > div > div > div > span > div > div:nth-child(2)")[0].click()
    except:
        logging.error("import_file_in_ads fails", exc_info=True)
        pass


def add_payment(browser, card_info):
    browser.get('https://www.facebook.com/ads/manager/billing_history/summary')
    sleep(2)
    # browser.find_elements_by_xpath("//*[contains(text(), 'Payment Settings')]")
    try:
        # go setting payment
        browser.find_elements_by_css_selector(".uiContextualLayerParent > div > div  > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div >div> div:nth-child(2) > div")[0].click()
        time.sleep(3)

        # click Add method
        browser.find_elements_by_css_selector(".uiContextualLayerParent > div > div > div > div > div:nth-child(2) > div > div:nth-child(3) >div >div>div>div>div>div:nth-child(2)>div>div>div>div>div>div>div>div>div>div>div>div>div:nth-child(2)")[0].click()
        time.sleep(3)

        # click Next
        browser.find_elements_by_css_selector(".uiLayer>div>div>div>div>div>div>div>div>div>div>div:nth-child(4)>div>div>div>div>div")[0].send_keys(Keys.ENTER)
        time.sleep(3)

        # Fill form: card_name, card_number, date, cvv
        inputs = browser.find_elements_by_css_selector("div > input")
        inputs[0].send_keys(card_info["name"])
        inputs[1].send_keys(card_info["number"])
        inputs[2].send_keys(card_info["date"])
        inputs[3].send_keys(card_info["cvv"])

        # click save
        browser.find_elements_by_css_selector('body > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > div >div>div>div>div>div:nth-child(1)>div:nth-child(4)>div>div>div>div:nth-child(1)')[0].click()
        time.sleep(15)
    except:
        logging.error(f"add_payment fails with card's number: {card_info['number']}", exc_info=True)
        pass


def accept_invite_to_be_admin(browser):
    sleep(3)
    # skip popup notify
    try:
        browser.find_elements_by_css_selector('div')[0].send_keys(Keys.ENTER)
    except:
        ...

    # accept invite
    browser.find_elements_by_css_selector(
        "div > div:nth-child(1) > div > div:nth-child(4) > div > div > div:nth-child(2) > span > div > a")[0].click()
    sleep(3)
    browser.find_elements_by_css_selector(
        "div > div:nth-child(1) > div > div:nth-child(4) > div > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div>div>div:nth-child(3) > div > div > div>div:nth-child(2)")[
        0].click()
    sleep(3)
    browser.find_element_by_xpath("//div[@aria-label='Chấp nhận']").click()
    return
    try:
        sleep(3)
        browser.find_elements_by_css_selector("div > div:nth-child(1) > div > div:nth-child(4) > div > div > div:nth-child(2) > span > div > a")[0].click()
        sleep(3)
        browser.find_elements_by_css_selector("div > div:nth-child(1) > div > div:nth-child(4) > div > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div>div>div:nth-child(3) > div > div > div>div:nth-child(2)")[0].click()
        sleep(3)
        browser.find_element_by_xpath("//div[@aria-label='Chấp nhận']").click()
    except:
        pass


if __name__ == '__main__':
    for acc in accounts[5:6]:
        # browser_driver.switch_to.window(browser_driver.window_handles[index])
        browser_driver = webdriver.Chrome(executable_path='./chromedriver')
        browser_driver.get("https://facebook.com")
        time.sleep(3)
        try:
            login_by_cookie(browser_driver)
        except:
            login_by_username(acc, browser_driver)
        accept_invite_to_be_admin(browser_driver)
        break

        # add method
        card_information = {
            "number": 5411741360450085,
            "cvv": 476,
            "date": '06/26',
            "name": "Barbara",
        }
        add_payment(browser_driver, card_information)

        # create campaign by import file
        import_file_in_ads(browser_driver)
        # browser_driver.close()
