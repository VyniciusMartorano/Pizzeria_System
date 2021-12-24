from grafico.janela_interface import Janela
from PyQt5.QtWidgets import *
import sys
from datetime import datetime
from dados.pizzas import catalogo
from sistema.write_file import cria_pdf_preparo, cria_pdf_entrega
from sistema.base_folders import base_folders
from sistema.create_table import create_table
from sistema.base_de_dados.copy_file_dados import copy_file
from sistema.base_de_dados.write_in_table import write_in_table
from sistema.base_de_dados.get_id import atual_id
import sqlite3
import getpass
from sistema.mounth_verify import verify_mounth
from sistema.print_file import imprimir


class Functions(QMainWindow):
    def __init__(self,*args,**argvs):
        super(Functions,self).__init__(*args,**argvs)
        self.ui = Janela()
        self.ui.setupUi(self)

        base_folders()
        self.current_time()
        create_table()
        copy_file()

        self.seta_id()
        #recebe o ultimo id da base de dados
        self.id = atual_id()

        #chaves de valor
        self.preco_refri = 0
        self.preco_pizza = 0
        self.preco_entrega = 0
        self.desconto = 0

        #lista que guarda os erros
        self.errors = []
        #chave que libera a impressão
        self._keymaster = False

        #
        #condicionais
        #

        #
        #Comands
        #
        #seta a data do dia
        self.ui.label_data_pedido.setText(f'{self.getTime("d")}/{self.getTime("m")}/{self.getTime("Y")}')
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.infos_cliente)
        self.ui.pushButton_novo_pedido.clicked.connect(self.limpa_campos)
        self.ui.frame_erro.hide()

        #COMANDOS WIDGETLIST PIZZAS
        self.ui.pushButton_pizzas_add_na_lista.clicked.connect(self.add_in_listWidget)
        self.ui.pushButton_pizzas_deletar_item.clicked.connect(self.dell_in_listWidget)
        self.ui.pushButton_pizzas_novo_item.clicked.connect(self.novo_item_listWidget)

        #COMANDOS WIDGETLIST REFRIGERANTES
        self.ui.pushButton_refri_add_na_lista.clicked.connect(self.add_item_widgetlist_refri)
        self.ui.pushButton_refri_novo_item.clicked.connect(self.new_item_widgetlist_refri)
        self.ui.pushButton_refri_deletar_item.clicked.connect(self.delete_item_widgetlist_refri)

        #FECHAR FRAME DE ERRO QUANDO CLICADO
        self.ui.Pushbutton_close_erro.clicked.connect(self.hide_frame_error)

        #CALCULAR VALORES DA WIDGETLIST QUANDO O BOTAO DE ADICIOANR ELEMENTO É CLICADO
        #( REMOVER ESTA LINHA DE CODIGO DEPOIS E COLOCAR SOMENTE QUANDO O PEDIDO FOR FINALIZAR  )
        self.ui.pushButton_pizzas_add_na_lista.clicked.connect(self.calcula_widgetBox_pizza)
        self.ui.pushButton_pizzas_deletar_item.clicked.connect(self.calcula_widgetBox_pizza)


        self.ui.pushButton_finalizar_pedido.clicked.connect(self.format_text_desconto)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.format_text_troco)

        self.ui.pushButton_refri_add_na_lista.clicked.connect(self.get_price_refri_box)
        self.ui.pushButton_refri_deletar_item.clicked.connect(self.get_price_refri_box)


        self.ui.pushButton_pizzas_add_na_lista.clicked.connect(self.get_total_value)
        self.ui.pushButton_pizzas_deletar_item.clicked.connect(self.get_total_value)
        self.ui.pushButton_refri_add_na_lista.clicked.connect(self.get_total_value)
        self.ui.pushButton_refri_deletar_item.clicked.connect(self.get_total_value)

        self.ui.pushButton_pizzas_add_na_lista.clicked.connect(self.delivery_price)
        self.ui.pushButton_pizzas_deletar_item.clicked.connect(self.delivery_price)
        self.ui.pushButton_refri_add_na_lista.clicked.connect(self.delivery_price)
        self.ui.pushButton_refri_deletar_item.clicked.connect(self.delivery_price)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.delivery_price)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.price_desconto)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.get_total_value)

        self.ui.pushButton_finalizar_pedido.clicked.connect(self.calcula_widgetBox_pizza)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.get_price_refri_box)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.write_in_folders)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.validated)

        self.ui.pushButton_pizzas_add_na_lista.clicked.connect(self.call_errors)
        self.ui.pushButton_pizzas_deletar_item.clicked.connect(self.call_errors)

        self.ui.pushButton_finalizar_pedido.clicked.connect(self.format_text_desconto)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.format_text_troco)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.write_in_database)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.seta_id)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.verify_database)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.call_errors)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.infos_cliente)
        self.ui.pushButton_finalizar_pedido.clicked.connect(self.current_time)

        self.ui.pushButton_refri_add_na_lista.clicked.connect(self.call_errors)
        self.ui.pushButton_pizzas_add_na_lista.clicked.connect(self.get_total_value)

    #
    #FUNCTIONS
    #

    def seta_id(self):
        self.id = atual_id()
        self.ui.label_numero_pedido.setText(self.id)

    def write_in_database(self):
        nome = self.ui.line_edit_nome_cliente.text().title()
        telefone = self.ui.line_edit_telefone_cliente.text()
        hora = self.ui.label_hora_pedido.text()
        entrega = self.ui.comboBox_local_entrega.currentText()
        forma_pagamento = self.ui.comboBox_forma_pagamento.currentText()
        valor_total = self.ui.label_valor_total.text().split()
        valor_total = float(valor_total[1])
        if self._keymaster == True:
            write_in_table(nome,telefone,hora,entrega,forma_pagamento,valor_total)

    def verify_database(self):
        #verificar se tem algum nome e telefone igual na base de dados iguais aos atuais
        #se existir dar um append na self.errors
        last_day = self.getTime('d')
        last_mounth = verify_mounth(self.getTime('m'))
        user = getpass.getuser()

        conection = sqlite3.connect(fr'C:\Users\{user}\Documents\Mister_Massas_LOG\base_directory\{last_mounth}\{last_day}\dados{last_day}.db')
        cursor = conection.cursor()
        comand = 'SELECT nome, telefone FROM clientes'
        cursor.execute(comand,)
        for item in cursor.fetchall():
            name, tell = item
            if name == self.ui.line_edit_nome_cliente.text().title() and tell == self.ui.line_edit_telefone_cliente.text():
                self.errors.append('Pedido concluido. Faça uma nova comanda')
                cursor.close()
                conection.close()
                return
        cursor.close()
        conection.close()

    def write_in_folders(self):
        nome_cliente = self.ui.line_edit_nome_cliente.text().title()
        telefone_cliente = self.ui.line_edit_telefone_cliente.text()
        endereco_cliente = self.ui.line_edit_endereco_cliente.text().title()
        local_cliente = self.ui.comboBox_local_entrega.currentText()
        numero_da_casa = self.ui.lineEdit_numero_da_casa.text()
        ponto_de_referencia = self.ui.lineEdit_ponto_referencia.text().title()
        if ponto_de_referencia == '':
            ponto_de_referencia = 'NÃO INFORMADO'
        observacoes = self.getText()
        hora_pedido = f'{self.getTime("H")}h{self.getTime("M")}'
        data_pedido = f'{self.getTime("d")}/{self.getTime("m")}/{self.getTime("Y")}'
        troco = self.ui.lineEdit_troco.text()
        user = getpass.getuser()
        current_day = self.getTime('d')
        current_mounth = verify_mounth(self.getTime('m'))
        if troco == None:
            troco = 'R$ 0.00'
        valor_total = self.ui.label_valor_total.text()
        forma_pagamento = self.ui.comboBox_forma_pagamento.currentText()


        if self._keymaster == True:
            carrinho_pizzas = []
            carrinho_refri = []
            self.seta_id()

            for index in range(self.ui.list_view_pizzas.count()):
                carrinho_pizzas.append(self.ui.list_view_pizzas.item(index).text())
            for index in range(self.ui.listView_refrigerantes_lista_de_itens.count()):
                carrinho_refri.append(self.ui.listView_refrigerantes_lista_de_itens.item(index).text())
            cria_pdf_preparo(self.id,hora_pedido,nome_cliente,carrinho_pizzas,carrinho_refri,endereco_cliente,numero_da_casa,observacoes)
            cria_pdf_entrega(self.id,hora_pedido,nome_cliente,local_cliente,telefone_cliente,endereco_cliente,numero_da_casa,ponto_de_referencia,
                             troco,valor_total,forma_pagamento,carrinho_refri)
            try:
                imprimir(fr'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Entregas\{current_mounth}\{current_day}\comanda_entrega{self.id}.pdf')
                imprimir(fr'C:\Users\{user}\Documents\Mister_Massas_LOG\Pdfs\Comanda\{current_mounth}\{current_day}\comanda{self.id}.pdf')
            except:
                ...

    def current_time(self):
        hour = self.getTime('H')
        minute = self.getTime('M')
        self.ui.label_hora_pedido.setText(f'{hour}:{minute}')


    def call_errors(self):
        """
        Organiza todos os erros numa lista
        Se existirem erros na lista ele exibe um erro por vez
        Se não existirem erros ele retorna a keymaster True
        :return:
        """
        self._keymaster = False
        self.calcula_widgetBox_pizza()
        self.infos_cliente()
        self.verify_database()
        lista_erros = self.errors
        if len(lista_erros) > 0:
            for erro in lista_erros:
                self.ui.label_error.setText(erro)
                self.ui.frame_erro.show()
                self.errors = []
                self._keymaster = False
                return
        else:
            self._keymaster = True


    def validated(self):
        if self._keymaster == True:
            self.ui.label_error.setText('Pedido Finalizado com sucesso')
            self.ui.frame_erro.setStyleSheet(
                "border-radius: 8px;\n"
                "background-color: rgb(70,221,55);")
            self.ui.frame_erro.show()
        elif self._keymaster == False:
            self.ui.frame_erro.setStyleSheet(
                "border-radius: 8px;\n"
                "background-color: rgb(255, 32, 32);")


    #calcula_widgetBox_pizza calcula o valor total da box
    #retorna o valor total da box
    def calcula_widgetBox_pizza(self):
        carrinho = []
        valor_total = 0
        for index in range(self.ui.list_view_pizzas.count()):
            carrinho.append(self.ui.list_view_pizzas.item(index).text())
        if len(carrinho) < 1:
            self.errors.append('Nenhuma pizza adicionada')
            self.preco_pizza = 0
            return

        for item in carrinho:
            separa_str = item.split()
            if len(separa_str) == 8:
                valor_total += float(separa_str[7])

            if len(separa_str) == 7:
                valor_total += float(separa_str[6])

            if len(separa_str) == 9:
                valor_total += float(separa_str[8])

            if len(separa_str) == 12:
                valor_total += float(separa_str[11])

            if len(str(valor_total)) == 10:
                self.ui.label_valor_total.setStyleSheet(
                'font-size: 22px;\n'
                'font-weight: bold;')
            else:
                self.ui.label_valor_total.setStyleSheet(
                    'font-size: 26px;\n'
                    'font-weight: bold;')
        self.preco_pizza = valor_total

    def get_price_refri_box(self):
        #puxa os valores da box dos refris
        carrinho = []
        valor_total = 0
        for index in range(self.ui.listView_refrigerantes_lista_de_itens.count()):
            carrinho.append(self.ui.listView_refrigerantes_lista_de_itens.item(index).text())

        for item in carrinho:
            str_split = item.split()
            valor = float(str_split[3])
            valor_total += valor
        self.preco_refri = valor_total

    def get_total_value(self):
        total = self.preco_pizza + self.preco_refri + self.preco_entrega - self.desconto
        total = self.money_format(total)
        return self.ui.label_valor_total.setText(total)

    def getTime(self,mode):
        """
        :param mode: H = Hour, M = Minute, d = dia, m = Mounth, Y = Year.
        :return: hour or minute or day or mounth or year
        """
        time = ''
        if mode == 'H':
            time = datetime.now().strftime('%H')
            return time
        if mode == 'M':
            time = datetime.now().strftime('%M')
            return time
        if mode == 'S':
            time =datetime.now().strftime('%S')
            return time
        if mode == 'd':
            time = datetime.now().strftime('%d')
            return time
        if mode == 'm':
            time = datetime.now().strftime('%m')
            return time
        if mode == 'Y':
            time = datetime.now().strftime('%Y')
            return time
        else:
            return print('Argumento irregular')

    def infos_cliente(self):
        """
        Campos de informação do cliente
        :return:
        """
        nome_cliente = self.ui.line_edit_nome_cliente.text()
        telefone_cliente = self.ui.line_edit_telefone_cliente.text()
        endereco_cliente = self.ui.line_edit_endereco_cliente.text()
        local_cliente = self.ui.comboBox_local_entrega.currentText()
        numero_da_casa = self.ui.lineEdit_numero_da_casa.text()
        ponto_de_referencia = self.ui.lineEdit_ponto_referencia.text()
        observacoes = self.getText()
        hora_pedido = f'{self.getTime("H")}:{self.getTime("M")}'
        data_pedido = f'{self.getTime("d")}/{self.getTime("m")}/{self.getTime("Y")}'

        if nome_cliente == '':
            self.errors.append('Nome vazio')

        if telefone_cliente == '':
            self.errors.append('Telefone vazio')

        if telefone_cliente != '':
            text = ''
            try:
                text = int(telefone_cliente)
            except:
                self.errors.append('Telefone precisar ser numérico')

        if endereco_cliente == '':
            self.errors.append('Endereço vazio')

        if numero_da_casa == '':
            self.errors.append('Numero da casa vazio')


    def limpa_campos(self):
        #
        #campos de informações do cliente
        #
        self.ui.line_edit_nome_cliente.setText('')
        self.ui.line_edit_telefone_cliente.setText('')
        self.ui.line_edit_endereco_cliente.setText('')
        self.ui.comboBox_local_entrega.currentText()
        self.ui.lineEdit_numero_da_casa.setText('')
        self.ui.lineEdit_ponto_referencia.setText('')
        self.ui.textEdit_observacoes.setText('')
        self.ui.comboBox_local_entrega.setCurrentIndex(0)
        #
        #campos de escolha de sabores e etc
        #
        self.ui.comboBox_tamanho_pizza.setCurrentIndex(0)
        self.ui.comboBox_1_sabor.setCurrentIndex(0)
        self.ui.comboBox_2_sabor.setCurrentIndex(0)
        self.ui.comboBox_3_sabor.setCurrentIndex(0)
        self.ui.comboBox_borda.setCurrentIndex(0)
        self.ui.comboBox_refrigerante_opcao.setCurrentIndex(0)
        self.ui.comboBox_forma_pagamento.setCurrentIndex(1)
        self.ui.lineEdit_desconto.setText('')
        self.ui.lineEdit_troco.setText('')
        self.ui.lineEdit_refrigerante_quantidade.setText('')
        self.ui.label_valor_total.setText('R$ 0.00')
        self.ui.label_hora_pedido.setText(f'{self.getTime("H")}:{self.getTime("M")}')
        self.ui.list_view_pizzas.clear()
        self.ui.listView_refrigerantes_lista_de_itens.clear()
        self.hide_frame_error()
        self.current_time()
        self.seta_id()
        self.preco_pizza = 0
        self.preco_refri = 0
        self.preco_entrega = 0
        self.desconto = 0
        self._keymaster = False

    #
    #LISTWIDGET REFRIS DEFS
    #
    def new_item_widgetlist_refri(self):
        """
        zera os campos de refrigerante
        :return:
        """
        self.ui.comboBox_refrigerante_opcao.setCurrentIndex(0)
        self.ui.lineEdit_refrigerante_quantidade.setText('')

    def add_item_widgetlist_refri(self):
        """
        Adiciona na widgetlist o texto da combo box
        :return:
        """
        if self.ui.comboBox_refrigerante_opcao.currentText() != 'Nenhum'\
                and self.ui.lineEdit_refrigerante_quantidade.text() != '':
            try:
                refrigerante_quantidade = int(self.ui.lineEdit_refrigerante_quantidade.text())
            except:
                self.errors.append('O campo "QUANTIDADE" deve ser numérico')
            else:
                self.ui.frame_erro.hide()
                valor = refrigerante_quantidade * 8
                text = f'{self.ui.comboBox_refrigerante_opcao.currentText():<49}{self.ui.lineEdit_refrigerante_quantidade.text():<38}' \
                       f'R$ {valor:.2f}'
                self.ui.listView_refrigerantes_lista_de_itens.addItem(text)
        else:
            self.errors.append('Selecione o refrigerante e a quantidade')

    def delete_item_widgetlist_refri(self):
        """
        deleta o item selecionado na widget list
        :return:
        """
        self.ui.listView_refrigerantes_lista_de_itens.takeItem(self.ui.listView_refrigerantes_lista_de_itens.currentRow())

    #
    #LISTWIDGET PIZZAS DEFS
    #
    def novo_item_listWidget(self):
        """
        zera todas as combo box do pedido
        :return:
        """
        self.ui.comboBox_tamanho_pizza.setCurrentIndex(0)
        self.ui.comboBox_1_sabor.setCurrentIndex(0)
        self.ui.comboBox_2_sabor.setCurrentIndex(0)
        self.ui.comboBox_3_sabor.setCurrentIndex(0)
        self.ui.comboBox_borda.setCurrentIndex(0)

    def dell_in_listWidget(self):
        """
        deleta o item selecionado na Widget list das pizzas
        :return:
        """
        self.ui.list_view_pizzas.takeItem(self.ui.list_view_pizzas.currentRow())

    def add_in_listWidget(self):
        """
        adiciona o texto das comboBox a Widget list
        :return:
        """
        #15 letras na comboBox

        tam = self.ui.comboBox_tamanho_pizza.currentText()
        sabor_1 = self.ui.comboBox_1_sabor.currentText()
        sabor_2 = self.ui.comboBox_2_sabor.currentText()
        sabor_3 = self.ui.comboBox_3_sabor.currentText()
        borda = self.ui.comboBox_borda.currentText()
        preco = ''

        #FORMATAR TEXTO DA LISTWIDGET

        if sabor_1 == 'Nenhum':
            sabor_1 = ''

        if sabor_2 == 'Nenhum':
            sabor_2 = ''

        if sabor_3 == 'Nenhum':
            sabor_3 = ''

        x = len(sabor_1)
        y = len(sabor_2)
        z = len(sabor_3)
        if x > 15:
            x = 17
        if y > 15:
            y = 17
        if z > 15:
            z = 17

        if sabor_1 != '' and sabor_2 == '' and sabor_3 == '':
            if borda != 'Sem_borda' and tam == 'Broto':
                self.errors.append('Broto não pode borda')
                return
            if tam == 'Broto' and borda == 'Sem_borda':
                lista = []
                valor_total = 0
                for index in range(self.ui.list_view_pizzas.count()):
                    lista.append(self.ui.list_view_pizzas.item(index).text())
                if len(lista) < 1:
                    self.errors.append('Adicione outra além da broto')
                    return
            text = f'{tam} |  {sabor_1[0:x]}  | ({borda}) | R$ {self.precifica()}'
            self.ui.frame_erro.hide()
            return self.ui.list_view_pizzas.addItem(text)

        if tam == 'G' and sabor_1 != '' and sabor_2 == '' and sabor_3 == '':
            text = f'{tam} |  {sabor_1[0:x]}  | ({borda}) | {self.precifica()}'
            self.ui.frame_erro.hide()
            return self.ui.list_view_pizzas.addItem(text)

        if tam == 'G' and sabor_1 != '' and sabor_2 != '' and sabor_3 != '':
            self.errors.append('3º sabor apenas na GG')
            return

        if tam == 'M' and sabor_1 != '' and sabor_2 != '' and sabor_3 != '':
            self.errors.append('3º sabor apenas na GG')
            return

        if sabor_1 != '' and sabor_2 != '' and sabor_3 != '':
            if tam == 'Broto':
                self.errors.append('Broto so pode ter 1 sabor')
                return
            if tam == 'M':
                self.errors.append('M so pode ter 2 sabores')
                return
            self.ui.frame_erro.hide()
            text = f'{tam} |  {sabor_1[0:x]} / {sabor_2[0:y]} / {sabor_3[0:z]} | ({borda}) | R$ {self.precifica()}'
            return self.ui.list_view_pizzas.addItem(text)


        if tam not in 'GG' and tam not in 'Broto' and sabor_1 != '' and sabor_2 != '' and sabor_3 != '':
            self.errors.append('3º sabor apenas na GG')
            return

        if sabor_1 == '' and sabor_2 == '' and sabor_3 == '':
            self.errors.append('Selecione pelo menos um sabor')
            return

        if sabor_1 == '' and sabor_3 != '' and sabor_2 != '':
            if tam == 'Broto':
                self.errors.append('O tamanho Broto so pode ter 1 sabor')
                return
            self.errors.append('Selecione o 1º sabor')
            return

        if sabor_1 != '' and sabor_2 != '' and sabor_3 == '':
            if tam == 'Broto':
                self.errors.append('O tamanho Broto so pode ter 1 sabor')
                return
            self.ui.frame_erro.hide()
            text = f'{tam} |  {sabor_1} / {sabor_2}  |({borda}) | R$ {self.precifica()}'
            return self.ui.list_view_pizzas.addItem(text)

        if sabor_1 != '' and sabor_2 == '' and sabor_3 != '':
            if tam == 'Broto':
                self.errors.append('O tamanho Broto so pode ter 1 sabor')
                return
            self.errors.append('Selecione o 2º sabor')
            return

        if sabor_1 == '' and sabor_2 != '' and sabor_3 == '':
            self.errors.append('Selecione o 1º sabor')
            return

        if sabor_1 == '' and sabor_2 == '' and sabor_3 !='':
            self.errors.append('Selecione o 1º e 2º sabor')
            return

        else:
            self.errors.append('Erro')
            return



    #define o preço da entrega
    def delivery_price(self):
        txt = self.ui.comboBox_local_entrega.currentText()
        if txt == 'Buzios':
            self.preco_entrega = 0
            return
        elif txt == 'Pirangi_do_norte':
            self.preco_entrega = 10
            return
        elif txt == 'Pirangi_do_sul':
            self.preco_entrega = 8
            return
        elif txt == 'Tabatinga_01':
            self.preco_entrega = 8
            return
        elif txt == 'Tabatinga_02':
            self.preco_entrega = 10
            return



    def price_desconto(self):
        txt = self.ui.lineEdit_desconto.text()
        if txt == '':
            self.desconto=0
            return
        else:
            txt = txt.split()
            txt = float(txt[1])
            self.desconto = txt



    def precifica(self):
        """
        A função faz a precificação de cada item que passa para a widgetList
        :return: Float --> VALOR DO PEDIDO DA LINHA das ComboBox's
        """
        #TABELA DE PREÇOS
        preco1 = {'Broto':20.00,'M': 35.00, 'G': 40.00,'GG': 46.00}
        preco2 = {'Broto':22.00,'M': 37.00, 'G': 42.00,'GG': 48.00}
        preco3 = {'Broto':20.00,'M': 41.00, 'G': 47.00, 'GG': 53.00}
        doces = {'Broto':20.00,'M': 35.00, 'G': 40.00, 'GG': 46.00}

        tamanho = self.ui.comboBox_tamanho_pizza.currentText()
        sabor1 = 0
        sabor2 = 0
        sabor3 = 0
        preco_final = 0
        preco_borda = 0
        sabores = 0


        for item in catalogo:
            id = item['id']
            if item['sabor'] == self.ui.comboBox_1_sabor.currentText():
                sabores += 1
                if id >= 1 and id <= 11:
                    preco_final += preco1[tamanho]

                elif id >= 12 and id <= 20:
                    preco_final += preco2[tamanho]

                elif id >= 21 and id <= 25:
                    preco_final += preco3[tamanho]

                elif id >= 26 and id <= 30:
                    preco_final += doces[tamanho]

            if item['sabor'] == self.ui.comboBox_2_sabor.currentText():
                sabores += 1
                if id >= 1 and id <= 11:
                    preco_final += preco1[tamanho]

                elif id >= 12 and id <= 20:
                    preco_final += preco2[tamanho]

                elif id >= 21 and id <= 25:
                    preco_final += preco3[tamanho]

                elif id >= 26 and id <= 30:
                    preco_final += doces[tamanho]

            if item['sabor'] == self.ui.comboBox_3_sabor.currentText():
                sabores += 1
                if id >= 1 and id <= 11:
                    preco_final += preco1[tamanho]

                elif id >= 12 and id <= 20:
                    preco_final += preco2[tamanho]

                elif id >= 21 and id <= 25:
                    preco_final += preco3[tamanho]

                elif id >= 26 and id <= 30:
                    preco_final += doces[tamanho]

        if self.ui.comboBox_borda.currentText() == 'Sem_borda':
            preco_borda += 0
        elif self.ui.comboBox_borda.currentText() == 'Catupiry':
            if tamanho == 'M':
                preco_borda += 5
            elif tamanho == 'G':
                preco_borda += 6
            elif tamanho == 'GG':
                preco_borda += 7
        elif self.ui.comboBox_borda.currentText() == 'Cheddar':
            if tamanho == 'M':
                preco_borda += 5
            elif tamanho == 'G':
                preco_borda += 6
            elif tamanho == 'GG':
                preco_borda += 7
        elif self.ui.comboBox_borda.currentText() == 'Chocolate':
            if tamanho == 'M':
                preco_borda += 8
            elif tamanho == 'G':
                preco_borda += 9
            elif tamanho == 'GG':
                preco_borda += 12
        preco_final = f'{(preco_final/sabores)+preco_borda:.2f}'
        return str(preco_final)

    def money_format(self,text):
        text_formated = f'R$ {text:.2f}'
        return text_formated

    def getText(self):
        """
        transformar o texto da textEdit em string
        """
        text = self.ui.textEdit_observacoes.toPlainText()
        txtstring = str(text)
        return txtstring

    def format_text_troco(self):
        #coloca um R$ no texto do troco
        text = self.ui.lineEdit_troco.text()
        if text == '':
            return
        if ',' in text:
            text = text.replace(',','.')
        try:
            text = float(text)
        except:
            if text.isalpha():
                self.errors.append('O troco precisa ser numérico')
                return self.ui.lineEdit_troco.setText('')
        else:
            self.ui.frame_erro.hide()
            return self.ui.lineEdit_troco.setText(f'R$ {text:.2f}')

    def format_text_desconto(self):
        #coloca um R$ no texto do desconto
        text = self.ui.lineEdit_desconto.text()
        if text == '':
            return
        if ',' in text:
            text = text.replace(',','.')
        try:
            text = float(text)
        except:
            if text.isalpha():
                self.errors.append('O desconto precisa ser numérico')
                return self.ui.lineEdit_desconto.setText('')
        else:
            self.ui.frame_erro.hide()
            return self.ui.lineEdit_desconto.setText(f'R$ {text:.2f}')

    def hide_frame_error(self):
        """
        Fecha o frame de erro
        :return:
        """
        self.ui.frame_erro.hide()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Functions()
    janela.show()
    sys.exit(app.exec_())