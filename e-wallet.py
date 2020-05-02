################## e-wallet.py ##################
## Author: Gilberto García Hiriart
## Date: 2020, April 17th
## Main file - control program execution
#################################################

from Customer import Customer
from Wallet import Account, Transaction
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, random, string
from datetime import date

#Function that read customer id and validate it is a number
def readCustomerID():
    while True:
        customer_id = input("Escribe tu número de cliente: ")
        if customer_id.isdigit():
            return customer_id 
        else:
            print ("Número de cliente incorrecto, escribe solo números...")

#Function that validate if entered customer id exist in customers.txt file, if not it is added to the file
def validateCustomerExist():
    customer_file = open('customers.txt','r+')
    customer_exist = False
    for line in customer_file:
        exist = line.find(customer_id)
        if exist != -1: 
            customer_exist = True
            aux_complete_name = line.split(" ")
            transactionCode = aux_complete_name[1]
            i = 2
            complete_name = ""
            while i < len(aux_complete_name):
                complete_name = complete_name + " " + aux_complete_name[i]
                i += 1
            validatedUser=Customer(complete_name,customer_id,transactionCode)
            break
    if customer_exist == False:
        complete_name=input("El usuario que ingesaste no existe, ingresa tu nombre completo: ")
        transactionCode = generateTransactionCode()
        customer_file.write(customer_id + " " + transactionCode + " " +complete_name + '\n')
        validatedUser = Customer(complete_name,customer_id,transactionCode)
    customer_file.close
    return validatedUser

#Function that generates a random transaction code
def generateTransactionCode():
    stringLength = 8
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(letters) for i in range(stringLength))

#Function that show main menu and control execution
def main_menu(user):
    option = 1
    while option != 6:
        print('\n' + "######### E-Wallet Desktop App #########" + '\n')
        print("Menú principal")
        print("1) Recibir cantidad")
        print("2) Transferir monto")
        print("3) Mostrar balance de una moneda")
        print("4) Mostrar balance general")
        print("5) Mostrar histórico de transacciones")
        print("6) Salir del programa")
        option = int(input("Ingresa el número del menú deseado..."))
        if option==1:
            #execute recieve ammount function
            recieveAmmount(user)
        elif option==2:
            #execute transfer ammount function
            transferAmmount(user)
        elif option==3:
            #execute show currency balance function
            showCurrencyBalance(user)
        elif option==4:
            #execute show general currency balance function
            showGeneralBalance(user)
        elif option==5:
            #execute show transaction history function
            showTransactionHistory(user)
        if option < 1 and option > 6:
            print("Opción incorrecta, intenta de nuevo...")
            option = 1

#Function that recieve an ammount according to the specified data
def recieveAmmount(user):
    print('\n' + "Para recibir la transferencia debes ingresar los siguientes datos:")
    currencyID = 0
    while currencyID == 0:
        currencyID = int(input(" - Moneda (Bitcoin - 1; Cardano - 2; Ethereum - 3): "))
        if currencyID==1 or currencyID==2 or currencyID==3:
            break
        else:
            print("Opción incorrecta, intenta de nuevo...")
            currencyID = 0
    if currencyID == 1:
        currency = "BTC"
    elif currencyID == 2:
        currency = "ADA"
    elif currencyID == 3:
        currency = "ETH"
    ammount = float(input(" - Cantidad por la que se hará la transferencia: "))
    valid_ammount = validateTransferAmmount(user,ammount,currency)
    if valid_ammount:
        valid = validateTransferAmmountData(user,currency,"recieve")
        if valid:
            applyTransfer(user,currency,ammount,None,"recieve")
    else:
        print("Los datos proporcionados no fueron encontrados.")

