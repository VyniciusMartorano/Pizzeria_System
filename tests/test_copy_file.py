from distutils.file_util import copy_file
import unittest
import sistema.base_de_dados.copy_file


class TestCopyFile(unittest.TestCase):
    def test_copia_arquivo_da_area_de_trabalho_para_a_pasta_dowloads_e_nao_retorna_nada(self):
        caminho_do_arquivo_a_ser_copiado = "C:/Users/vynic/Desktop/table.db"
        caminho_onde_o_arquivo_deve_chegar = "C:/Users/vynic/Downloads/"
        novo_nome_do_arquivo = 'table01'
        copy_file.copy_file_to_new_path(
            file_to_copy_path=caminho_do_arquivo_a_ser_copiado,
            path_target=caminho_onde_o_arquivo_deve_chegar,
            new_name_file=novo_nome_do_arquivo
            )


if __name__ == '__main__':
    unittest.main(verbosity=2)