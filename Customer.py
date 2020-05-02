################## Customer.py ##################
## Author: Gilberto García Hiriart
## Date: 2020, April 17th
#################################################

class Customer(object):
    def __init__(self, complete_name, customerID, transactionCode):
        self.complete_name = complete_name
        self.customerID = customerID
        self.transactionCode = transactionCode
    
    def setCompleteName(self, complete_name):
        self.complete_name = complete_name
    
    def setCustomerID(self, customerID):
        self.customerID = customerID

    def setTransactionCode(self, transactionCode):
        self.transactionCode = transactionCode
    
    def getCompleteName(self):
        return self.complete_name
    
    def getCustomerID(self): 
        return self.customerID
    
    def getTransactionCode(self):
        return self.transactionCode