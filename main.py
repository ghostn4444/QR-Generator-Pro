import qrcode
from PIL import Image
from colorama import Fore, Style, init

init(autoreset=True)


def banner():
    print(Fore.CYAN + """
========================================
        QR CODE GENERATOR PRO
   (Logo • Gradiente • Personalizado)
========================================
""")


def escolher_cor(msg, padrao):
    cor = input(msg).strip()
    return cor if cor else padrao


def gerar_qr():
    banner()

    url = input(Fore.YELLOW + "Digite o link: ").strip()
    if not url:
        print(Fore.RED + "Link inválido!")
        return

    nome = input("Nome do arquivo (sem extensão): ").strip() or "qrcode"

    usar_cor = input("Usar cor personalizada? [y/N]: ").strip().lower()

    usar_gradiente = input("Usar gradiente? [y/N]: ").strip().lower()

    usar_logo = input("Adicionar logo no centro? [y/N]: ").strip().lower()

    # Config QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # importante p/ logo
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Cores
    fill_color = "black"
    back_color = "white"

    if usar_cor == "y":
        fill_color = escolher_cor("Cor do QR (ex: black, #0000FF): ", "black")
        back_color = escolher_cor("Cor de fundo (ex: white, #FFFFFF): ", "white")

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # Gradiente (simples vertical overlay)
    if usar_gradiente == "y":
        gradient = Image.new("RGB", img.size)
        for y in range(img.size[1]):
            r = int(255 * (y / img.size[1]))
            g = 0
            b = 255 - r
            for x in range(img.size[0]):
                gradient.putpixel((x, y), (r, g, b))

        img = Image.blend(img, gradient, alpha=0.4)

    # Logo no centro
    if usar_logo == "y":
        try:
            logo_path = input("Caminho do logo (PNG recomendado): ").strip()
            logo = Image.open(logo_path)

            base_width = img.size[0] // 4
            logo = logo.resize((base_width, base_width))

            pos = (
                (img.size[0] - logo.size[0]) // 2,
                (img.size[1] - logo.size[1]) // 2
            )

            img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

        except Exception as e:
            print(Fore.RED + f"Erro ao adicionar logo: {e}")

    output = f"{nome}.png"
    img.save(output)

    print(Fore.GREEN + f"\nQR Code gerado com sucesso: {output}")


if __name__ == "__main__":
    gerar_qr()
