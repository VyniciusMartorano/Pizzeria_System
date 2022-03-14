import unittest
from sistema.base_de_dados.write_in_table import write_in_table


class TestWriteInTable(unittest.TestCase):
    def test_escrever_na_tabela_e_deve_passar(self):
        name_table = 'clientes'
        caminho = "C:/Users/vynic/Desktop/table.db"
        dicionario_dados = {
            'id': 1,
            'nome': 'Vynicius Martorano',
            'telefone': 994041304,
            'hora': '18:30',
            'entrega': 'BUZIUS',
            'forma_pagamento': 'DINHEIRO',
            'valor_total': 155.00
        }
        write_in_table(table_name=name_table,caminho=caminho,dados=dicionario_dados)

    def test_deve_verificar_os_tipos_dos_dados_do_dicionario_e_todos_os_testes_que_derem_errado_retornam_suas_respectivas_mensagens_de_erro(self):
        dados = {
            'id': '1',
            'nome': 'Vynicius Martorano',
            'telefone': '994041304',
            'hora': '18:30',
            'entrega': 'BUZIUS',
            'forma_pagamento': 'DINHEIRO',
            'valor_total': '155.00'
        }
        lista_erros = []

        if not isinstance(dados['id'], int):
            lista_erros.append('\n\033[1;31mA entrada de dados de "id" não está correta\033[m')

        if not isinstance(dados['nome'], str):
            lista_erros.append('\n\033[1;31mA entrada de dados de "nome" não está correta\033[m')

        if not isinstance(dados['telefone'], int):
            lista_erros.append('\n\033[1;31mA entrada de dados de "telefone" não está correta\033[m')

        if not isinstance(dados['hora'], str):
            lista_erros.append('\n\033[1;31mA entrada de dados de "hora" não está correta\033[m')

        if not isinstance(dados['entrega'], str):
            lista_erros.append('\n\033[1;31mA entrada de dados de "entrega" não está correta\033[m')

        if not isinstance(dados['forma_pagamento'], str):
            lista_erros.append('\n\033[1;31mA entrada de dados de "forma_pagamento" não está correta\033[m')

        if not isinstance(dados['valor_total'], float):
            lista_erros.append('\n\033[1;31mA entrada de dados do "valor_total" não está correta\033[m\n')

        if lista_erros:
            for erro in lista_erros:
                with self.subTest(msg=erro):
                    print(erro)
            raise 'Erros exibidos acima'
            


if __name__ == '__main__':
    unittest.main(verbosity=2)