#Function that transfer an ammount according to the specified data
def transferAmmount(user):
    print('\n' + "Para realizar la transferencia debes ingresar los siguientes datos:")
    currencyID = 0
    while currencyID == 0:
        currencyID = int(input(" - Moneda (Bitcoin - 1; Cardano - 2; Ethereum - 3): "))
        if currencyID==1 or currencyID==2 or currencyID==3:
            break
        else:
            print("Opción incorrecta, intenta de nuevo...")
            currencyID = 0
    if currencyID == 1:
        currency = "BTC"
    elif currencyID == 2:
        currency = "ADA"
    elif currencyID == 3:
        currency = "ETH"
    ammount = float(input(" - Cantidad por la que se hará la transferencia: "))
    flagTransactionCode = 0
    while flagTransactionCode == 0:
        transactionCode = input(" - Codigo de transferencia del destinatario: ")
        valid = validateTransactionCode(transactionCode)
        if valid:
            flagTransactionCode = 1
        else:
            print("No existe cliente con el código de transferencia ingresado, intente nuevamente...")
    valid = validateTransferAmmountData(user,currency,"transfer")
    if valid:
        applyTransfer(user,currency,ammount,transactionCode,"transfer")
    else:
        print("Los datos proporcionados no fueron encontrados.")

#Function that show currency balance according to the specified data
def showCurrencyBalance(user):
    currencyID = 0
    currency = ""
    while currencyID == 0:
        print('\n' + "Para mostrar el balance de una moneda debes ingresar los siguientes datos:")
        currencyID = int(input(" - Moneda (Bitcoin - 1; Cardano - 2; Ethereum - 3): "))
        if currencyID==1 or currencyID==2 or currencyID==3:
            break
        else:
            print("Opción incorrecta, intenta de nuevo...")
            currencyID = 0
    if currencyID == 1:
        currency = "BTC"
    elif currencyID == 2:
        currency = "ADA"
    elif currencyID == 3:
        currency = "ETH"
    objAccount = validateSelectedCurrencyBalance(user.getCustomerID(),currency)
    if objAccount != None:
        showSelectedCurrencyBalance(objAccount)
    else:
        print("Los datos proporcionados no fueron encontrados.")

#Function that show general balance
def showGeneralBalance(user):
    print('\n' + "Número de cliente: " + str(user.getCustomerID()) + ", Nombre: " + str(user.getCompleteName()))
    account_file = open('accounts.txt','r')
    total_price = 0.0
    for line in account_file:
        if line.find(user.getCustomerID()) != -1:
            data_list=line.split(" ")
            quotation = getQuotationFromJson(data_list[1])
            price = quotation * float(data_list[2])
            print("  -Moneda: " + data_list[1] + " Cantidad: " + str(data_list[2]) + " Monto en USD: " + str(price))
            total_price = total_price + price
    print("  *Monto total: " + str(total_price))

#Function that show transaction history
def showTransactionHistory(user):
    listObjTransaction = validateTransactionHistory(user)
    if listObjTransaction != None:
        showSelectedTransactionHistory(user,listObjTransaction)
    else:
        print("Los datos proporcionados no fueron encontrados.")

#Function that validates if exist customer with selected transaction code
def validateTransactionCode(transactionCode):
    transaction_code_exist = False
    customer_file = open('customers.txt','r')
    for line in customer_file:
        if line.find(transactionCode) != -1:
            transaction_code_exist = True
    return transaction_code_exist

#Function that validates if transfer file has selected ammount and transfer code
def validateTransferAmmount(user,ammount,currency):
    transaction_exist = False
    transactions_file = open('transactions.txt','r')
    for line in transactions_file:
        if line.find(user.getTransactionCode()) != -1 and line.find(str(ammount)) != -1 and line.find(currency) != -1:
            transaction_exist = True
    return transaction_exist

#Function that validates if customer has selected currency
def validateTransferAmmountData(user,currency,operation):
    if operation=="transfer":
        currency_exist = False
        account_file = open('accounts.txt','r')
        for line in account_file:
            if line.find(currency) != -1 and line.find(user.getCustomerID()):
                currency_exist = True
        return currency_exist
    elif operation=="recieve":
        currency_exist = False
        account_file = open('accounts.txt','r')
        for line in account_file:
            if line.find(currency) != -1 and line.find(user.getCustomerID()):
                currency_exist = True
        if not currency_exist:
            account_file = open('accounts.txt','a+')
            account_file.write(str(user.getCustomerID()) + " " + currency + " 0.00" + '\n')
            account_file.close
            currency_exist = True
        return currency_exist

