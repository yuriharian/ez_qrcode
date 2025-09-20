import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import pyperclip


def trocar_tela(tela_atual, tela_destino):
    # Esconde a tela atual e mostra a tela de destino dentro da mesma janela
    tela_atual.pack_forget()
    tela_destino.pack(fill="both", expand=True)


# Janela principal (única)
root = tb.Window(themename="superhero")
root.title("EZ QR Code")
root.geometry("800x480")
root.resizable(False, False)
try:
    root.iconbitmap("ez_qrcode.ico")
except Exception as e:
    print(f"Erro ao definir ícone: {e}")

fonte_padrao = ("Helvetica", 12)

# ---------------- Tela Inicial ----------------

tela_inicial = tb.Frame(root)
tela_inicial.pack(fill="both", expand=True)
container_inicial = tb.Frame(tela_inicial)
container_inicial.pack(expand=True)
label_bem_vindo = tb.Label(
    container_inicial,
    text="Escolha uma opção",
    font=("Helvetica", 18),
    bootstyle=INFO,
)
label_bem_vindo.pack(pady=24)
btn_gerar_qr = tb.Button(
    container_inicial,
    text="Gerar QR Code",
    command=lambda: trocar_tela(tela_inicial, tela_gerar),
    bootstyle=SUCCESS,
    width=24,
)
btn_gerar_qr.pack(pady=8)
btn_ler_qr = tb.Button(
    container_inicial,
    text="Ler QR Code",
    command=lambda: trocar_tela(tela_inicial, tela_ler),
    bootstyle=PRIMARY,
    width=24,
)
btn_ler_qr.pack(pady=8)

# ---------------- Tela Gerar QR Code ----------------

tela_gerar = tb.Frame(root)
# layout em 2 colunas: menu à esquerda, conteúdo à direita
tela_gerar.columnconfigure(0, weight=0)
tela_gerar.columnconfigure(1, weight=1)
tela_gerar.rowconfigure(0, weight=1)

menu_gerar = tb.Frame(tela_gerar)
menu_gerar.grid(row=0, column=0, sticky="nsw", padx=12, pady=12)
conteudo_gerar = tb.Frame(tela_gerar)
conteudo_gerar.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)

label_gerar = tb.Label(
    menu_gerar,
    text="Insira o link para gerar o QR Code:",
    font=fonte_padrao,
    bootstyle=INFO,
)
label_gerar.pack(pady=(0, 8), anchor="w")
entrada = tb.Entry(menu_gerar, width=40, font=fonte_padrao)
entrada.pack(pady=6, anchor="w")

frame_qr_code = tb.Frame(conteudo_gerar)
frame_qr_code.pack(expand=True, fill="both")
qr_code_label = tb.Label(frame_qr_code)
qr_code_label.pack(expand=True, fill="both")


def exibir_qr_code(img):
    img_tk = ImageTk.PhotoImage(img)
    qr_code_label.config(image=img_tk)
    qr_code_label.image = img_tk
    qr_code_label.qr_image = img


def gerar_qr_code():
    link = entrada.get().strip()
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
    img = img.convert("RGB")
    img.thumbnail((320, 320))
    exibir_qr_code(img)
    salvar_btn.config(state=NORMAL)


def salvar_como():
    if not hasattr(qr_code_label, "qr_image"):
        messagebox.showwarning("Aviso", "Gere um QR Code primeiro.")
        return
    caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile="qrcode.png",
            filetypes=[("PNG files", "*.png")],
    )
    if caminho_arquivo:
        qr_code_label.qr_image.save(caminho_arquivo)
        messagebox.showinfo("Sucesso", f"QR Code salvo em:\n{caminho_arquivo}")




gerar_btn = tb.Button(menu_gerar, text="Gerar QR Code", command=gerar_qr_code, bootstyle=SUCCESS, width=24)
gerar_btn.pack(pady=(12, 6), anchor="w")
salvar_btn = tb.Button(menu_gerar, text="Salvar Como", command=salvar_como, bootstyle=SUCCESS, width=24, state=DISABLED)
salvar_btn.pack(pady=6, anchor="w")
btn_voltar_gerar = tb.Button(
    menu_gerar,
    text="Voltar",
    command=lambda: trocar_tela(tela_gerar, tela_inicial),
    bootstyle=DANGER,
    width=24,
)
btn_voltar_gerar.pack(pady=(16, 0), anchor="w")

# ---------------- Tela Ler QR Code ----------------

tela_ler = tb.Frame(root)
tela_ler.columnconfigure(0, weight=0)
tela_ler.columnconfigure(1, weight=1)
tela_ler.rowconfigure(0, weight=1)

menu_ler = tb.Frame(tela_ler)
menu_ler.grid(row=0, column=0, sticky="nsw", padx=12, pady=12)
conteudo_ler = tb.Frame(tela_ler)
conteudo_ler.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)

label_ler = tb.Label(
    menu_ler,
    text="Escolha uma imagem para ler o QR Code:",
    font=fonte_padrao,
    bootstyle=INFO,
)
label_ler.pack(pady=(0, 8), anchor="w")

area_texto_frame = tb.Frame(conteudo_ler)
area_texto_frame.pack(expand=True, fill="both")
resultado_texto = tb.Text(area_texto_frame, height=10, width=50, wrap="word", font=fonte_padrao)
resultado_texto.pack(side="left", fill="both", expand=True)
scrollbar = tb.Scrollbar(area_texto_frame, command=resultado_texto.yview)
scrollbar.pack(side="right", fill="y")
resultado_texto.config(yscrollcommand=scrollbar.set)


def ler_qr_code():
    caminho_imagem = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if not caminho_imagem:
        return
    try:
        img = Image.open(caminho_imagem)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
        return
    try:
        resultado = decode(img)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na leitura do QR Code: {e}")
        return
    if resultado:
        # Pode haver mais de um QR na imagem; concatenamos resultados
        textos = []
        for obj in resultado:
            try:
                textos.append(obj.data.decode("utf-8"))
            except Exception:
                textos.append(str(obj.data))
        resultado_texto.delete(1.0, "end")
        resultado_texto.insert("end", "\n".join(textos))
        copiar_btn.config(state=NORMAL)
    else:
        messagebox.showwarning("Aviso", "Nenhum QR Code encontrado na imagem.")


def copiar_para_clipboard():
    texto = resultado_texto.get(1.0, "end").strip()
    if texto:
        pyperclip.copy(texto)
        messagebox.showinfo("Copiado", "O conteúdo foi copiado para a área de transferência.")


ler_btn = tb.Button(menu_ler, text="Ler QR Code de Imagem", command=ler_qr_code, bootstyle=PRIMARY, width=24)
ler_btn.pack(pady=8, anchor="w")
copiar_btn = tb.Button(menu_ler, text="Copiar Texto", command=copiar_para_clipboard, bootstyle=WARNING, width=24, state=DISABLED)
copiar_btn.pack(pady=6, anchor="w")
btn_voltar_ler = tb.Button(
    menu_ler,
    text="Voltar",
    command=lambda: trocar_tela(tela_ler, tela_inicial),
    bootstyle=DANGER,
    width=24,
)
btn_voltar_ler.pack(pady=(16, 0), anchor="w")

# Inicia app (apenas um mainloop)
root.mainloop()