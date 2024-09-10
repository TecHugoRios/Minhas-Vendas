import dearpygui.dearpygui as dpg
import pandas as pd
import os
from datetime import datetime


#criar pesquisa por nome, verificação em tempo real, e exclusão de venda
#criar historico de adição de vendas
#melhorar o visual

dpg.create_context()

# Constantes para largura e altura da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 550

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
        dpg.set_value("txtCommissionValue", f"Valor de Comissão ao Corretor: {cms_value:.2f}")
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

    if os.path.exists(xlsx_path):
        existing_df = pd.read_excel(xlsx_path)
        if any(existing_df['Nome Completo'] == name_ver):
            dpg.set_value("input_txtName", 'Nome já existente')


# Função para criar as entradas de texto
def text_inputs():
    dpg.add_text("Nome Completo:")
    dpg.add_input_text(tag="input_txtName", callback=name_verification)
    dpg.add_text("Produto:")
    dpg.add_input_text(tag="input_txtProduct")
    dpg.add_text("Seguradora:")
    dpg.add_listbox(items=['','Tokio', 'Yelum', 'Bradesco','Allianz', 'Azul', 'HDI', 'Mapfre', 'Mitsui', 'Porto Seguro', 'Sompo', 'Suhai'],tag='input_txtInsCompany')

    dpg.add_text("Valor:")
    dpg.add_input_int(label="Valor", tag="input_txtInsValue", callback=calculate_commission)
    dpg.add_input_int(label="(%) Comissão", tag="input_txtCommissionPct", callback=calculate_commission)

    dpg.add_text("", tag="txtCommissionValue", color=(102, 204, 153))
    dpg.add_input_int(label="Valor do Crédito", tag="input_txtCreditValue")

    dpg.add_input_text(label="Data do Crédito", tag="input_txtCreditDate", callback=refactor.credit_date_refactor)
    dpg.add_input_text(label="Data de Vigência Final", tag="input_txtEndDate", callback=refactor.end_date_refactor)

    dpg.add_checkbox(label="Indicado?", tag="input_btnIndicated", callback=show_indicator)

    with dpg.group(tag="indicator_inputs", show=False):
        dpg.add_input_text(label="Indicador", tag="input_txtIndicator")
        dpg.add_input_text(label="Valor de Comissão ao Indicador", tag="input_txtIndicatorCommissionValue")


def fiels_verification(fields):
    fields_names = {
        "Nome Completo": fields[0],
        "Produto": fields[1],
        "Seguradora": fields[2],
        "Valor": fields[3],
        "(%) Comissão": fields[4],
        "Valor do Crédito": fields[5],
        "Data do Crédito": fields[6],
        "Vigência Final": fields[7]
    }

    empty_fields = [key for key, value in fields_names.items() if not value]

    if empty_fields:
        empty_fields_string = ", \n".join(empty_fields)
        with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True,
                        max_size=[400, 300]):
            dpg.add_text(f"Os seguintes campos estão vazios: \n{empty_fields_string}")
        return

# Função de callback do botão salvar
def button_callback():
    name = dpg.get_value("input_txtName")
    product = dpg.get_value("input_txtProduct")
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

    fields = [name, product, InsCompany, InsValue, commission_pct, cms_value, credit_value, credit_date, end_date, indicated, indicator, indicator_commission_value]

    fiels_verification(fields)

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

    chart = pd.DataFrame(data_dictionary)
    xlsx_path = XlsxPath.get_path(self=XlsxPath)

    if os.path.exists(xlsx_path):
        existing_df = pd.read_excel(xlsx_path)

        if any((existing_df['Nome Completo'] == name) & (existing_df['Produto'] == product) & (existing_df['Data do Crédito'] == credit_date) & (existing_df['Vigência Final'] == end_date)):
            with dpg.window(label="Aviso", pos=(200, 100), no_close=False, popup=True, horizontal_scrollbar=True,
                            autosize=True, max_size=[300, 50]):
                dpg.add_text("Venda já cadastrada")
            return
        else:
            updated_df = pd.concat([existing_df, chart], ignore_index=True)

    else:
        updated_df = chart

    updated_df.to_excel(xlsx_path, index=False)

    with dpg.window(label="Mensagem", pos=(50, 200), no_close=False):
        dpg.add_text(f'Cliente "{name}" cadastrado com sucesso!')
        dpg.add_text(f"Dados salvos com sucesso em {xlsx_path}")


# Configuração da interface
with dpg.window(tag="App", pos=[0, 0], width=WINDOW_WIDTH, height=WINDOW_HEIGHT, no_resize=True, no_background=True, no_collapse=True,
                no_close=True, no_move=True, no_focus_on_appearing=True):
    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save")
            dpg.add_menu_item(label="Save As")

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", check=True)
                dpg.add_menu_item(label="Setting 2")

    xlsx.xlsx_state(self=xlsx)
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

dpg.create_viewport(title='Minhas Vendas', small_icon='icons/icon.ico',width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
dpg.setup_dearpygui()
dpg.show_viewport(minimized=True)
dpg.set_primary_window("App", False)
#dpg.show_style_editor()
dpg.start_dearpygui()
dpg.destroy_context()