#Function that applies transaction on file
def applyTransfer(user,currency,ammount,transactionCode,operation):
    #ammount is decreased or increased on the transaction ammount
    account_file = open('accounts.txt','r')
    content = list()
    for line in account_file:
        account_data = line.split(" ")
        if line.find(currency) != -1 and line.find(user.getCustomerID()) != -1:
            if operation=="recieve":
                account_data[2] = float(account_data[2]) + ammount
                status = "applied"
            elif operation=="transfer":
                account_data[2] = float(account_data[2]) - ammount
                status = "pending"
            account_data[2]=str(account_data[2])+'\n'
        content.append(' '.join(account_data))
    account_file.close
    account_file = open('accounts.txt','r+')
    account_file.writelines(content)
    account_file.close
    #transaction is registered in transactions file
    if operation == "recieve":
        content = list()
        transaction_file = open('transactions.txt','r')
        for line in transaction_file:
            transaction_data = line.split(" ")
            if line.find(user.getTransactionCode()) != -1 and line.find(str(ammount)) != -1 and line.find("pending") != -1:
                transaction_data[7] = "applied"+'\n'
            content.append(' '.join(transaction_data))
        transaction_file.close
        transaction_file = open('transactions.txt','r+')
        transaction_file.writelines(content)
        transaction_file.close

    elif operation == "transfer":
        transaction_date = date.today()
        date_format = "%d/%m/%y"
        transaction_date = transaction_date.strftime(date_format)  
        transaction_file = open('transactions.txt','a+')
        quotation = getQuotationFromJson(currency)
        total_ammount = quotation * float(ammount)
        transaction_file.write( str(user.getCustomerID()) + " " + str(transaction_date) + " " + currency + " " + transactionCode + " " + str(ammount) + " " + str(quotation) + " " + str(total_ammount) + " " + status + '\n')
        transaction_file.close

#Function that validate if customer has transaction history
def validateTransactionHistory(user):
    transaction_file = open('transactions.txt','r')
    customer_id_exist = False
    listObjTransaction = []
    for line in transaction_file:
        if line.find(user.getCustomerID()) != -1 or line.find(user.getTransactionCode()) != -1:
            data_list=line.split(" ")
            objTransaction = Transaction(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7])
            listObjTransaction.append(objTransaction)
            customer_id_exist = True
    if customer_id_exist == False:
        print("El usuario actual no cuenta con transferencias en su historial.")
    transaction_file.close
    return listObjTransaction

#Function that print selected transaction history
def showSelectedTransactionHistory(user, listObjTransaction):
    i = 0
    print('\n' + "Número de cliente: " + str(listObjTransaction[i].getCustomerID()) + ", Nombre: " + str(user.getCompleteName()))
    while i < len(listObjTransaction):
        print("Fecha: " + str(listObjTransaction[i].getDate()))
        print("Moneda: " + str(listObjTransaction[i].getCurrency()))
        print("Codigo de transferencia: " + str(listObjTransaction[i].getKey()))
        print("Cantidad: " + str(listObjTransaction[i].getQuantity()))
        print("Cotización: " + str(listObjTransaction[i].getQuotation()))
        print("Monto Total: " + str(listObjTransaction[i].getAmmount()))
        print("Operación: " + listObjTransaction[i].getStatus())
        i = i + 1 

#Function that validate if customer has selected currency
def validateSelectedCurrencyBalance(customerID,currency):
    account_file = open('accounts.txt','r')
    currency_exist = False
    for line in account_file:
        if line.find(customerID) != -1 and line.find(currency) != -1:
            data_list=line.split(" ")
            objAccount = Account(data_list[0],data_list[1],data_list[2])
            return objAccount
    if currency_exist == False:
        print("El usuario actual no cuenta con montos en la moneda seleccionada.")
    account_file.close
    return None

#Function that print selected currency balance
def showSelectedCurrencyBalance(objAccount):
    quotation = getQuotationFromJson(objAccount.getCurrency())
    ammountUSD = float(objAccount.getAmmount()) * float(quotation)
    print("Numero de cuenta: " + objAccount.getCustomerID())
    print("Moneda: " + objAccount.getCurrency())
    print("Cantidad: " + objAccount.getAmmount())
    print("Monto en USD: " + str(ammountUSD))

#Function that gets quotation
def getQuotationFromJson(currency):
    COINMARKET_API_KEY = "ee6660c3-9192-4cc9-885a-40a0e549d188"
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {'symbol': currency}
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKET_API_KEY
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = data['data'][currency]['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return price

#main code
print("Bienvenido a tu E-Wallet" + '\n')
customer_id = readCustomerID()
current_user = validateCustomerExist()
main_menu(current_user)