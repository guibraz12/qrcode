from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import filedialog as fd 
import qrcode
import cv2


def fechar_janela():
    if askyesno(title='Fechar Aplicativo de Leitor e Gerador de QR Code', message='Tem certeza de que deseja fechar o aplicativo?'):
        raiz.destroy()
        

def gerar_qrcode():
    dados_qrcode = str(entrada_dados.get())
    nome_qrcode = str(entrada_nome_arquivo.get())
    if nome_qrcode == '':
        showerror(title='Erro', message='Ocorreu um erro.' \
                   '\nA causa:' \
                    '\n-> Campo de nome do arquivo vazio\n' \
                    'Certifique-se de preencher o campo de nome ao gerar o QR Code')
    else:
        if askyesno(title='Confirmação', message=f'Deseja criar um QR Code com as informações fornecidas?'):
            try:
                qr = qrcode.QRCode(version=1, box_size=6, border=4)
                qr.add_data(dados_qrcode)
                qr.make(fit=True)
                nome = nome_qrcode + '.png'
                imagem_qrcode = qr.make_image(fill_color='black', back_color='white')
                imagem_qrcode.save(nome)
                global Imagem
                Imagem = PhotoImage(file=f'{nome}')
                rotulo_imagem1.config(image=Imagem)
                botao_resetar.config(state=NORMAL, command=resetar)
            except:
                showerror(title='Erro', message='Por favor, forneça um nome de arquivo válido')
        
def resetar():
    if askyesno(title='Redefinir', message='Tem certeza de que deseja redefinir?'):
        rotulo_imagem1.config(image='')
        botao_resetar.config(state=DISABLED)
        
def abrir_dialogo():
    nome_arquivo = fd.askopenfilename()
    entrada_arquivo.delete(0, END)
    entrada_arquivo.insert(0, nome_arquivo)

def detectar_qrcode():
    arquivo_imagem = entrada_arquivo.get()
    if arquivo_imagem == '':
        showerror(title='Erro', message='Por favor, forneça um arquivo de imagem de QR Code para detectar')
    else:
        try:
            qr_img = cv2.imread(f'{arquivo_imagem}')    
            qr_detector = cv2.QRCodeDetector()  
            global imagem_qrcode
            imagem_qrcode = PhotoImage(file=f'{arquivo_imagem}')
            rotulo_imagem2.config(image=imagem_qrcode)
            dados, pts, st_code = qr_detector.detectAndDecode(qr_img)  
            rotulo_dados.config(text=dados)
        except:
            showerror(title='Erro', message='Ocorreu um erro ao detectar os dados do arquivo fornecido' \
                   '\nAs possíveis causas são:' \
                    '\n-> Arquivo de imagem incorreto\n' \
                    'Certifique-se de que o arquivo de imagem é um QR Code válido')


raiz = Tk()
raiz.title('Aplicativo de Leitor e Gerador de QR Code')
raiz.geometry('500x480+440+180')
raiz.resizable(height=FALSE, width=FALSE)
raiz.protocol('WM_DELETE_WINDOW', fechar_janela)

estilo_rotulo = ttk.Style()
estilo_rotulo.configure('TLabel', foreground='#000000', font=('OCR A Extended', 11))

estilo_entrada = ttk.Style()
estilo_entrada.configure('TEntry', font=('arial', 15))

estilo_botao = ttk.Style()
estilo_botao.configure('TButton', foreground='#000000', font=('arial', 10))

abas_controle = ttk.Notebook(raiz)

aba_gerador = ttk.Frame(abas_controle)
aba_detector = ttk.Frame(abas_controle)

abas_controle.add(aba_gerador, text='Gerador de QR Code')
abas_controle.add(aba_detector, text='Detector de QR Code')
abas_controle.pack(expand=1, fill="both")

canvas_gerador = Canvas(aba_gerador, width=500, height=480)
canvas_gerador.pack()

canvas_detector = Canvas(aba_detector, width=500, height=480)
canvas_detector.pack()

rotulo_imagem1 = Label(raiz)
canvas_gerador.create_window(250, 150, window=rotulo_imagem1)

rotulo_dados_qrcode = ttk.Label(raiz, text='Dados do QR Code', style='TLabel')
entrada_dados = ttk.Entry(raiz, width=55, style='TEntry')

canvas_gerador.create_window(70, 330, window=rotulo_dados_qrcode)
canvas_gerador.create_window(300, 330, window=entrada_dados)

rotulo_nome_arquivo = ttk.Label(raiz, text='Nome do Arquivo', style='TLabel')
entrada_nome_arquivo = ttk.Entry(width=55, style='TEntry')

canvas_gerador.create_window(84, 360, window=rotulo_nome_arquivo)
canvas_gerador.create_window(300, 360, window=entrada_nome_arquivo)

botao_resetar = ttk.Button(raiz, text='Redefinir', style='TButton', state=DISABLED)
botao_gerar = ttk.Button(raiz, text='Gerar QR Code', style='TButton', command=gerar_qrcode)

canvas_gerador.create_window(300, 390, window=botao_resetar)
canvas_gerador.create_window(410, 390, window=botao_gerar)

rotulo_imagem2 = Label(raiz)
rotulo_dados = ttk.Label(raiz)

canvas_detector.create_window(250, 150, window=rotulo_imagem2)
canvas_detector.create_window(250, 300, window=rotulo_dados)

entrada_arquivo = ttk.Entry(raiz, width=60, style='TEntry')
botao_procurar = ttk.Button(raiz, text='Procurar', style='TButton', command=abrir_dialogo)

canvas_detector.create_window(200, 350, window=entrada_arquivo)
canvas_detector.create_window(430, 350, window=botao_procurar)

botao_detectar = ttk.Button(raiz, text='Detectar QR Code', style='TButton', command=detectar_qrcode)
canvas_detector.create_window(65, 385, window=botao_detectar)

raiz.mainloop()
