# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 09:33:46 2021

@author: tsfei
"""
# importação das packages necessárias
import cv2
from PIL import Image
    
# versão simplificada de uma função sigmoide para comparação de cores
def sigmoid_lin(x1,x2):
    if abs(x1-x2) < 20:
        return 1
    if abs(x1-x2) > 30:
        return 0
    return -abs(x1-x2)/10 + 3

# função para comparar as cores de dois pixeis (pix1 e pix2)
def compare_pixels(pix1, pix2):
    return sigmoid_lin(pix1[0],pix2[0])*sigmoid_lin(pix1[1],pix2[1])*sigmoid_lin(pix1[2],pix2[2])

start_time = time.time()

# nomes dos ficheiros de video a analisar
videos = [
    '0.15ml.min_20rpm_cropped.mp4',
    '0.15ml.min_50rpm_cropped.mp4',
    '0.15ml.min_100rpm_cropped.mp4',
    '0.25ml.min_20rpm_cropped.mp4',
    '0.25ml.min_50rpm_cropped.mp4',
    '0.25ml.min_100rpm_cropped.mp4'
    ]
# cores finais das soluções misturadas de cada video
color = [
    [[127,183,142],[111,116,39]], #7fb78e + #6f7427
    [[0,140,136],[0,55,25]], #008c88 + #00370f
    [[0,118,118],[1,73,32]], #007676 + #014920
    [[0,117,126],[0,43,25]], #00757e + #002b15
    [[0,127,127],[0,64,46]], #007f7f + #00402e
    [[0,58,60],[0,38,25]] #003a3c + #002619
    ]
# arrays para guardar os valores e os tempos
val = [[],[],[],[],[],[]]
times = [[],[],[],[],[],[]]

# itera-se por todos os videos
for j in range(len(videos)):
    # guarda-se o video num formato analisável
    vidcap = cv2.VideoCapture(videos[j])
    # e extrai-se o primeiro frame
    # success: True se a leitura funcionar, False quando se chega ao fim do video
    success,image = vidcap.read() 
    # variavel count serve para saber quantos frames já foram lidos por video
    count = 0
    # como se vai fazer a média a cada 4 frames, part serve para controlar isso
    part = 0
    while success:
        if (count % 2) == 0:
            print('Success:', success, 'Frames read:', count)
            # quando já se extraiu 4 frames
            if part == 4:
                # faz-se a média e dá-se reset a part
                val[j][len(val[j]) - 1] /= 4
                part = 0
            # quando part for 0
            if part == 0:
                # acrescenta-se um novo valor aos valores e aos tempos
                val[j].append(0)
                times[j].append((count + 2)/30)
            # guardar a imagem num formato analisável (PIL.Image)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            im = Image.fromarray(image)
            # e extrair os pixeis para um array
            pixels = list(im.getdata())
            # para todos os pixeis
            for i in range(len(pixels)):
                # soma-se o valor da comparação com o final ao valor do frame
                val[j][len(val[j]) - 1] += (
                                            compare_pixels(pixels[i],color[j][0]) +
                                            compare_pixels(pixels[i],color[j][1])
                                            )
            # incrementa-se as variáveis de controlo e lê-se um novo frame
            part += 1
        count += 1
        success,image = vidcap.read()
# Criação de um ficheiro para escrever o output
output = open('data.txt', 'w')
for j in range(len(videos)):
    print('VIDEO', videos[j], file=output)
    for k in range(len(val[j])):
        print('Time', times[j][k], 'Value', val[j][k], file=output)
output.close()

print("--- %s seconds ---" % (time.time() - start_time))
