import dearpygui.dearpygui as dpg
import pandas as pd
import os
import re
from datetime import datetime


#criar pesquisa por nome, verificação em tempo real, e exclusão de venda
#criar historico de adição de vendas
#melhorar o visual

dpg.create_context()

# Constantes para largura e altura da janela
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 880

# Classe para verificar o estado do arquivo .xlsx
class xlsx:
    def xlsx_state(self):
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
                'Placa':[],
                'Observação':[],
                'Categoria':[],
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

    def credit_date_refactor(self):
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

    def end_date_refactor(self):
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

    def plate_refactor(placa):
        plate_input = re.sub(r'[^A-Za-z0-9]', '', placa)

        if len(plate_input) != 7:
            dpg.set_value("input_txtPlate", "A Placa deve conter exatamente 7 caracteres alfanuméricos.")
            return

        try:
            placa_formatada = f"{plate_input[0:3]}{plate_input[3]}{plate_input[4]}{plate_input[5:7]}"
            dpg.set_value("input_txtPlate", placa_formatada.upper())
        except IndexError:
            dpg.set_value("input_txtPlate", "Formato de placa inválido.")


# Classe para obter o caminho do arquivo .xlsx
class XlsxPath(xlsx):
    def get_path(self):
        return xlsx.xlsx_state(self)


# Função para calcular a comissão e atualizar o texto na interface
def calculate_commission(sender, app_data, user_data):
    try:
        InsValue = float(dpg.get_value("input_txtInsValue"))
        commission_pct = float(dpg.get_value("input_txtCommissionPct"))
        cms_value = float((InsValue * commission_pct) / 100)
        dpg.set_value("txtCommissionValue", f"Valor de Comissão ao Corretor: R$ {cms_value:.2f}")
    except ValueError:
        dpg.set_value("txtCommissionValue", "Valor de Comissão ao Corretor: -")


def show_indicator(sender, app_data, user_data):
    indicated = dpg.get_value("input_btnIndicated")

    if indicated:
        dpg.show_item("indicator_inputs")
    else:
        dpg.hide_item("indicator_inputs")


def name_verification():
    xlsx_path = XlsxPath.get_path(self=XlsxPath)
    name_ver = dpg.get_value("input_txtName")
    plate_ver = dpg.get_value("input_txtPlate")

    if os.path.exists(xlsx_path):
        existing_df = pd.read_excel(xlsx_path)
        if any((existing_df['Nome Completo'] == name_ver)):
            dpg.set_value("input_txtName", 'Nome já existente')
#
def plate_verification():
    xlsx_path = XlsxPath.get_path(self=XlsxPath)
    plate_ver = dpg.get_value("input_txtPlate")

    if os.path.exists(xlsx_path):
        existing_df = pd.read_excel(xlsx_path)
        if any((existing_df['Placa'] == plate_ver)):
            dpg.set_value("input_txtPlate", 'Placa já existente')

def combined_callback_plate(sender, app_data):
    plate_input = dpg.get_value("input_txtPlate")
    refactor.plate_refactor(plate_input)
    plate_verification()




# Função para criar as entradas de texto
def text_inputs():
    input_name = dpg.add_text("Nome Completo:")
    input_txtName = dpg.add_input_text(tag="input_txtName", callback=name_verification, width=-1)

    input_product = dpg.add_text("Produto:")
    input_txtProduct = dpg.add_input_text(tag="input_txtProduct", width=-1)

    input_plate = dpg.add_text("Placa:")
    input_txtPlate = dpg.add_input_text(tag="input_txtPlate", width=-1,callback=combined_callback_plate)

    input_obs = dpg.add_text("Observação:")
    input_txtObs = dpg.add_input_text(tag="input_txtObs", width=-1)

    input_category = dpg.add_text("Categoria:")
    input_txtCategory = dpg.add_listbox(
        items=['', 'Carro', 'Moto', 'Caminhão', 'Frota', 'Plano De Saúde', 'Consórcio', 'Celular', 'Embarcação'],
        tag='input_txtCategory', width=-1)

    input_insCompany = dpg.add_text("Seguradora:")
    input_txtInsCompany = dpg.add_listbox(
        items=['', 'Tokio', 'Yelum', 'Bradesco', 'Allianz', 'Azul', 'HDI', 'Mapfre', 'Mitsui', 'Porto Seguro', 'Sompo',
               'Suhai'], tag='input_txtInsCompany', width=-1)

    input_insValue = dpg.add_text("Valor:")
    input_txtInsValue = dpg.add_input_int(tag="input_txtInsValue", callback=calculate_commission, width=-1)

    input_commissionPct = dpg.add_text("(%) Comissão")
    input_txtCommissionPct = dpg.add_input_int(tag="input_txtCommissionPct", callback=calculate_commission, width=-1)

    txtCommissionValue = dpg.add_text("", tag="txtCommissionValue", color=(102, 204, 153))

    input_creditValue = dpg.add_text("Valor do Crédito:")
    input_txtCreditValue = dpg.add_input_int(tag="input_txtCreditValue", width=-1)

    input_creditDate = dpg.add_text("Data do Crédito:")
    input_txtCreditDate = dpg.add_input_text(tag="input_txtCreditDate", callback=refactor.credit_date_refactor, width=-1)

    input_endDate = dpg.add_text("Data de Vigência Final:")
    input_txtEndDate = dpg.add_input_text(tag="input_txtEndDate", callback=refactor.end_date_refactor, width=-1)

    input_btnIndicated = dpg.add_checkbox(label="Indicado?", tag="input_btnIndicated", callback=show_indicator)

    with dpg.group(tag="indicator_inputs", show=False):
        input_indicator = dpg.add_text("Indicador:")
        input_txtIndicator = dpg.add_input_text(tag="input_txtIndicator", width=-1)

        input_indicatorCommissionValue = dpg.add_text("Valor de Comissão ao Indicador:")
        input_txtIndicatorCommissionValue = dpg.add_input_text(tag="input_txtIndicatorCommissionValue", width=-1)

    text_fields = [
        input_name,
        input_product,
        input_plate,
        input_obs,
        input_category,
        input_insCompany,
        input_insValue,
        input_commissionPct,
        txtCommissionValue,
        input_creditValue,
        input_creditDate,
        input_endDate,
        input_indicator,
        input_indicatorCommissionValue
    ]

    return text_fields


