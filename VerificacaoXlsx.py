import os
import pandas as pd

import GUI

def XlsxExiste():
    #função para verificar e se um arquivo .xlsx existe na pasta do arquivo main
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    nome_arquivo = "dados.xlsx"
    pasta_arquivo = os.path.join(diretorio_atual, "dados")
    os.makedirs(pasta_arquivo, exist_ok=True)
    caminho = os.path.join(pasta_arquivo, nome_arquivo)
    existe = os.path.exists(caminho)

    if not existe:
        dados = {
            'Nome Completo': [],
            'Produto': [],
            'Seguradora': [],
            'Valor': [],
            '(%) Comissão': [],
            'Valor de Comissão': [],
            'Valor do Crédito': [],
            'Data do Crédito': [],
            'Vigência Final': [],
            'Indicado': [],
            'Indicador': [],
            'Valor de Comissão do Indicador': []
        }

        # Criar um DataFrame vazio
        df = pd.DataFrame(dados)

        try:
            # Criar um arquivo .xlsx
            df.to_excel(caminho, sheet_name='dados', index=True)
            GUI.label_Aviso = GUI.Label(GUI.frame,
                                text=f"Arquivo 'dados.xlsx' inexistente, \n o arquivo foi criado automaticamente em: {caminho}",
                                bg="red", font="Poppins 8 bold")
            GUI.label_Aviso.grid(column=1, row=15, padx=2, pady=2)
        except Exception as e:
            print(f"Erro ao criar o arquivo: {e}")

    return existe, caminho
