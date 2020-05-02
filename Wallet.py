################### Wallet.py ###################
## Author: Gilberto García Hiriart
## Date: 2020, April 17th
#################################################

class Account(object):
    def __init__(self, customerID, currency, ammount):
        self.customerID = customerID
        self.currency = currency
        self.ammount = ammount
    
    def setCustomerID(self, customerID):
        self.customerID = customerID

    def setCurrency(self, currency):
        self.currency = currency
    
    def setAmmount(self, ammount):
        self.ammount = ammount
    
    def getCustomerID(self):
        return self.customerID
    
    def getCurrency(self):
        return self.currency
    
    def getAmmount(self): 
        return self.ammount

class Transaction(object):
    def __init__(self, customerID, date, currency, key, quantity, quotation, ammount, status):
        self.customerID = customerID
        self.date = date
        self.currency = currency
        self.key = key
        self.quantity = quantity
        self.quotation = quotation
        self.ammount = ammount
        self.status = status

    def setCustomerID(self, customerID):
        self.customerID = customerID

    def setDate(self, date):
        self.date = date

    def setCurrency(self, currency):
        self.currency = currency

    def setKey(self, key):
        self.key = key

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setQuotation(self, quotation):
        self.quotation = quotation

    def setAmmount(self, ammount):
        self.ammount = ammount

    def setStatus(self, status):
        self.status = status

    def getCustomerID(self):
        return self.customerID

    def getDate(self):
        return self.date
    
    def getCurrency(self):
        return self.currency
    
    def getKey(self):
        return self.key

    def getQuantity(self):
        return self.quantity

    def getQuotation(self):
        return self.quotation

    def getAmmount(self):
        return self.ammount

    def getStatus(self):
        return self.status