def fields_verification(fields):
    fields_names = {
        "Nome Completo": fields[0],
        "Produto": fields[1],
        "Categoria":fields[2],
        "Seguradora": fields[3],
        "Valor": fields[4],
        "(%) Comissão": fields[5],
        "Valor do Crédito": fields[6],
        "Data do Crédito": fields[7],
        "Vigência Final": fields[8]
    }

    empty_fields = [key for key, value in fields_names.items() if value in [None, "", 0]]

    if empty_fields:
        empty_fields_string = ", \n".join(empty_fields)
        with dpg.window(label="Aviso", pos=(100, 100), no_close=False, popup=True, horizontal_scrollbar=True,
                        max_size=[400, 300]):
            dpg.add_text(f"Os seguintes campos estão vazios: \n{empty_fields_string}")
        return False
    return True
# Função de callback do botão salvar
def button_callback():
    name = dpg.get_value("input_txtName")
    product = dpg.get_value("input_txtProduct")
    plate = dpg.get_value("input_txtPlate")
    obs = dpg.get_value("input_txtObs")
    category = dpg.get_value("input_txtCategory")
    InsCompany = dpg.get_value("input_txtInsCompany")
    InsValue = float(dpg.get_value("input_txtInsValue"))
    commission_pct = float(dpg.get_value("input_txtCommissionPct"))
    cms_value = dpg.get_value("txtCommissionValue").split(": ")[-1]
    credit_value = float(dpg.get_value("input_txtCreditValue"))
    credit_date = dpg.get_value("input_txtCreditDate")
    end_date = dpg.get_value("input_txtEndDate")
    indicated = dpg.get_value("input_btnIndicated")
    indicator = dpg.get_value("input_txtIndicator") if indicated else ""
    indicator_commission_value = dpg.get_value("input_txtIndicatorCommissionValue") if indicated else ""

    fields = [name, product, category,InsCompany, InsValue, commission_pct, cms_value, credit_value, credit_date, end_date, indicated, indicator, indicator_commission_value]

    if fields_verification(fields):

        data_dictionary = {
            'Nome Completo': [name],
            'Produto': [product],
            'Placa':[plate],
            'Observação': [obs],
            'Categoria': [category],
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

        chart = pd.DataFrame(data_dictionary)
        xlsx_path = XlsxPath.get_path(self=XlsxPath)

        if os.path.exists(xlsx_path):
            existing_df = pd.read_excel(xlsx_path)

            if any((existing_df['Placa'] == plate) & (existing_df['Produto'] == product)):
                with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True,
                                autosize=True, max_size=[300, 50]):
                    dpg.add_text("Venda já cadastrada")
                return
            else:
                updated_df = pd.concat([existing_df, chart], ignore_index=True)

        else:
            updated_df = chart

        updated_df.to_excel(xlsx_path, index=False)

        with dpg.window(label="Mensagem", pos=(200, 100), no_close=False):
            dpg.add_text(f'Cliente "{name}" cadastrado com sucesso!')
            dpg.add_text(f"Dados salvos com sucesso em: \n{xlsx_path}")


# Configuração da interface
with dpg.window(tag="App", pos=[0, 0], width=WINDOW_WIDTH, height=WINDOW_HEIGHT, no_resize=True, no_collapse=True,
                no_close=True, no_move=True, no_focus_on_appearing=True):

       xlsx.xlsx_state(self=xlsx)
       top_msg = dpg.add_text('Bem-vindo ao Cadastro de Vendas, Corretor.', color=(255, 189, 89))


       text_fields= text_inputs()



       save_button = dpg.add_button(label="Salvar", callback=button_callback)

       baseboard_text = dpg.add_text('Minhas Vendas\nVersão 1.0', pos=[340, 800], color=(255, 189, 89))


with dpg.theme() as theme:
   with dpg.theme_component():
       dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (14, 37, 46))
       dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 228, 188))
       dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
       dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (23, 57, 71))


   with dpg.theme_component(dpg.mvThemeCol_FrameBg):
       dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (241, 236, 202), category=dpg.mvThemeCat_Core)

dpg.bind_theme(theme)

dpg.create_viewport(title='Minhas Vendas', small_icon='icons/icon.ico',width=460, height=WINDOW_HEIGHT, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport(minimized=True)
dpg.set_primary_window("App", True)
dpg.start_dearpygui()
dpg.destroy_context()
