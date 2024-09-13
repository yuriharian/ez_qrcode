import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
from io import BytesIO
from pyzbar.pyzbar import decode
import pyperclip

# Função para gerar o QR Code
def gerar_qr_code():
    link = entrada.get()

    if not link:
        messagebox.showwarning("Aviso", "Por favor, insira um link!")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.thumbnail((320, 320))
    exibir_qr_code(img)

    # Mostrar o frame do QR Code e botões de salvar e copiar
    frame_qr_code.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    salvar_btn.grid(row=3, column=0, pady=5, sticky="ew")
    copiar_img_btn.grid(row=4, column=0, pady=5, sticky="ew")

# Função para exibir o QR Code gerado na interface
def exibir_qr_code(img):
    img_tk = ImageTk.PhotoImage(img)
    qr_code_label.config(image=img_tk)
    qr_code_label.image = img_tk
    qr_code_label.qr_image = img

# Função para salvar o QR Code como imagem
def salvar_como():
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png")])
    if caminho_arquivo:
        qr_code_label.qr_image.save(caminho_arquivo)
        messagebox.showinfo("Sucesso", f"QR Code salvo como {caminho_arquivo}")

# Função para copiar o QR Code para a área de transferência
def copiar_imagem():
    output = BytesIO()
    qr_code_label.qr_image.save(output, format="PNG")
    data = output.getvalue()
    output.close()

    root.clipboard_clear()
    root.clipboard_append(data)
    messagebox.showinfo("Sucesso", "QR Code copiado para a área de transferência.")

# Função para ler QR Code de uma imagem
def ler_qr_code():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if not caminho_imagem:
        return

    img = Image.open(caminho_imagem)
    resultado = decode(img)

    if resultado:
        qr_data = resultado[0].data.decode("utf-8")
        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, qr_data)
        copiar_btn.grid(row=3, column=0, pady=5, sticky="ew")
    else:
        messagebox.showerror("Erro", "Nenhum QR Code encontrado na imagem.")

# Função para copiar o conteúdo do campo de texto
def copiar_para_clipboard():
    texto = resultado_texto.get(1.0, tk.END).strip()
    if texto:
        pyperclip.copy(texto)
        messagebox.showinfo("Copiado", "O conteúdo foi copiado para a área de transferência.")

# Função para abrir a tela de geração de QR Code
def abrir_tela_gerar():
    tela_inicial.pack_forget()
    tela_gerar.pack(fill="both", expand=True)

# Função para abrir a tela de leitura de QR Code
def abrir_tela_ler():
    tela_inicial.pack_forget()
    tela_ler.pack(fill="both", expand=True)

# Função para voltar à tela inicial
def voltar_tela_inicial():
    tela_gerar.pack_forget()
    tela_ler.pack_forget()
    tela_inicial.pack(fill="both", expand=True)

# Configuração da interface gráfica
root = tk.Tk()
root.title("EZ QR Code")
root.geometry("800x400")
root.resizable(False, False)

# Definindo cores e fontes
fundo = "#282c34"
cor_texto = "#61dafb"
fonte_padrao = ("Helvetica", 12)

# Função para validar a entrada
def validar_entrada(char, text):
    if len(text) > 150:
        messagebox.showwarning("Aviso", "O link não pode ter mais de 150 caracteres!")
        return False
    return True

# Configuração do método de validação
validate_command = root.register(validar_entrada)

# Tela Inicial
tela_inicial = tk.Frame(root, bg=fundo)
tela_inicial.pack(fill="both", expand=True)

label_bem_vindo = tk.Label(tela_inicial, text="Escolha uma opção", bg=fundo, fg=cor_texto, font=("Helvetica", 16))
label_bem_vindo.pack(pady=20)

btn_gerar_qr = tk.Button(tela_inicial, text="Gerar QR Code", command=abrir_tela_gerar, bg="#4CAF50", fg="white", font=fonte_padrao)
btn_gerar_qr.pack(pady=10)

btn_ler_qr = tk.Button(tela_inicial, text="Ler QR Code", command=abrir_tela_ler, bg="#2196F3", fg="white", font=fonte_padrao)
btn_ler_qr.pack(pady=10)

