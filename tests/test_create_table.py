from sistema.create_table import create_table
import unittest


class TestCriaTabela(unittest.TestCase):
    def test_deve_criar_tabela_na_area_de_trabalho_e_passar(self):
        caminho = 'C:/Users/vynic/Desktop'
        name_table = 'clientes'
        name_file = 'table'
        create_table(caminho=caminho,name_table=name_table,name_file=name_file)
            

if __name__ == '__main__':
    unittest.main(verbosity=2)