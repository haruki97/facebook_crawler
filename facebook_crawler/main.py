from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pyotp
import time
import pickle

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
            pass
            # browser.close()
        # save cookie
    save_cookie(browser, path_cookie_file)


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
    except:
        pass


if __name__ == '__main__':
    for acc in accounts[:1]:
        # browser_driver.switch_to.window(browser_driver.window_handles[index])
        browser_driver = webdriver.Chrome(executable_path='./chromedriver')
        browser_driver.get("https://facebook.com")
        time.sleep(3)
        try:
            login_by_cookie(browser_driver)
        except:
            login_by_username(acc, browser_driver)

        card_information = {
            "name": "Oh Sehun",
            "number": 8437846374,
            "date": "12/12",
            "cvv": 213
        }
        # add method
        add_payment(browser_driver, card_information)
        # browser.close()
