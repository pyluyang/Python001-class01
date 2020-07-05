from selenium import webdriver
import time

class ShimoLogin:
    
    def login(self):
        try:
            #chrome browser `   ```````````
            browser = webdriver.Chrome()
            
            browser.get('https://www.shimo.im')
            time.sleep(1)
            #entry of login
            btm1 = browser.find_element_by_xpath('//button[@class="login-button btn_hover_style_8"]')
            #btm1 = browser.find_element_by_xpath('//button[contains(text(), "登录")]')
            btm1.click()
            #login 
            browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('18642827832')
            browser.find_element_by_xpath('//input[@name="password"]').send_keys('Spring2019!@')
            time.sleep(1)
            browser.find_element_by_xpath('//button[contains(text(), "立即登录")]').click()
            time.sleep(1)
            cookies = browser.get_cookies() # 获取cookies
            print(cookies)
            time.sleep(3)

            browser.close()
        except Exception as e:
            print(e)
        finally:
            browser.close()

def main():
    w = ShimoLogin()
    w.login()

if __name__ == '__main__':
    main()