# Tela de Geração de QR Code
tela_gerar = tk.Frame(root, bg=fundo)
tela_gerar.grid_columnconfigure(0, weight=6)
tela_gerar.grid_columnconfigure(1, weight=1)
tela_gerar.grid_rowconfigure(0, weight=1)

# Frame das opções
frame_opcoes_gerar = tk.Frame(tela_gerar, bg=fundo)
frame_opcoes_gerar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_opcoes_gerar.grid_propagate(False)

label_gerar = tk.Label(frame_opcoes_gerar, text="Insira o link para gerar o QR Code:", bg=fundo, fg=cor_texto, font=fonte_padrao)
label_gerar.grid(row=0, column=0, sticky="w", padx=20, pady=10)

entrada = tk.Entry(frame_opcoes_gerar, width=40, font=fonte_padrao, validate="key", validatecommand=(validate_command, "%S", "%P"))
entrada.grid(row=1, column=0, padx=20, pady=5)

gerar_btn = tk.Button(frame_opcoes_gerar, text="Gerar QR Code", command=gerar_qr_code, bg="#4CAF50", fg="white", font=fonte_padrao)
gerar_btn.grid(row=2, column=0, pady=10, sticky="ew")

salvar_btn = tk.Button(frame_opcoes_gerar, text="Salvar Como", command=salvar_como, bg="#8BC34A", fg="white", font=fonte_padrao)
copiar_img_btn = tk.Button(frame_opcoes_gerar, text="Copiar Imagem", command=copiar_imagem, bg="#FF9800", fg="white", font=fonte_padrao)

# Botão Voltar
btn_voltar_gerar = tk.Button(frame_opcoes_gerar, text="Voltar", command=voltar_tela_inicial, bg="#FF5722", fg="white", font=fonte_padrao)
btn_voltar_gerar.grid(row=5, column=0, pady=(20, 0), sticky="ew")

# Frame do QR Code
frame_qr_code = tk.Frame(tela_gerar, bg="white")
frame_qr_code.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
frame_qr_code.grid_propagate(False)
frame_qr_code.grid_forget()

# Ajusta o Label para preencher o Frame
qr_code_label = tk.Label(frame_qr_code, bg="white")
qr_code_label.pack(expand=True, fill="both")

# Tela de Leitura de QR Code
tela_ler = tk.Frame(root, bg=fundo)
tela_ler.grid_columnconfigure(0, weight=3)
tela_ler.grid_columnconfigure(1, weight=2)
tela_ler.grid_rowconfigure(0, weight=1)
tela_ler.grid_rowconfigure(1, weight=1)

frame_opcoes_ler = tk.Frame(tela_ler, bg=fundo)
frame_opcoes_ler.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

label_ler = tk.Label(frame_opcoes_ler, text="Escolha uma imagem para ler o QR Code:", bg=fundo, fg=cor_texto, font=fonte_padrao)
label_ler.grid(row=0, column=0, sticky="w", padx=20, pady=10)

ler_btn = tk.Button(frame_opcoes_ler, text="Ler QR Code de Imagem", command=ler_qr_code, bg="#2196F3", fg="white", font=fonte_padrao)
ler_btn.grid(row=1, column=0, pady=10, sticky="ew")

copiar_btn = tk.Button(frame_opcoes_ler, text="Copiar Texto", command=copiar_para_clipboard, bg="#FF9800", fg="white", font=fonte_padrao)

btn_voltar_ler = tk.Button(frame_opcoes_ler, text="Voltar", command=voltar_tela_inicial, bg="#FF5722", fg="white", font=fonte_padrao)
btn_voltar_ler.grid(row=4, column=0, pady=(20, 0), sticky="ew")

frame_leitura = tk.Frame(tela_ler, bg="white")
frame_leitura.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
frame_leitura.grid_propagate(False)  # Impede que o frame ajuste seu tamanho ao conteúdo

resultado_texto = tk.Text(frame_leitura, height=20, width=40, wrap="word", font=fonte_padrao)
resultado_texto.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_leitura, command=resultado_texto.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

resultado_texto.config(yscrollcommand=scrollbar.set)

root.mainloop()