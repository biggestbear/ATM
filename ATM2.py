# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 13:17:50 2017

@author: hp
"""
'''
参照生活中的ATM存取款机，
编写程序，模拟用户进行ATM常用操作。如插卡，退卡，输入密码，
查询余额，存款，取款，转账等常用操作。
输出格式以打印控制台输出
'''

import getpass

class Bank_Card:
     cardID = 0    
     cardPWD = '123'      
     balance = 0  
     userName = ' '  
     def __init__(self,cardID,cardPWD,userName,balance): 
         self.cardID = cardID 
         self.cardPWD = cardPWD 
         self.userName = userName 
         self.balance = balance

         
class ATM: 
    #存款
    def deposite(self,card): 
        divide()
        print('存款\n'.center(50))
        cash=int(input("存款金额为100的倍数,金额要求在100-10000之间:\n"))
        if cash%100==0 and cash>0 and cash<=10000:
            card.balance=cash+card.balance
            divide()
            print("存款成功\n".center(50))
            print("\n余额 :",card.balance)
        else:
            divide()
            print('存款失败\n'.center(50))
        divide()
        
    #取款    
    def withdraw(self,card):
       divide() 
       print("取款\n".center(50))
       money=int(input('取款金额为100的倍数,金额要求在100-10000之间：\n'))
       if money%100==0 and money<card.balance and money>0 and card.balance>100:
          card.balance=card.balance-money
          divide()
          print('取款成功\n'.center(50))
          print("\n余额:",card.balance)
       else:
            divide()
            print('\n取款失败'.center(50))
       divide()
     
    #转账
    def transfer(self,card):
       divide()
       print("转账\n".center(50))
       #userid=int(input('转账的卡号:\n'))
       gold=int(input('转账的金额最多50000：\n'))
       if gold<card.balance and gold>0:
          card.balance=card.balance-gold
          divide()
          print('转账成功\n'.center(50))
          print("余额:",card.balance)
       else:
            divide()
            print('转账失败\n'.center(50))
       divide()
     
    #查询
    def query(self,card): 
       divide()
       print("查询成功\n".center(50))
       print('银行卡信息'.center(50))
       print('%-10s%-10s%-10s'%('卡号','姓名','余额'))
       print('%-11s%-11s%-11s'%(str(card.cardID),card.userName,str(card.balance)))
       divide()
     
    #退卡
    def refundCard(self,card):
       divide()
       print('谢谢使用，请收好您的卡片')
       divide()
 
      
def divide():
    print("\n--------------------------------------------------\n")
         

def createCard():
    choice=input('请选择一张银行卡（1~3）:')
    if int(choice) == 1:
        newcard = Bank_Card(101,'123','张三',10000)
        add(newcard)
    elif int(choice) == 2:
        newcard = Bank_Card(102,'123','老王',20000)
        add(newcard)
    elif int(choice) == 3:
        newcard = Bank_Card(103,'123','李四',30000)
        add(newcard)
    else:
        print('输入信息有误')
        
def add(card):
    divide()
    
    print('\n        卡已插入')
    divide()
    sum=0
    pwd=''
    while pwd!=card.cardID:
        pwd=getpass.getpass('\n请输入密码：')
        sum=sum+1
        if pwd==card.cardPWD:
            break
        else:
             print('密码错误次数%d,请重新输入密码'%sum)
             if sum>2:
                print('\n密码错误次数过多,退出系统')
                exit()
    print('\n 密码正确，进入系统')
    divide()
    A=ATM()
    menu(A,card)
    
def init():
    f=open('D:\\a.txt','w')
    info='''\
   101 123 张三 10000
   102 123 老王 20000
   103 123 李四 30000'''
    f.write(info)
    f.close()
    s=open('D:\\a.txt','r')
    print('银行卡信息'.center(50))
    print('%-10s%-10s%-10s%-10s'%('卡号','密码','姓名','余额'))
    for line in s.readlines():
        for i in range(0,4):
            print('%-11s'%line.split()[i],end ='')
            if i==3:
                print()
    s.close
    divide()
    return

def start():
    divide()
    print('欢迎使用')
    divide()
    init()
    createCard()
    
def menu(A,card):
    options={1:'查询账户信息',2:'存款',3:'取款',4:'转账',5:'退卡'} 
    for i in options.items():
        print(i[0],i[1])
    choice=int(input("\n请输入（1-5）："))
    if choice==1:
        A.query(card)
        menu(A,card)
    elif choice==2:
        A.deposite(card)
        menu(A,card)    
    elif choice==3:
        A.withdraw(card)
        menu(A,card)   
    elif choice==4:
        A.transfer(card)
        menu(A,card)
    elif choice==5:
        A.refundCard(card)
    else:
        print('错误')
        menu(A,card)
    
def main():
    start()
    
if __name__ == "__main__":  
    main()       
    
