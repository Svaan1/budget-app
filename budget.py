
def percentage(part, whole):
  percentage = 100 * float(part)/float(whole)
  return percentage
           
class Category:

    def __init__(self,category):
        self.category = category
        self.ledger = list()
        self.funds = 0
      
    def __str__(self):
        self.title = self.category.center(30,'*') + '\n'
        self.table = ''
        self.total = f'Total: {self.funds}'
        for index in self.ledger:
            self.amount = str(f"{index['amount']:.2f}")[:7]
            self.table += index['description'][:23] + ' ' * (30 - (len(index['description'][:23]) + len(str(self.amount))))
            self.table += self.amount
            self.table += '\n'

        return self.title + self.table + self.total

    def deposit(self,amount,description=None):
        if description == None:
            self.ledger.append({"amount": amount,"description": ""})
        else:
            self.ledger.append({"amount": amount,"description": description})
        self.funds += amount
    
    def withdraw(self,amount,description=None):
        if self.check_funds(amount) == False:
            return False
        else: 
            if description == None:
                self.ledger.append({"amount": -amount,"description": ""})
            else:
                self.ledger.append({"amount":-amount,"description": description})
            self.funds -= amount
            return True

    def get_balance(self):
        return self.funds
    
    def transfer(self,amount,destination):
        if self.check_funds(amount) == False:
            return False
        else:
            self.withdraw(amount,f'Transfer to {destination.category}')
            destination.deposit(amount,f'Transfer from {self.category}')
            return True

    
    def check_funds(self,amount):
        if self.funds < amount:
            return False
        else:
            return True


def create_spend_chart(category_list):

    values = list()
    lines = ''
    maxlen = 0
    all_withdrawals = 0
    for index in category_list:
        value = {}
        deposits = 0
        withdrawals = 0
        if len((index.category)) > maxlen:
            maxlen = len((index.category))                
        for i in index.ledger:
            if i['amount'] > 0:
                deposits += i['amount']
            if i['amount'] < 0:
                withdrawals += i['amount']
        value['Category'] = index.category
        value['Spent'] = abs(withdrawals)
        all_withdrawals += abs(withdrawals)
        values.append(value)
    
    for number in range(len(values)):
        values[number]['Percentage'] = percentage(values[number]['Spent'],all_withdrawals)
    
    lines += 'Percentage spent by category\n'

    for number in range(100,-10,-10):
        lines += f'{number:>3}| '
        for index in values:
            if index['Percentage'] > number:
                lines += 'o  '
            else:
                lines += '   '
        lines += '\n'   
    
    lines += ' '*(4) + '-' * (1 + (3*len(values))) + '\n'

    for number in range(maxlen):
        lines += ' ' * (5)
        for index in values:
            try:
                lines += index['Category'][number] + '  '
            except:
                lines += ' ' * (3)
        lines += '\n'
    result = lines[:-1]
    return result