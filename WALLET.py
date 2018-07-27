import gi
import sqlite3
import pyqrcode
import requests
import hashlib
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class main:
   
    
    def __init__(self):

        # CONEXÃO COM BD
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()

        #   CRIAÇÃO DE ENTIDADES BD
        def createdatabase():
            conn.execute('CREATE TABLE IF NOT EXISTS user(iduser INTEGER PRIMARY KEY AUTOINCREMENT, idname TEXT, email TEXT, name TEXT, password TEXT, pass TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS wallet(idwallet INTEGER PRIMARY KEY AUTOINCREMENT, publickey text, privatekey text, walletname text, iduser integer, FOREIGN KEY(iduser) REFERENCES user(iduser))')
            conn.execute('CREATE TABLE IF NOT EXISTS contact(idcontact INTEGER PRIMARY KEY AUTOINCREMENT, publickey text, contactname text, iduser integer,FOREIGN KEY(iduser) REFERENCES user(iduser))')
            conn.execute('CREATE TABLE IF NOT EXISTS register(idregister INTEGER PRIMARY KEY AUTOINCREMENT, date date, type text, value real, status text, idcontact integer, idwallet integer, FOREIGN KEY(idwallet) REFERENCES wallet(idwallet), FOREIGN KEY(idcontact) REFERENCES contact(idcontact))')
            
        createdatabase()
        

        # IMPORTANDO ARQUIVO GLADE
        #OBJ INTERFACE GLADE
        builder = Gtk.Builder()
        builder.add_from_file("WALLET-00.glade")

        self.window01 = builder.get_object("window1")
        self.window02 = builder.get_object("window2")
        self.window03 = builder.get_object("window3")
        self.window04 = builder.get_object("window4")
        self.window05 = builder.get_object("window5")
        self.window06 = builder.get_object("window6")
        self.window07 = builder.get_object("window7")
        self.window08 = builder.get_object("window8")
        self.window09 = builder.get_object("window9")

        self.dialog01 = builder.get_object("dialog1")
        self.dialog02 = builder.get_object("dialog2")

        #OBJETOS DE ENTRADA - JANELA DE LOGIN
        self.W1logintext = builder.get_object("entry1")
        self.W1passawordtext = builder.get_object("entry2")
        self.W1statustext = builder.get_object("label70")
        self.W1nametext = builder.get_object("label71")
        self.W1text = builder.get_object("label5")

        self.W1obj1 = builder.get_object("label6")
        self.W1obj2 = builder.get_object("label7")
        self.W1obj3 = builder.get_object("button1")
        self.W1obj4 = builder.get_object("button2")       

        self.img1 = builder.get_object("image10")       

        #OBJETOS DE ENTRADA - JANELA DE REGISTRO
        self.W2statustext = builder.get_object("label57")
        self.W2nametext = builder.get_object("entry17")
        self.W2logintext = builder.get_object("entry4")
        self.W2emailtext = builder.get_object("entry5")
        self.W2passtext = builder.get_object("entry6")
        self.W2passwordtext = builder.get_object("entry7")
        self.W2confirmationtext = builder.get_object("entry8")

        #OBJETOS DE ENTRADA - JANELA DE CONTATOS
        self.W3statustext = builder.get_object("label64") 
        self.W3contactnametext = builder.get_object("entry10")
        self.W3contactpktext = builder.get_object("entry11")

        #OBJETOS DE ENTRADA E SAIDA - JANELA DE NOVA CHAVE
        self.W8publickeytext = builder.get_object("label58")
        self.W8privatekeytext = builder.get_object("label59")        
        self.W8namewallettext = builder.get_object("entry16")
        self.W8statustext = builder.get_object("label1")

        #OBJETOS DE ENTRADA - JANELA DE IMPORTAR CHAVE
        self.W5publickeytext = builder.get_object("entry9")
        self.W5privatekeytext = builder.get_object("entry12")         
        self.W5namewallettext = builder.get_object("entry3")
        self.W5statustext = builder.get_object("label2")

        #OBJETOS DE ENTRADA - JANELA DE BALANÇO
        self.W4selectwallet = builder.get_object("comboboxtext1")
        self.W4totaltext = builder.get_object("label52")

        #OBJETOS DE ENTRADA E SAIDA - JANELA DE RECEBIMENTO
        self.W7selectwallet = builder.get_object("comboboxtext2")
        self.W7address = builder.get_object("label56")
        self.W7img = builder.get_object("image1")

        #OBJETOS DE ENTRADA E SAIDA - JANELA DE PAGAMENTO
        self.W6selectwallet = builder.get_object("comboboxtext3")
        self.W6selectcontact = builder.get_object("comboboxtext4")
        self.W6selectvalue = builder.get_object("spinbutton1")
        self.W6currentbalance = builder.get_object("label47")
        self.W6finalbalance = builder.get_object("label48")
        self.W6statustext = builder.get_object("label3")
        
                        
        #INICIALIZAÇÃO DA JANELA PRINCIPAL
        self.window01.show()
        self.idmaster = ''
        self.myprivatekey = ''
        self.mycontact = ''
        self.currentvalue = 0       

        #EVENTOS DA INTERFACE COM PYTHON
        Handler = {

            #EVENTO DE INICIALIZAÇÃO - LOGIN
            "button_ok_clicked": self.loginApplication,

            #EVENTOS DE CONTROLE E REGISTRO DE USUÁRIO
            "button_register_clicked": self.register,
            "button_registersend_clicked": self.sendRegister,
            "button_registerclose_clicked":self.closeRegister,

            #EVENTOS DE CONTROLE E REGISTRO DE CONTATO - AGENDA
            "button_registercontact_clicked": self.contact,
            "button_contactsend_clicked": self.sendContact,
            "button_contactclose_clicked": self.closeContact,            

            #EVENTOS DE CONTROLE E CRIAÇÃO DE NOVA CARTEIRA
            "button_newkey_clicked": self.newkey,
            "button_newwallet_clicked":self.saveNewWallet,            
            "button_newkeyclose_clicked":self.closeNewkey,

            #EVENTOS DE CONTROLE E IMPORTAÇÃO DE CARTEIRA
            "button_importkey_clicked": self.importkey,
            "button_importwallet_clicked":self.saveImportWallet,
            "button_importkeyclose_clicked":self.closeImportkey,

            #EVENTOS DE CONTROLE E ENVIO DE CRIPTOMOEDAS
            "button_send_clicked": self.send,
            "button_sendsend_clicked":self.sendSend,
            "button_sendclose_clicked":self.closeSend,

            #EVENTOS DE CONTROLE E RECEBIMENTO DE CRIPTOMOEDAS
            "button_receive_clicked": self.receive,
            "button_receiveclose_clicked":self.closeReceive,

            #EVENTOS DE CONTROLE E BALANÇO DE CRIPTOMOEDAS - CARTEIRA
            "button_balance_clicked": self.balance,
            "button_balanceclose_clicked":self.closeBalance,

            #EVENTOS DE CONTROLE E EDIÇÃO DE CARTEIRA
            "button_editkey_clicked": self.editkey,
            "button_editkeyclose_clicked":self.closeEditkey,

            #EVENTOS DE FINALIZAÇÃO DA APLICAÇÃO
            "gtk_main_quit": Gtk.main_quit           
            }
        #CONEXÃO DOS EVENTOS
        builder.connect_signals(Handler)
        
    #***__JANELA WELCOME TO WALLET__***# 
    def loginApplication(self, widget):

        #CAPTURA DE DADOS DE ENTRADA - INTERFACE
        self.W1statustext.set_text("")
        self.W1nametext.set_text("")        
        w1login = self.W1logintext.get_text()
        w1password = self.W1passawordtext.get_text()

        #ENCRIPTAÇÃO MD5 DE SENHA
        p = hashlib.md5()
        p.update(w1password.encode('utf-8'))
        w1password = p.hexdigest()

        #CONEXÃO COM BANCO DE DADOS E CONSULTA SQL PARA VALIDAR LOGIN       
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()
        x = False 
        sql = 'SELECT * FROM user WHERE idname = ? AND password = ?'

        for row in conn.execute(sql, (w1login,w1password,)):
            x = True
            self.W1logintext.set_text("")       
            self.W1passawordtext.set_text("")
            
            self.W1obj1.hide() 
            self.W1obj2.hide() 
            self.W1obj3.hide()
            self.W1obj4.hide()            
            self.W1logintext.hide()      
            self.W1passawordtext.hide()

            self.idmaster = row[0]             
            name = row[3]
            name = name.split()
            name = name[0]
            self.W1text.set_text("Bem Vindo")
            self.W1nametext.set_text(name)
            self.img1.show()
            break
        
        if x == False:
            self.W1statustext.set_text("Atenção: Dados Inválidos! \nTente Novamente!")
            
    #INICIALIZADOR DE JANELA DE REGISTRO DO USUÁRIO
    def register(self, widget):
        self.window02.show()
        
    #INICIALIZADOR DE JANELA DE REGISTRO DO CONTATO
    def contact(self, widget):
        self.window03.show()

    #CONEXÃO COM BANCO DE DADOS E CONSULTA SQL PARA VALIDAR CADASTRO DO USUÁRIO
    def sendRegister(self, widget):
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()
        
        self.W2statustext.set_text("")        
        w2login = self.W2logintext.get_text()
        w2email = self.W2emailtext.get_text()       
        w2name = self.W2nametext.get_text()
        w2password = self.W2passwordtext.get_text()
        w2confirmation = self.W2confirmationtext.get_text()
        w2pass = self.W2passtext.get_text()
        
        w2login_test = w2login.replace(" ", "")        
        w2email_test = w2email.replace(" ", "")
        w2name_test = w2name.replace(" ", "")
        w2password_test = w2password.replace(" ", "")
        w2confirmation_teste = w2confirmation.replace(" ", "")
        w2pass_test = w2pass.replace(" ", "")

        #VERIFICAÇÃO DE CAMPOS EM BRANCO
        if (w2login_test != "") and (w2email_test != "") and (w2name_test != "") and (w2password_test != "") and (w2confirmation_teste != "") and (w2pass_test != ""):

            #VERIFICAÇÃO DA CONFIRMAÇÃO DE SENHA 
            if (w2confirmation == w2password):
                
                x = False
                A = False
                P = False
                E = False
                sql = 'SELECT * FROM user WHERE idname = ?'

                #VERIFICAÇÃO DA VALIDADE DO EMAIL
                for i in w2email:
                    if i == " ":                        
                        E = True
                    if i == "@":
                        A = True
                    if i == ".":
                        P = True
                if (E == True) or (A == False) or (P == False):
                    self.W2statustext.set_text("Atenção: Email Inválido!")
                    x = True
                #VERIFICAÇÃO DA VALIDADE DA PALAVRA-CHAVE    
                for i in w2pass:
                    if i == " ":
                        self.W2statustext.set_text("Atenção: Palavra-Chave Inválida, Remova os Espaços!")
                        x = True
                        
                #VERIFICAÇÃO DA VALIDADE DA LOGIN 
                for i in w2login:
                    if i == " ":
                        self.W2statustext.set_text("Atenção: Login Inválido, Remova os Espaços!")
                        x = True
                        
                #VERIFICAÇÃO DA EXISTENCIA DA LOGIN         
                for row in conn.execute(sql, (w2login,)):                
                    self.W2statustext.set_text("Atenção: Esse Login já possui um Dono!")
                    x = True
                #INSERÇÃO DOS DADOS NO BANCO DE DADOS    
                if x == False:
                    p = hashlib.md5()
                    p.update(w2password.encode('utf-8'))
                    w2password = p.hexdigest()
                    print(w2password)
                    
                    conn.execute('INSERT INTO user (idname, email, name, password, pass) VALUES (?, ?, ?, ?, ?)', (w2login, w2email, w2name, w2password, w2pass))
                    connection.commit()                
                    self.W2statustext.set_text("Usuário Cadastrado com Sucesso!")
                    
                    #REINICIALIZAÇÃO DOS CAMPOS
                    self.W2logintext.set_text("")
                    self.W2emailtext.set_text("")       
                    self.W2nametext.set_text("")
                    self.W2passwordtext.set_text("")
                    self.W2confirmationtext.set_text("")
                    self.W2passtext.set_text("")                
            else:            
                self.W2statustext.set_text("Atenção: Essas Senhas Não Coincidem!")
        else:
            self.W2statustext.set_text("Atenção: Existem Campos em Branco!")
            
    #FINALIZADOR DA JANELA DE REGISTRO DO USUÁRIO
    def closeRegister(self, widget):
        #REINICIALIZAÇÃO DOS CAMPOS
        self.W2logintext.set_text("")
        self.W2emailtext.set_text("")       
        self.W2nametext.set_text("")
        self.W2passwordtext.set_text("")
        self.W2confirmationtext.set_text("")
        self.W2passtext.set_text("")
        self.W2statustext.set_text("")        
        self.window02.hide()

    #CONEXÃO COM BANCO DE DADOS E CONSULTA SQL PARA VALIDAR NOVO CONTATO - AGENDA
    def sendContact(self, widget):
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()
        x = False
        pkValid = True
        contactExist = False
        contactValid = True     
        
        w3contactname = self.W3contactnametext.get_text()       
        w3contactpk = self.W3contactpktext.get_text()

        w3contactname_test = w3contactname.replace(" ", "")        
        w3contactpk_test = w3contactpk.replace(" ", "")

        #VERIFICAÇÃO DE CAMPOS EM BRANCO
        if (w3contactname_test != "") and (w3contactpk_test != ""):

            #VERIFICAÇÃO DA VALIDADE DA CHAVE PUBLICA 
            for i in w3contactpk:
                if i == " ":
                    self.W3statustext.set_text("Atenção: Chave Pública Inválida, Remova os Espaços!")
                    pkValid = False
                    break
                        
            #VERIFICAÇÃO DA EXISTENCIA DO CONTATO
            if pkValid == True:
                sql = 'SELECT * FROM contact WHERE iduser = ? AND contactname = ?'
                for row in conn.execute(sql, (self.idmaster, w3contactname,)):                
                    self.W3statustext.set_text("Atenção: Esse Nome já está Registrado! /nTente Novamente!")
                    contactExist = True
                    break
            if contactExist == False:
                sql = 'SELECT * FROM contact WHERE iduser = ? AND publickey = ?'
                for row in conn.execute(sql, (self.idmaster, w3contactpk,)):                
                    self.W3statustext.set_text("Atenção: Esse Chave Pública já está Registrada! \nTente Novamente!")
                    contactValid = False
                    break
            if contactValid == True:
                conn.execute('INSERT INTO contact (publickey, contactname, iduser) VALUES (?, ?, ?)', (w3contactpk, w3contactname, self.idmaster))
                connection.commit()                
                self.W3statustext.set_text("Contato Cadastrado com Sucesso!")

                #REINICIALIZAÇÃO DOS CAMPOS
                self.W3contactpktext.set_text("")
                self.W3contactnametext.set_text("")
        else:
            self.W3statustext.set_text("Atenção: Existem Campos em Branco!")
            
     #FINALIZADOR DA JANELA CONTATO  
    def closeContact(self, widget):
        self.W3statustext.set_text("")  
        self.W3contactpktext.set_text("")
        self.W3contactnametext.set_text("")
        self.window03.hide()
        
    #JANELA DE NOVA CARTEIRA 
    def newkey(self, widget):        
        url = 'https://moeda.ucl.br'
        #wallet = KeyPair()
        #publickey = wallet.public_key
        #privatekey = wallet.private_key
        #wallet = KeyPair(f'{privatekey}')

        #self.W8publickeytext.set_text(publickey)
        #self.W8privatekeytext.set_text(privatekey)
        self.window08.show()
        
    #CONEXÃO COM BANCO DE DADOS E CONSULTA SQL PARA VALIDAR CARTEIRA    
    def saveNewWallet(self, widget):
        nameWallet = self.W8namewallettext.get_text()
        nameWallet_teste = nameWallet.replace(" ", "")
        if (nameWallet_teste == ""):
            self.W8statustext.set_text("Atenção! O Nome da Carteira não poder ser Vazio")
        else:
            connection = sqlite3.connect('walletdata.db')
            conn = connection.cursor()
            conn.execute('INSERT INTO wallet (publickey, privatekey, walletname, iduser) VALUES (?, ?, ?, ?)', (self.W8publickeytext, self.W8privatekeytext, nameWallet, self.idmaster))
            connection.commit()                
            self.W8statustext.set_text("Carteira Salva com Sucesso!")
            
    #JANELA DE IMPORTAÇÃO DE CARTEIRA    
    def importkey(self, widget):        
        self.window05.show()
        
    #CONEXÃO COM BANCO DE DADOS E CONSULTA SQL PARA VALIDAR IMPORTAÇÃO
    def saveImportWallet(self, widget):
        publickey = self.W5publickeytext.get_text()
        privatekey = self.W5privatekeytext.get_text()         
        nameWallet = self.W5namewallettext.get_text()

        publickey_test = publickey.replace(" ", "")
        privatekey_test = privatekey.replace(" ", "")
        wallet_test = nameWallet.replace(" ", "")

        if (publickey_test == "") or (privatekey_test == "") or (wallet_test == ""):
            self.W5statustext.set_text("Atenção! Todos Campos devem ser Preenchidos")
        else:
            connection = sqlite3.connect('walletdata.db')
            conn = connection.cursor()
            conn.execute('INSERT INTO wallet (publickey, privatekey, walletname, iduser) VALUES (?, ?, ?, ?)', (publickey, privatekey, nameWallet, self.idmaster))
            connection.commit()                
            self.W5statustext.set_text("Carteira Salva com Sucesso!")
            self.W5publickeytext.set_text("")
            self.W5privatekeytext.set_text("")         
            self.W5namewallettext.set_text("")  
            
    #JANELA DE RECEBIMENTO DE CRIPTOMOEDAS                 
    def receive(self, widget):        
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()
        x = False
        indice = 0
        sql = 'SELECT * FROM wallet WHERE iduser = ?'
        self.W7selectwallet.append(str(indice), 'Selecione uma Carteira')

        qr_code = pyqrcode.create('QRCODE')
        qr_code.png('code.png', scale=4)
        self.W7img.set_from_file("code.png")

        for row in conn.execute(sql, (self.idmaster,)):
            x = True
            indice = indice + 1
            self.W7selectwallet.append(str(indice), row[3])
            
        if x == False:
            self.W7selectwallet.append(str(indice), 'Nenhuma Carteira Encontrada')           
            
        self.W7selectwallet.set_active(0)
        self.W7selectwallet.connect("changed", self.selectedportfolio_receive)
               
        self.window07.show()
        
    #CONTROLE DO COMBOBOX - CARTEIRAS
    def selectedportfolio_receive(self, combo):
        wallet = combo.get_active_text()
        publickey = ''
       
        if (wallet == 'Selecione uma Carteira') or (wallet == 'Nenhuma Carteira Encontrada'):
            self.W7address.set_text("***")

            #GERADOR DE QRCODE
            qr_code = pyqrcode.create('GUILHERME')
            qr_code.png('code.png', scale=4)
            self.W7img.set_from_file("code.png")
            
        else:            
            connection = sqlite3.connect('walletdata.db')
            conn = connection.cursor()        
            sql = 'SELECT * FROM wallet WHERE iduser = ? AND walletname = ?'

            for row in conn.execute(sql, (self.idmaster,wallet,)):
                publickey = row[1]
                break
                      
            self.W7address.set_text(publickey)
            qr_code = pyqrcode.create(publickey)
            qr_code.png('code.png', scale=4)            
            self.W7img.set_from_file("code.png")
            
    #JANELA DE ENVIO DE CRIPTOMOEDAS
    def send(self, widget):
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()

        #SELETOR DE CARTEIRA - COMBOBOX
        x = False
        indiceX = 0
        sql = 'SELECT * FROM wallet WHERE iduser = ?'
        self.W6selectwallet.append(str(indiceX), 'Selecione uma Carteira')

        for row in conn.execute(sql, (self.idmaster,)):
            x = True
            indiceX = indiceX + 1
            self.W6selectwallet.append(str(indiceX), row[3])
            
        if x == False:
            indiceX = indiceX + 1
            self.W6selectwallet.append(str(indiceX), 'Nenhuma Carteira Encontrada')           
            
        self.W6selectwallet.set_active(0)
        self.W6selectwallet.connect("changed", self.selectedportfolio_send)

        #SELETOR DE CONTATO - COMBOBOX
        y = False
        indiceY = 0
        sql = 'SELECT * FROM contact WHERE iduser = ?'
        self.W6selectcontact.append(str(indiceY), 'Selecione um Contato')

        for row in conn.execute(sql, (self.idmaster,)):
            y = True
            indiceY = indiceY + 1
            self.W6selectcontact.append(str(indiceY), row[2])
            
        if x == False:
            indiceY = indiceY + 1
            self.W6selectcontact.append(str(indiceY), 'Nenhuma Contato Encontrado')           
            
        self.W6selectcontact.set_active(0)
        self.W6selectcontact.connect("changed", self.selectedcontact_send)
        
        self.window06.show()
        
    #CONTROLADOR DO COMBOBOX 
    def selectedportfolio_send(self, combo):
        wallet = combo.get_active_text()
        publickey = ''
       
        if (wallet != 'Selecione uma Carteira') or (wallet != 'Nenhuma Carteira Encontrada'):           
            connection = sqlite3.connect('walletdata.db')
            conn = connection.cursor()        
            sql = 'SELECT * FROM wallet WHERE iduser = ? AND walletname = ?'

            for row in conn.execute(sql, (self.idmaster,wallet,)):
                #DECRIPTAÇÃO DE CHAVE PRIVADA
                self.myprivatekey = row[2]
                publickey = row[1]
                
                print(self.myprivatekey)
                break
            
            url = 'https://moeda.ucl.br/balance/'
            res = requests.get(url+publickey)            
            res = res.json()            
            balance = res['balance']            
            self.W6currentbalance.set_text(str('%.2f' % balance))
            self.currentvalue = balance
            self.W6selectvalue.connect(self.calculation)
        else:
            publickey = ''
            self.W6currentbalance.set_text('0.00')
            
    def calculation(self):
        value = self.W6selectvalue.get_value()
        calc = self.currentvalue - value
        self.W6finalbalance.set_text(str('%.2f' % calc))
        
            
    def selectedcontact_send(self, combo):
        contact = combo.get_active_text()
       
        if (contact != 'Selecione um Contato') or (contact != 'Nenhuma Contato Encontrado'):           
            connection = sqlite3.connect('walletdata.db')
            conn = connection.cursor()        
            sql = 'SELECT * FROM contact WHERE iduser = ? AND contactname = ?'

            for row in conn.execute(sql, (self.idmaster,contact,)):
                self.mycontact = (row[0], row[1], row[2])
                print(self.mycontact[1])
                break
    #REQUEST DE TRANSAÇÃO        
    def sendSend(self, widget):
        publickey = self.mycontact[1]
        privatekey = self.myprivatekey 
        value = self.W6selectvalue.get_value()
        url = 'https://moeda.ucl.br/transaction'
        res = requests.post(url +'/'+ privatekey +'/'+ privatekey +'/'+ str(value))

        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()
        conn.execute('INSERT INTO register (date, type, value, status, idcontact, idwallet) VALUES (?, ?, ?, ?, ?, ?)',(data, 'Envio', value, '',  ))
                
    #JANELA DE BALANÇO DE SALDOS - CARTEIRA                   
    def balance(self, widget):
        connection = sqlite3.connect('walletdata.db')
        conn = connection.cursor()
        x = False
        indice = 0
        sql = 'SELECT * FROM wallet WHERE iduser = ?'
        self.W4selectwallet.append(str(indice), 'Selecione uma Carteira')

        for row in conn.execute(sql, (self.idmaster,)):
            x = True
            indice = indice + 1
            self.W4selectwallet.append(str(indice), row[3])
            
        if x == False:
            self.W4selectwallet.append(str(indice), 'Nenhuma Carteira Encontrada')           
            
        self.W4selectwallet.set_active(0)
        self.W4selectwallet.connect("changed", self.selectedportfolio)
               
        self.window04.show()
    def selectedportfolio(self, combo):
        wallet = combo.get_active_text()
        publickey = ''
        url = ''
        res = ''
        
        if (wallet == 'Selecione uma Carteira') or (wallet == 'Nenhuma Carteira Encontrada'):
            url = ''
            res = ''
            self.W4totaltext.set_text("0.00")
        else:            
            connection = sqlite3.connect('walletdata.db')
            conn = connection.cursor()        
            sql = 'SELECT * FROM wallet WHERE iduser = ? AND walletname = ?'

            for row in conn.execute(sql, (self.idmaster,wallet,)):
                publickey = row[1]
                break
            url = 'https://moeda.ucl.br/balance/'
            res = requests.get(url+publickey)
            res = res.json()            
            balance = res['balance']
            self.W4totaltext.set_text(str('%.2f' % balance))

    #JANELA DE ENCERRAMENTO NOVA CARTEIRA
    def closeNewkey(self, widget):
        self.W8publickeytext.set_text("***")
        self.W8privatekeytext.set_text("***")
        self.W8statustext.set_text("")
        self.window08.hide()

    #JANELA  DE ENCERRAMENTO DE IMPORTAÇÃO DE CARTEIRA
    def closeImportkey(self, widget):
        self.W5statustext.set_text("")
        self.W5publickeytext.set_text("")
        self.W5privatekeytext.set_text("")         
        self.W5namewallettext.set_text("")        
        self.window05.hide()

    #JANELA DE ENCERRAMENTO DE ENVIO DE CRIPTOMOEDAS
    def closeSend(self, widget):
        self.W6selectwallet.remove_all() 
        self.W6selectcontact.remove_all() 
        self.W6selectvalue.set_value(0)
        self.W6currentbalance.set_text("0.00")
        self.W6finalbalance.set_text("0.00")
        self.W6statustext.set_text("")
        self.window06.hide()

    #JANELA DE ENCERRAMENTO DE RECEBIMENTO DE CRIPTOMOEDAS
    def closeReceive(self, widget):
        print('close')
        self.W7address.set_text('***')
        self.W7selectwallet.remove_all()        
        self.window07.hide()

    #JANELA DE ENCERRAMENTO DE BALANÇO DE SALDO - CARTEIRA
    def closeBalance(self, widget):
        self.W4totaltext.set_text('0.00')
        self.W4selectwallet.remove_all()        
        self.window04.hide()
        
    #JANELA DE EDIÇÃO DE CARTEIRA    
    def editkey(self, widget):
        self.window04.hide()
        self.window09.show()

    #JANELA DE ENCERRAMENTO DE EDIÇÃO DE CARTEIRA
    def closeEditkey(self, widget):        
        self.window09.hide()
    
        
        


if __name__ == "__main__":
    application = main()
    Gtk.main()
    



