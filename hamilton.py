#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
from os import system
from json import *
from constantes import *

system('setfont Lat15-TerminusBold14')

# Motores
motor_esq = LargeMotor('outB')
motor_dir = LargeMotor('outC')

# Connect EV3 color and touch sensors to any sensor ports
sensor_esq = ColorSensor("in1")
sensor_dir = ColorSensor("in3")

# Put the color sensor into RGB mode.
sensor_esq.mode = 'RGB-RAW'
sensor_dir.mode = 'RGB-RAW'

button = Button()



def RGB(button):
    sensor_esq.mode = 'RGB-RAW'
    sensor_dir.mode = 'RGB-RAW'

    sensores = {'esquerdo branco': {}, 'direito branco': {}}
    sensores2 = {'esquerdo preto': {}, 'direito preto': {}}
    sensores3 = {'esquerdo verde': {}, 'direito verde': {}}
    total_esquerdo = {'tot branco esquerdo': {}, 'tot preto esquerdo': {}, 'tot verde esquerdo': {}}
    total_direito = {'tot branco direito': {}, 'tot preto direito': {}, 'tot verde direito': {}}

    # COMEÇA PELO BRANCO
    print("-----------------")
    print("---<<BRANCOS>>---")
    print("-----------------")
    print("")

    print("Pressione o botao do meio")
    print("")

    while True:
        if button.enter:
            red = sensor_esq.value(0)
            green = sensor_esq.value(1)
            blue = sensor_esq.value(2)

            sensores['esquerdo branco']['red'] = red
            sensores['esquerdo branco']['green'] = green
            sensores['esquerdo branco']['blue'] = blue
            total_esquerdo['tot branco esquerdo'] = red + green + blue

            red2 = sensor_dir.value(0)
            green2 = sensor_dir.value(1)
            blue2 = sensor_dir.value(2)

            sensores['direito branco']['red'] = red2
            sensores['direito branco']['green'] = green2
            sensores['direito branco']['blue'] = blue2

            total_direito['tot branco direito'] = red2 + green2 + blue2

            sleep(1)
            break
    system("clear")
    sleep(1)

    # AGORA VEM O  PRETOOO
    print("-----------------")
    print("---<<PRETOS>>----")
    print("-----------------")
    print("")

    print("Pressione o botao do meio!")

    while True:
        if button.enter:
            red = sensor_esq.value(0)
            green = sensor_esq.value(1)
            blue = sensor_esq.value(2)

            sensores2['esquerdo preto']['red'] = red
            sensores2['esquerdo preto']['green'] = green
            sensores2['esquerdo preto']['blue'] = blue
            total_esquerdo['tot preto esquerdo'] = red + green + blue

            red2 = sensor_dir.value(0)
            green2 = sensor_dir.value(1)
            blue2 = sensor_dir.value(2)

            sensores2['direito preto']['red'] = red2
            sensores2['direito preto']['green'] = green2
            sensores2['direito preto']['blue'] = blue2
            total_direito['tot preto direito'] = red2 + green2 + blue2

            sleep(1)
            break
    system("clear")
    sleep(1)

    # E POR ULTIMO O VERDE
    print("----------------")
    print("---<<VERDE>>---")
    print("----------------")
    print("")

    print("Pressione o botao! ")
    print("")

    while True:
        if button.enter:
            red = sensor_esq.value(0)
            green = sensor_esq.value(1)
            blue = sensor_esq.value(2)

            sensores3['esquerdo verde']['red'] = red
            sensores3['esquerdo verde']['green'] = green
            sensores3['esquerdo verde']['blue'] = blue
            total_esquerdo['tot verde esquerdo'] = red + green + blue

            red2 = sensor_dir.value(0)
            green2 = sensor_dir.value(1)
            blue2 = sensor_dir.value(2)

            sensores3['direito verde']['red'] = red2
            sensores3['direito verde']['green'] = green2
            sensores3['direito verde']['blue'] = blue2
            total_direito['tot verde direito'] = red2 + green2 + blue2

            sleep(1)
            break
    system("clear")
    sleep(1)

    arq = open('calibranco.txt', 'w')
    dump(sensores, arq)
    arq1 = open('calipreto.txt', 'w')
    dump(sensores2, arq1)
    arq2 = open('caliverde.txt', 'w')
    dump(sensores3, arq2)
    arq3 = open('totesquerdo.txt', 'w')
    dump(total_esquerdo, arq3)
    arq4 = open('totdireito.txt', 'w')
    dump(total_direito, arq4)

    arq.close()
    arq1.close()
    arq2.close()
    arq3.close()
    arq4.close()
    print("Os valores foram salvos!")


