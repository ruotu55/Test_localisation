import os
import sys
import random
import string
from PIL import ImageFont, ImageDraw, Image

def obter_largura_pixel_texto(texto, caminho_fonte='/usr/share/fonts/truetype/alegreya-sc/AlegreyaSansSC-Black.ttf', tamanho_fonte=10):
    fonte = ImageFont.truetype(caminho_fonte, tamanho_fonte)
    imagem = Image.new('RGB', (1, 1))
    desenho = ImageDraw.Draw(imagem)
    caixa_limites = desenho.textbbox((0, 0), texto, fonte=fonte)
    largura = caixa_limites[2] - caixa_limites[0]
    return largura

def gerar_palavra(caminho_fonte, tamanho_fonte):
    letras = 'abcdefghijklmnopqrstuvwxyzáéíóúàèìòùâêîôûãõç'
    comprimento = random.randint(1, 10)  # Varia o comprimento das palavras
    palavra = ''.join(random.choice(letras) for _ in range(comprimento))
    return palavra.capitalize()  # Capitaliza a primeira letra de cada palavra

def gerar_frase_com_largura(largura_desejada, caminho_fonte, tamanho_fonte, max_tentativas=1000):
    largura_espaco = obter_largura_pixel_texto(' ', caminho_fonte, tamanho_fonte)
    for _ in range(max_tentativas):
        num_palavras = random.randint(1, 3)
        palavras = [gerar_palavra(caminho_fonte, tamanho_fonte) for _ in range(num_palavras)]
        frase = ' '.join(palavras)
        largura_frase = obter_largura_pixel_texto(frase, caminho_fonte, tamanho_fonte)
        if largura_frase == largura_desejada:
            return frase
        elif largura_frase > largura_desejada:
            continue  # Ignora frases muito longas

    return None  # Retorna None se não encontrar uma frase com a largura desejada dentro de max_tentativas

def main(largura_desejada):
    caminho_fonte = '/usr/share/fonts/truetype/alegreya-sc/AlegreyaSansSC-Black.ttf'
    tamanho_fonte = 10
    try:
        largura_desejada = int(largura_desejada)
        frases = []
        for _ in range(50):
            frase = gerar_frase_com_largura(largura_desejada, caminho_fonte, tamanho_fonte)
            if frase:
                frases.append(frase)
            else:
                print(f"Não foi possível gerar uma frase com largura de {largura_desejada} pixels.")
                break

        texto_resumo = f"Geradas {len(frases)} frases com largura de {largura_desejada} pixels:\n\n"
        for frase in frases:
            texto_resumo += f"{frase}\n"
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as arquivo_resumo:
            arquivo_resumo.write(texto_resumo)
        print(texto_resumo)
    except IOError:
        print(f"Arquivo de fonte '{caminho_fonte}' não encontrado. Certifique-se de que o arquivo de fonte esteja presente no diretório ou atualize o caminho da fonte.")
    except ValueError:
        print("Forneça um número inteiro válido para a largura desejada.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python Pixel_box_final_generator.py <largura_desejada>")
        sys.exit(1)
    largura_desejada = sys.argv[1]
    main(largura_desejada)
