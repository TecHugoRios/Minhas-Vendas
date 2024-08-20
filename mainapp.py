import dearpygui.dearpygui as dpg
import pandas as pd
import os
from datetime import datetime

#criar drop list de seguradoras
#melhorar o visual
#adicionar verificação de data
#criar pesquisa por nome e exclusão de venda

dpg.create_context()

# Classe para verificar o estado do arquivo .xlsx
class xlsx:
    def xlsx_state():
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
                df.to_excel(path, sheet_name='dados', index=False)
            except Exception as e:
                print(f"Erro ao criar o arquivo: {e}")

        return path

class refactor:
    def date_validation(date):
        try:
            datetime.strptime(date, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def credit_date_refactor():
        date_text_credit = dpg.get_value("input_txtCreditDate")
        if len(date_text_credit) < 10 and len(date_text_credit) > 4:
            day_credit = date_text_credit[:2]
            month_credit = date_text_credit[2:4]
            year_credit = date_text_credit[4:]
            credit_date = (f'{day_credit}/{month_credit}/{year_credit}')
            validate = refactor.date_validation(credit_date)

            if validate: 
              dpg.set_value("input_txtCreditDate", f'{credit_date}')   
            else:
              dpg.set_value("input_txtCreditDate", "Insira DD/MM/AAAA")
                

    def end_date_refactor():
        date_text_end = dpg.get_value("input_txtEndDate")
        if len(date_text_end) < 10 and len(date_text_end) > 4:
            day_end = date_text_end[:2]
            month_end = date_text_end[2:4]
            year_end = date_text_end[4:]
            end_date = (f'{day_end}/{month_end}/{year_end}')

            dpg.set_value("input_txtEndDate", f'{end_date}')
            validate = refactor.date_validation(end_date)

            if validate: 
                dpg.set_value("input_txtEndDate", f'{end_date}')  
            else:
               dpg.set_value("input_txtEndDate", "Insira DD/MM/AAAA")
                
# Classe para obter o caminho do arquivo .xlsx
class XlsxPath(xlsx):
    def get_path():
        return xlsx.xlsx_state()

# Função para calcular a comissão e atualizar o texto na interface
def calculate_commission(sender, app_data, user_data):
    try:
        InsValue = float(dpg.get_value("input_txtInsValue"))
        commission_pct = float(dpg.get_value("input_txtCommissionPct"))
        cms_value = (InsValue * commission_pct) / 100
        dpg.set_value("txtCommissionValue", f"Valor de Comissão ao Corretor: {cms_value:.2f}")
    except ValueError:
        dpg.set_value("txtCommissionValue", "Valor de Comissão ao Corretor: -")

def show_indicator(sender, app_data, user_data):
    indicated = dpg.get_value("input_btnIndicated")
    
    if indicated:
        dpg.show_item("indicator_inputs")
    else:
        dpg.hide_item("indicator_inputs")

# Função para criar as entradas de texto
def text_inputs():
    dpg.add_input_text(label="Nome Completo", tag="input_txtName")
    dpg.add_input_text(label="Produto", tag="input_txtProduct")
    dpg.add_input_text(label="Seguradora", tag="input_txtInsCompany")

    dpg.add_input_text(label="Valor", tag="input_txtInsValue", callback=calculate_commission)
    dpg.add_input_text(label="(%) Comissão", tag="input_txtCommissionPct", callback=calculate_commission)

    dpg.add_text("", tag="txtCommissionValue", color=(102, 204, 153))
    dpg.add_input_text(label="Valor do Crédito", tag="input_txtCreditValue")

    dpg.add_input_text(label="Data do Crédito", tag="input_txtCreditDate", callback=refactor.credit_date_refactor)
    dpg.add_input_text(label="Data de Vigência Final", tag="input_txtEndDate", callback=refactor.end_date_refactor)

    dpg.add_checkbox(label="Indicado?", tag="input_btnIndicated", callback=show_indicator)
    
    with dpg.group(tag="indicator_inputs", show=False):
        dpg.add_input_text(label="Indicador", tag="input_txtIndicator")
        dpg.add_input_text(label="Valor de Comissão ao Indicador", tag="input_txtIndicatorCommissionValue")

# Função de callback do botão salvar
def button_callback():
    name = dpg.get_value("input_txtName")
    product = dpg.get_value("input_txtProduct")
    InsCompany = dpg.get_value("input_txtInsCompany")
    InsValue = dpg.get_value("input_txtInsValue")
    commission_pct = dpg.get_value("input_txtCommissionPct")
    cms_value = dpg.get_value("txtCommissionValue").split(": ")[-1]
    credit_value = dpg.get_value("input_txtCreditValue")
    credit_date = dpg.get_value("input_txtCreditDate")
    end_date = dpg.get_value("input_txtEndDate")

    indicated = dpg.get_value("input_btnIndicated")
    indicator = dpg.get_value("input_txtIndicator") if indicated else ""
    indicator_commission_value = dpg.get_value("input_txtIndicatorCommissionValue") if indicated else ""
    
    fields = {
        "Nome Completo": name,
        "Produto": product,
        "Seguradora": InsCompany,
        "Valor": InsValue,
        "(%) Comissão": commission_pct,
        "Valor do Crédito": credit_value,
        "Data do Crédito": credit_date,
        "Vigência Final": end_date,
    }

    empty_fields = [key for key, value in fields.items() if not value]

    if empty_fields:
        empty_fields_str = ", \n".join(empty_fields)
        with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True, max_size=[400,300]):
            dpg.add_text(f"Os seguintes campos estão vazios: \n{empty_fields_str}")
        return

    data_dictionary = {  
        'Nome Completo': [name],
        'Produto': [product],
        'Seguradora': [InsCompany],
        'Valor': [InsValue],
        '(%) Comissão': [commission_pct],
        'Valor de Comissão': [cms_value],
        'Valor do Crédito': [credit_value],
        'Data do Crédito': [credit_date],
        'Vigência Final': [end_date],
        'Indicado': [indicated],
        'Indicador': [indicator],
        'Valor de Comissão do Indicador': [indicator_commission_value]
    }
    
    tabel = pd.DataFrame.from_dict(data_dictionary)
    xlsx_path = XlsxPath.get_path()

    if os.path.exists(xlsx_path):
        existing_df = pd.read_excel(xlsx_path)
        if any(existing_df['Nome Completo'] == name):
            with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True, autosize=True, max_size=[300,50]):
                dpg.add_text("Venda já cadastrada")
            return  
        else:
            updated_df = pd.concat([existing_df, tabel], ignore_index=True)
    else:
        updated_df = tabel
    
    updated_df.to_excel(xlsx_path, index=False)

    with dpg.window(label="Mensagem", pos=(50, 200), no_close=False):
        dpg.add_text(f'Cliente "{name}" cadastrado com sucesso!')
        dpg.add_text(f"Dados salvos com sucesso em {xlsx_path}")

# Configuração da interface
with dpg.window(tag="App"):
    xlsx.xlsx_state()
    dpg.add_text('Bem-vindo ao Cadastro de Vendas, Corretor.')
    text_inputs()
    dpg.add_button(label="Salvar", callback=button_callback)


with dpg.theme() as theme:
    with dpg.theme_component():
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (1, 4, 18), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 247, 217), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9)

    with dpg.theme_component(dpg.mvThemeCol_FrameBg):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (241, 236, 202), category=dpg.mvThemeCat_Core)

dpg.bind_theme(theme)

dpg.create_viewport(title='Minhas Vendas', small_icon='icons/icon.ico', width=500, height=600, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("App", True)
dpg.show_style_editor()
dpg.start_dearpygui()
dpg.destroy_context()