def lerDados():
    # Pega os valores do Arquivo Cali.txt onde estão os valores fixos em cada uma das cores com os sensores Esquerdo e Direito

    arq = open('calibranco.txt', 'r')
    sensores = load(arq)
    arq1 = open('calipreto.txt', 'r')
    sensores2 = load(arq1)
    arq2 = open('caliverde.txt', 'r')
    sensores3 = load(arq2)
    arq3 = open("totesquerdo.txt", "r")
    total_esquerdo = load(arq3)
    arq4 = open("totdireito.txt", "r")
    total_direito = load(arq4)

    return total_esquerdo, total_direito


def getSensorDireito(valorC):
    # Retorna o valor do sensor direito calibrado, na escala 0-100
    valorC = ((valorC["tot branco direito"] - sensor_dir.value()) / (
                valorC["tot branco direito"] - valorC["tot preto direito"])) * -100 + 100
    return valorC


def getSensorEsquerdo(valorC):
    # Retorna o valor do sensor direito calibrado, na escala 0-100
    valorC = ((valorC["tot branco esquerdo"] - sensor_dir.value()) / (
                valorC["tot branco esquerdo"] - valorC["tot preto esquerdo"])) * -100 + 100
    return valorC


def verde():
    # Função para executar 90º de acordo com qual sensor ele vê o verde

    sensor_esq.mode = 'RGB-RAW'
    sensor_dir.mode = 'RGB-RAW'

    verdeE = sensor_esq.value()
    verdeD = sensor_dir.value()

    verdeEA = total_esquerdo['tot verde esquerdo']
    verdeDA = total_direito['tot verde direito']

    '''if((verdeE==verdeEA ) and (verdeD==verdeDA)): 
    #condição para verificar se há dois verdes

        twoverde()'''

    if (verdeE == verdeEA):  # condição caso ele veja verde apenas com o sensor esquerdo

        # Primeiro anda um pouco para trás para verifica se a linha de tras é branca ou preta

        """
        TAVA  70 , COLOCOU 80 e melhorou, agora retornou para 70  !
        """
        '''motor_dir.run_to_rel_pos(position_sp=60, speed_sp=400, stop_action="hold")
        motor_esq.run_to_rel_pos(position_sp=60, speed_sp=400, stop_action="hold")
        sleep(0.5)

        stop()'''

        '''modifiquei as condições do verde'''

        '''if (sensor_esq.value() == 1): 
        #caso a linha atras seja preta ,ele compensa o que andou para tras para ignorar esse verde ( verde pós preto )


                        if(sensor_dir.value() > 3):


                            motor_esq.run_to_rel_pos(position_sp=-120, speed_sp=400, stop_action="hold")
                            motor_dir.run_to_rel_pos(position_sp=120, speed_sp=400, stop_action="hold")
                            sleep(0.5)

                            motor_dir.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")
                            motor_esq.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")



                        elif(sensor_dir.value() == 1 ) :

                            motor_dir.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")
                            motor_esq.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")

                            sleep(0.5)


        elif(sensor_esq.value() == 6): 
        #caso  a linha atras seja branca , quer dizer que é um verde normal , ou seja ele executa a funça normalmente 

            Sound.beep() '''

        motor_esq.run_to_rel_pos(position_sp=-50, speed_sp=400, stop_action="hold")
        motor_dir.run_to_rel_pos(position_sp=-50, speed_sp=400, stop_action="hold")
        sleep(0.5)

        motor_dir.run_to_rel_pos(position_sp=-120, speed_sp=400, stop_action="hold")
        motor_esq.run_to_rel_pos(position_sp=-120, speed_sp=400, stop_action="hold")
        sleep(0.5)

        motor_esq.run_to_rel_pos(position_sp=360, speed_sp=400, stop_action="hold")
        motor_dir.run_to_rel_pos(position_sp=-360, speed_sp=400, stop_action="hold")
        sleep(0.5)


    elif (verdeD == verdeDA):

        '''motor_dir.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
        motor_esq.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
        sleep(0.5)

        stop()

        if (sensor_dir.value() == 1):


                        if(sensor_esq.value() > 3):


                            motor_esq.run_to_rel_pos(position_sp=-120, speed_sp=400, stop_action="hold")
                            motor_dir.run_to_rel_pos(position_sp=120, speed_sp=400, stop_action="hold")
                            sleep(0.5)

                            motor_dir.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")
                            motor_esq.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")



                        elif(sensor_dir.value() == 1 ) :

                            motor_dir.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")
                            motor_esq.run_to_rel_pos(position_sp=-150, speed_sp=400, stop_action="hold")

                            sleep(0.5)


        elif(sensor_dir.value() == 6) : 
        #caso  a linha atras seja branca , quer dizer que é um verde normal , ou seja ele executa a funça normalmente 

            Sound.beep() '''

        motor_esq.run_to_rel_pos(position_sp=-50, speed_sp=400, stop_action="hold")
        motor_dir.run_to_rel_pos(position_sp=-50, speed_sp=400, stop_action="hold")
        sleep(0.5)

        motor_esq.run_to_rel_pos(position_sp=-120, speed_sp=400, stop_action="hold")
        motor_dir.run_to_rel_pos(position_sp=-120, speed_sp=400, stop_action="hold")
        sleep(0.5)

        motor_dir.run_to_rel_pos(position_sp=360, speed_sp=400, stop_action="hold")
        motor_esq.run_to_rel_pos(position_sp=-360, speed_sp=400, stop_action="hold")

        sleep(0.5)

    sensor_esq.mode = 'COL-REFLECT'
    sensor_dir.mode = 'COL-REFLECT'


