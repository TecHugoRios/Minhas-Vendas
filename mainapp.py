import dearpygui.dearpygui as dpg
import pandas as pd
import os

dpg.create_context()

class xlsx():
    def xlsx_state():
         # Função para verificar se um arquivo .xlsx existe na pasta do arquivo principal
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = "dados.xlsx"
        pasta_arquivo = os.path.join(diretorio_atual, "dados")
        os.makedirs(pasta_arquivo, exist_ok=True)
        path = os.path.join(pasta_arquivo, nome_arquivo)
        exists = os.path.exists(path)

        if not exists:
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

            df = pd.DataFrame(dados)

            try:
                # Cria o arquivo Excel se ele não existir
                df.to_excel(path, sheet_name='dados', index=False)
            except Exception as e:
                print(f"Erro ao criar o arquivo: {e}")

        return path

class XlsxPath(xlsx):
    def get_path(self):
        # Retorna o caminho do arquivo .xlsx usando a função herdada
        return self.xlsx_state()

def text_inputs():

    dpg.add_input_text(label="Nome Completo", tag="input_txtName")
    dpg.add_input_text(label="Produto", tag="input_txtProduct")
    dpg.add_input_text(label="Seguradora", tag="input_txtInsCompany")
    dpg.add_input_text(label="Valor", tag="input_txtInsValue")
    dpg.add_input_text(label="(%) Comissão", tag="input_txtCommissionPct")
    dpg.add_input_text(label="Valor de Comissão", tag="input_txtCommissionValue")
    dpg.add_input_text(label="Valor do Crédito", tag="input_txtCreditValue")
    dpg.add_input_text(label="Data do Crédito", tag="input_txtCreditDate")
    dpg.add_input_text(label="Vigência Final", tag="input_txtEndDate")
    dpg.add_checkbox(label="Indicado?", tag="input_txtIndicated")
    dpg.add_input_text(label="Indicador", tag="input_txtIndicator")
    dpg.add_input_text(label="Valor de Comissão do Indicador", tag="input_txtIndicatorCommissionValue")

def button_callback():
    name = dpg.get_value("input_txtName")
    product = dpg.get_value("input_txtProduct")
    InsCompany = dpg.get_value("input_txtInsCompany")
    InsValue = dpg.get_value("input_txtInsValue")
    commission_pct = dpg.get_value("input_txtCommissionPct")
    commission_value = dpg.get_value("input_txtCommissionValue")
    credit_value = dpg.get_value("input_txtCreditValue")
    credit_date = dpg.get_value("input_txtCreditDate") # mudar para formato data
    end_date = dpg.get_value("input_txtEndDate") # mudar para formato data
    indicated = dpg.get_value("input_txtIndicated") # mudar para radio button 
    indicator = dpg.get_value("input_txtIndicator")
    indicator_commission_value = dpg.get_value("input_txtIndicatorCommissionValue")
    
    fields = {
        "Nome Completo": name,
        "Produto": product,
        "Seguradora": InsCompany,
        "Valor": InsValue,
        "(%) Comissão": commission_pct,
        "Valor de Comissão": commission_value,
        "Valor do Crédito": credit_value,
        "Data do Crédito": credit_date,
        "Vigência Final": end_date
    }

    empty_fields = [fields for fields, value in fields.items() if not value or value.strip() == ""]

    if empty_fields:
        empty_fields_str = ", \n".join(empty_fields)
        with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True,max_size=[300,200]):
            dpg.add_text(f"Os seguintes campos estão vazios: \n{empty_fields_str}")
        return
    if indicated ==  False:
        pass

    data_dictionary = {  'Nome Completo': [name],
                        'Produto': [product],
                        'Seguradora': [InsCompany],
                        'Valor': [InsValue],
                        '(%) Comissão': [commission_pct],
                        'Valor de Comissão': [commission_value],
                        'Valor do Crédito': [credit_value],
                        'Data do Crédito': [credit_date],
                        'Vigência Final': [end_date],
                        'Indicado': [indicated],
                        'Indicador': [indicator],
                        'Valor de Comissão do Indicador': [indicator_commission_value]
                    }
    
    tabel = pd.DataFrame.from_dict(data_dictionary)
    if os.path.exists('dados/dados.xlsx'):
        existing_df = pd.read_excel('dados/dados.xlsx')

        if any(existing_df['Nome Completo'] == name):
            with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True,autosize=True, max_size=[300,50]):
                dpg.add_text("Venda já cadastrada")
            return  
        else:
            updated_df = pd.concat([existing_df, tabel], ignore_index=True)
    else:
        # Se o arquivo não existir, cria um novo DataFrame
        updated_df = tabel
    
    # Salva o DataFrame atualizado no arquivo Excel
    updated_df.to_excel('dados/dados.xlsx', index=False)

    xlsx_path = XlsxPath.get_path(self=XlsxPath)

    with dpg.window(label="Mensagem", pos=(50, 200), no_close=False):
        dpg.add_text(f'Cliente "{name}" cadastrado com sucesso!')
        dpg.add_text(f"Dados salvos com sucesso em {xlsx_path}")

with dpg.window(tag="App"):
    xlsx.xlsx_state()
    top_msg = dpg.add_text('Bem vindo ao cadastro de clientes',)
    text_inputs()



    btn = dpg.add_button(label="Salvar", callback=button_callback)
    
    #dpg.add_file_dialog(directory_selector=True, show=False, tag="file_dialog_id",width=700 ,height=400)
    #dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))

    dpg.add_button(label="Button 2")

    #tabela para informar usuarios cadastrados
    with dpg.table(header_row=False, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True):

       
        dpg.add_table_column()

        for i in range(0, 4):
            with dpg.table_row():
                for j in range(0, 3):
                    dpg.add_text(f"Row{i} Column{j}")


dpg.create_viewport(title='Minhas Vendas',small_icon='icons/icon.ico', width=800, height=600, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
#dpg.show_style_editor()
#dpg.show_font_manager()
dpg.set_primary_window("App", True)
dpg.start_dearpygui()
dpg.destroy_context()
