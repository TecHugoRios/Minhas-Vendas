from tkinter import *
import tkinter as tk
import pandas as pd

menu_principal = tk.Tk()
menu_principal.title("Minhas Vendas")
menu_principal['bg'] = "#f0f8ff"  # Mudança de cor de fundo
menu_principal.iconbitmap("imgs/icon.ico")

# Dimensões da janela
largura = 1200
altura = 800

# Resolução do sistema
largura_screen = menu_principal.winfo_screenwidth()
altura_screen = menu_principal.winfo_screenheight()

# Posição da janela
posx = largura_screen / 2 - largura / 2
posy = altura_screen / 2 - altura / 2

menu_principal.resizable(0, 0)  # Não permitir redimensionamento

# GUI
frame = Frame(menu_principal, padx=20, pady=20, bg="#e0f7fa")  # Fundo diferente para o frame
frame.grid(column=0, row=0, padx=20, pady=20, sticky="nsew")

# Configurar redimensionamento das colunas e linhas
menu_principal.grid_rowconfigure(0, weight=1)
menu_principal.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

Label(frame, text="Bem-vindo, cadastre sua venda:", font="Poppins 15 bold", bg="#e0f7fa").grid(column=0, row=0,
                                                                                               columnspan=2,
                                                                                               pady=10)
# Estilo dos Labels

label_nome = Label(frame, text="Nome Completo:", bg="#e0f7fa", font="Poppins 10 bold")
label_nome.grid(column=0, row=1, sticky=E, padx=5, pady=5)

label_produto = Label(frame, text="Produto:", bg="#e0f7fa", font="Poppins 10 bold")
label_produto.grid(column=0, row=2, sticky=E, padx=5, pady=5)

label_seguradora = Label(frame, text="Seguradora:", bg="#e0f7fa", font="Poppins 10 bold")
label_seguradora.grid(column=0, row=3, sticky=E, padx=5, pady=5)

label_valor = Label(frame, text="Valor:", bg="#e0f7fa", font="Poppins 10 bold")
label_valor.grid(column=0, row=4, sticky=E, padx=5, pady=5)

label_comissao = Label(frame, text="Comissão (%):", bg="#e0f7fa", font="Poppins 10 bold")
label_comissao.grid(column=0, row=5, sticky=E, padx=5, pady=5)

label_valorComissao = Label(frame, text="Valor da Comissão:", bg="#e0f7fa", font="Poppins 10 bold")
label_valorComissao.grid(column=0, row=6, sticky=E, padx=5, pady=5)

label_valorCredito = Label(frame, text="Valor de Crédito:", bg="#e0f7fa", font="Poppins 10 bold")
label_valorCredito.grid(column=0, row=7, sticky=E, padx=5, pady=5)

label_dataCredito = Label(frame, text="Data de Crédito:", bg="#e0f7fa", font="Poppins 10 bold")
label_dataCredito.grid(column=0, row=8, sticky=E, padx=5, pady=5)

label_VigenciaFinal = Label(frame, text="Vigência Final:", bg="#e0f7fa", font="Poppins 10 bold")
label_VigenciaFinal.grid(column=0, row=9, sticky=E, padx=5, pady=5)

label_Indicador = Label(frame, text="Indicador:", bg="#e0f7fa", font="Poppins 10 bold")
label_Indicador.grid(column=0, row=10, sticky=E, padx=5, pady=5)

label_valorComissaoIndicador = Label(frame, text="Valor da Comissão para o indicador:", bg="#e0f7fa",
                                     font="Poppins 10 bold")
label_valorComissaoIndicador.grid(column=0, row=11, sticky=E, padx=5, pady=5)

# Mensagem de rodapé
Label(frame, text="Desenvolvido por [Hugo Rios]", bg="#e0f7fa", font="Poppins 8 italic").grid(column=0, row=13,
                                                                                              columnspan=2,
                                                                                              pady=10)

# Estilo da Entry
NomeCompleto = Entry(frame, width=30, font="Poppins 10")
NomeCompleto.grid(column=1, row=1, pady=5, sticky="ew", padx=5)

Produto = Entry(frame, width=30, font="Poppins 10")
Produto.grid(column=1, row=2, pady=5, sticky="ew", padx=5)

Seguradora = Entry(frame, width=30, font="Poppins 10")
Seguradora.grid(column=1, row=3, pady=5, sticky="ew", padx=5)

Valor = Entry(frame, width=30, font="Poppins 10")
Valor.grid(column=1, row=4, pady=5, sticky="ew", padx=5)

Comissao = Entry(frame, width=30, font="Poppins 10")
Comissao.grid(column=1, row=5, pady=5, sticky="ew", padx=5)

ValorComissao = Entry(frame, width=30, font="Poppins 10")
ValorComissao.grid(column=1, row=6, pady=5, sticky="ew", padx=5)

ValorCredito = Entry(frame, width=30, font="Poppins 10")
ValorCredito.grid(column=1, row=7, pady=5, sticky="ew", padx=5)

DataCredito = Entry(frame, width=30, font="Poppins 10")
DataCredito.grid(column=1, row=8, pady=5, sticky="ew", padx=5)

VigenciaFinal = Entry(frame, width=30, font="Poppins 10")
VigenciaFinal.grid(column=1, row=9, pady=5, sticky="ew", padx=5)

botaocheck = Checkbutton(frame, text="Indicado?")
botaocheck.grid(column=2, row=10, pady=5, sticky="ew", padx=5)

Indicador = Entry(frame, width=30, font="Poppins 10")
Indicador.grid(column=1, row=10, pady=5, sticky="ew", padx=5)

# Botão para adicionar vendas
botao_cadastrar = Button(frame, text="Cadastrar Venda", font="Poppins 10 bold", bg="#00796b", fg="white",
                         relief="solid")
botao_cadastrar.grid(column=0, row=12, columnspan=2, pady=20)




