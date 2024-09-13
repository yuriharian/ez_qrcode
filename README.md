# ez_qrcode

`ez_qrcode` é uma aplicação Python com interface gráfica que permite gerar códigos QR a partir de URLs ou textos e ler códigos QR a partir de imagens.

## Funcionalidades

- **Geração de QR Code**: Gere códigos QR a partir de URLs ou textos.
- **Leitura de QR Code**: Leia e decodifique códigos QR a partir de arquivos de imagem.
- **Salvar QR Codes**: Salve códigos QR gerados como arquivos de imagem (`.png`).
- **Copiar QR Codes**: Copie a imagem do código QR gerado para a área de transferência.
- **Copiar Dados Decodificados**: Copie os dados decodificados do código QR para a área de transferência.

## Requisitos

Para rodar a aplicação, você precisa das seguintes bibliotecas Python:

- `tkinter`
- `qrcode`
- `Pillow`
- `pyzbar`
- `pyperclip`

Instale as dependências usando `pip`:

```bash
pip install qrcode[pil] pillow pyzbar pyperclip
```

## Rodando a Aplicação
1. Clone o repositório:
```bash
git clone https://github.com/yuriharian/ez_qrcode.git
```
2. Navegue até o diretório do projeto:
```bash
cd ez_qrcode
```
3. Execute a aplicação:
```bash
python ez_qrcode.py
```
## Executável

Para facilitar o uso, um arquivo executável está disponível na seção de Releases deste repositório. Você pode baixar o arquivo executável da última release e executá-lo diretamente em seu sistema, sem a necessidade de instalar Python.

## Licença

Este projeto está licenciado sob a Licença MIT.