def menu():
    # Faz a conexão entre o usuario e robô onde ele pode escolher entre
    # calibrar(botão Direito) os valores da pista e rodar(botão Esquerdo) o programa

    button = Button()

    print("<< Calibrar | Iniciar >>")

    while True:
        if button.left:
            system("clear")
            RGB(button)
            break
            system("clear")
            valorC = lerDados()
            # executar(kp,TP,valorC)
            break


sensor_esq.mode = 'COL-REFLECT'
sensor_dir.mode = 'COL-REFLECT'

print("Pressione o botao para comecar")
print("")

button = Button()

TP = -150.0
kp = 8
p = 0
valorC = lerDados()


def executar(kp, TP, valorC):
    while True:

        if ((valorC[ESQUERDA]['tot branco esquerdo']) - 2 < sensor_esq.value() < (valorC[ESQUERDA]['tot branco esquerdo']) + 2):
            verde()

        elif ((valorC[DIREITA]['tot branco direito']) - 2 < sensor_dir.value() < (valorC[DIREITA]['tot branco direito']) + 2):
            verde()

        offset = 5  # margem de erro para que ele fique reto na linha
        erro = ((
                            sensor_esq.value() - sensor_dir.value()) + offset)  # Calcula o erro para que ele sempre siga a linha preta
        p = kp * erro  # constante proporcional
        # anda de acordo com o erro calculado

        motor_esq.run_forever(speed_sp=TP - p)
        motor_dir.run_forever(speed_sp=TP + p)


executar(kp, TP, valorC)