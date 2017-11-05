# ATM
//用python来实现ATM的简单功能

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 20:32:13 2017

@author: biggestbear
"""

class CardNotEnoughBalanceError(ValueError):
    pass

class MachineNotEnoughBalanceError(ValueError):
    pass

class User(object):
    def __init__(self,name,tel,id):
        self.__name = name
        self.__tel = tel
        self.__id = id
        self.__card = []
    
    def getName(self):
        return self.__name
    
    def getTel(self):
        return self.__tel
    
    def getId(self):
        return self.__id
    
    '''按卡号获得用户的卡的对象'''
    def getCard(self,cno):
        for x in self.__card:
            if x.getCno()==cno:
                return x
            
    '''返回用户所拥有的卡的卡号'''
    def getCards(self):
        l = []
        for x in self.__card:
            l.append(x.getCno())
        return l
    
    def addCard(self,addcard):
        self.__card += [addcard]
        
    def delCard(self,delcard):
        self.__card.remove(delcard)
        
class Card(object):
    def __init__(self,cno,password,owner):
        self.setCno(cno)
        self.setPassword(password)
        self.setBalance(0)
        self.setFrozen(False)
        self.setOwner(owner)
        owner.addCard(self)
        Server.add_account(self)
    
    def setCno(self,cno):
        self.__cno = cno
        
    def getCno(self):
        return self.__cno
    
    def setPassword(self,password):
        self.__password = password
        
    def getPassword(self):
        return self.__password
    
    def setBalance(self,balance):
        self.__balance = balance
        
    def getBalance(self):
        return self.__balance
    
    def setFrozen(self,frozen):
        self.__frozen = frozen
        
    def getFrozen(self):
        return self.__frozen
    
    def setOwner(self,owner):
        self.__owner = owner
        
    def getOwner(self):
        return self.__owner
    
'''模拟数据库  只是用于储存卡的对象 方便查找获得卡的对象'''
class Server(object):
    d = dict()
    @classmethod
    def add_account(cls,card):
        cls.d[card.getCno()] = card
        pass
    
    @classmethod
    def get_account(cls,cno):
        return cls.d.get(cno)
    
class ATMMachine(object):
    def __init__(self,id,balance):
       self.__id = id
       self.is_inserted(False)
       self.setBalance(balance)
       
    '''设置是否插入卡片'''
    def is_inserted(self,inserted):
        self.__isinserted = inserted
        
    '''密码验证'''
    def password_check(self,card):
        n = 0
        while n < 3:
            print('''
        -1:退卡
            ''')
            password = input('请输入密码：')
            if password == '-1':
                self.back_card()
                return False
            elif password == card.getPassword():
                return True
            n += 1
            print('你还有%d次机会' % (3-n))
        else:
            print('三次输入错误，卡已被冻结')
            card.setFrozen(True)
            return False
        
    '''插入卡片'''
    def insert_card(self,card): 
        self.is_inserted(True)
        if card.getFrozen()==False:
            if self.password_check(card):
                self.__card = card
                self.control()
        else:
            print('该卡已被冻结')
            self.back_card()
            
    '''退卡'''            
    def back_card(self):
        self.__card = None
        self.is_inserted(False)
        
    def getCardNo(self):
        return self.__card.getCno()
    
    def setBalance(self,balance):
        self.__balance = balance
    
    def getBalance(self):
        return self.__balance
    
    def cardBalanceCheck(self,m):
        if m > self.__card.getBalance() or m < 0:
            raise CardNotEnoughBalanceError('账户余额不足') 
            
    def machineBalanceCheck(self,m):
        if m > self.getBalance() or m < 0:
            raise MachineNotEnoughBalanceError('ATM余额不足')
            
    '''主操作界面'''
    def control(self):
        print('''
        -1：退卡
        1：转账
        2：查询余额
        3：取款
        4：存款
        5：修改密码
        ''')
        while True:
            x = input('请输入对应的操作：')
            if x == '-1':
                return self.back_card()
            elif x == '1':
                return self.transfer_accounts()
            elif x == '2':
                return self.query_balance()
            elif x == '3':
                return self.withdraw()
            elif x == '4':
                return self.deposit()
            elif x == '5':
                return self.modify_password()
            
    '''转账操作'''
    def transfer_accounts(self):
        print('''
        -1：退卡
        -2：返回
        ''')
        x = input('请输入转账金额：')
        if x == '-1':
            return self.back_card()
        elif x == '-2':
            return self.control()
        elif x == '' or x == '0':
            return self.transfer_accounts()
        else:
            try:
                x = int(x)
                self.cardBalanceCheck(x)
                while True:
                    print('''
        -2：返回
                    ''')
                    to_cno = input('转予账号：')
                    if to_cno == '-2':
                        return self.transfer_accounts()
                    to_card = Server.get_account(to_cno)
                    if to_card:
                        to_owner = to_card.getOwner().getName()
                        to_owner = to_owner[0]+'*'*(len(to_owner)-1)
                        print('''
        转予账号：%s
        持卡人：%s
        金额：%.2f
    1：确认    -2：返回
                        ''' % (to_cno,to_owner,x))
                        while True:
                            sure = input("请输入指令:")
                            if sure == '-2':
                                break
                            elif sure=='1':
                                to_card.setBalance(to_card.getBalance()+x)
                                self.__card.setBalance(self.__card.getBalance()-x)
                                print('''
        转账成功
                                ''')
                                return self.control()
                    else:
                        print('''
        找不到该用户
                        ''')
            except CardNotEnoughBalanceError as e:
                print('''
        账户余额不足
                ''')
                self.transfer_accounts()
                
    '''查询余额操作'''
    def query_balance(self):  
        while True:
            print('''
        余额：%.2f
    -1：退卡   -2：返回
        ''' % self.__card.getBalance())
            code = input('请输入指令：')
            if code == '-1':
                return self.back_card()
            elif code == '-2':
                return self.control()
            
    '''取款操作'''        
    def withdraw(self):
        print('''
        -1：退卡
        -2：返回
        ''')
        draw = input('请输入取款金额：')
        if draw == '-1':
            return self.back_card()
        elif draw == '-2':
            return self.control()
        elif draw == '' or draw == '0':
            return self.withdraw()
        else:
            try:
                draw = int(draw)
                self.cardBalanceCheck(draw)
                self.machineBalanceCheck(draw)
                print('''
        取款金额：%.2f
    1：确认    -2：返回
                        ''' % draw)
                while True:
                    sure = input("请输入指令:")
                    if sure == '-2':
                        return self.withdraw()
                    elif sure=='1':
                        self.__card.setBalance(self.__card.getBalance()-draw)
                        self.setBalance(self.getBalance()-draw)
                        print('''
        取款成功
                                ''')
                        return self.control()
            except CardNotEnoughBalanceError as e:
                print('''
        账户余额不足
                ''')
                self.withdraw()
            except MachineNotEnoughBalanceError as e:
                print('''
        ATM余额不足
                ''')
                self.withdraw()
                
    '''存款操作'''            
    def deposit(self):
        print('''
        -1：退卡
        -2：返回
        ''')
        deposit_money = input('请将钞票平整放入钞口(最多可放100张，勿夹纸条等异物)：')
        if deposit_money == '-1':
            return self.back_card()
        elif deposit_money == '-2':
            return self.control()
        elif deposit_money == '' or deposit_money == '0':
            return self.deposit()
        else:
            deposit_money = int(deposit_money)
            print('''
        存款金额：%.2f
        失败张数：0
    1：确认    -2：返回
            ''' % deposit_money)
            while True:
                sure = input("请输入指令:")
                if sure == '-2':
                    return self.deposit()
                elif sure=='1':
                    self.__card.setBalance(self.__card.getBalance()+deposit_money)
                    self.setBalance(self.getBalance()+deposit_money)
                    print('''
        存款成功
                    ''')
                    return self.control()
                
    '''修改密码操作'''        
    def modify_password(self):
        print('''
        -1：退卡
        -2：返回
        ''')
        o_password = input('请输入原密码：')
        if o_password == '-1':
            return self.back_card()
        elif o_password == '-2':
            return self.control()
        else:
            if o_password == self.__card.getPassword():
                while True:
                    print('''
        -2：返回
                    ''')
                    n_password = input('请输入新密码：')
                    if n_password == '-2':
                        return self.modify_password()
                    elif o_password == n_password:
                        print('''
        新旧密码重复
                        ''')
                    elif n_password.isdigit() and len(n_password)==6:
                        n_password1 = input('请再次输入新密码：')
                        if n_password == n_password1:
                            self.__card.setPassword(n_password)
                            print('''
        修改成功
                            ''')
                            return self.control()
                        else:
                            print('''
        两次密码不一致
                            ''')
            else:
                print('密码不正确')
                return self.modify_password()
            
'''测试类'''            
class TestATM(object):
    me = User('郑鸿基','18024046167','441640199706262584')#用户对象
    c = Card('01','123456',me)#卡1对象     卡号01 密码123456 拥有者我   
    c1 = Card('02','654321',me)#卡2对象    卡号01 密码654321 拥有者我    
    c.setBalance(10000)#卡1预设10000元
    m = ATMMachine('01',5000)#机器对象     机号01 机内金额 5000
    
                  
    '''测试转账'''    
    def testTransfer(self):
        self.m.insert_card(self.c)#动作1  插入卡1
        self.m.insert_card(self.c)#动作2  插入卡1
        self.m.insert_card(self.c1)#动作3  插入卡2
    
    '''测试冻结或修改密码'''    
    def testFrozen(self):
        self.m.insert_card(self.c)#动作4  插入卡1
        self.m.insert_card(self.c)#动作5  插入卡1
        
    '''
    1.动作1
    2.进行余额查询
    3.进行取款(卡内余额不足  机器余额不足  成功)
    4.进行余额查询
    5.进行存款(然后取出机内所有的钱)
    6.进行余额查询
    7.进行转账
    8.进行余额查询
    9.进行密码修改
    10.退卡 然后重新插入 动作2
    11.测试密码是否修改成功
    12.退卡后 插入卡2 动作3
    13.查询余额  测试转账是否成功
    14.退卡后 插入卡1 动作4
    15.连续输入三次 旧密码 让账户冻结
    16.再次插入卡1 动作5
    '''

t = TestATM()
t.testTransfer()
t.testFrozen()

