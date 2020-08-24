## Importação de bibliotecas auxiliares
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np

def questao_1():

    """
    Letra a)
    Do enunciado, sabemos que Tc = 0.
    Analisando o gráfico, podemos retirar os dados da variação (chamada
    de alpha) de omega para cada tempo de intervalo mostrado. Disso foram
    criados dois arrays:
        :array alpha: expressado em rad/s²
        :array time: expressado em s
    Sabendo-se que o Torque Eletromagnético (Tem) é dado pela multiplicação de
    Jeq e alpha, assim conseguimos, para cada valor de alpha, um valor para Tem.
    Após isto, basta fazermos um plot do gráfico, usando a bilbioteca matplotlib.

    Observações:
        - Jeq ficará em aberto na equação, para que seja possível plotar
    o gráfico.
        - Foram adicionados alguns pontos ao gráfico, de forma que o plot
        ficasse correto via matplotlib

    :return: O gráfico do Tem em função do tempo

    Letra b)
    Basta integrar a equação dW = J.w.dw, que chegamos em W = (1/2)*J.w²
    """

    ### Letra a

    ## Inicialização de variáveis
    alpha_array = [
        100,100,
        0,0,
        -100,-100,
        0,0]

    time_array = [
        0,1,
        1,2,
        2,3,
        3,4
    ]

    ## Cálculo do Tem
    plt.plot(time_array,alpha_array)
    plt.xlabel("time")
    plt.ylabel("EM Torque")
    plt.title("EM Torque as a function of time")

    print("Resultado questão 2a:")
    print("Observar o gráfico")

    ### Letra b
    print("Resultado questão 2b:")
    print("W = (1/2)*J.w²")

    plt.show()

def questao_2():
    """
    Para determinar o raio da polia necessário, iremos usar, do enunciado,
    as seguintes variáveis:
        :parameter mass: 0,02 kg
        :parameter motor_inertia: 4.10^-6 kg.m²
        :parameter load_force: 0
    Sabemos também que com Tem = 0, conseguimos chegar numa relação
    motor_inertia = mass*(radius²)
    :return: O raio da polia necessário
    """

    ## Inicialização de variáveis
    mass = 0.02 # kg
    motor_inertia = 0.000004 # kg.m²

    ## Cálculo do raio
    radius = round(sqrt(motor_inertia/mass),4) #m

    ## print do resultado em tela
    print("Resultado questão 2:")
    print("O valor do raio é de: {} m".format(radius))

def questao_3():
    """
    Questao não foi unicamente implementada via python.
    Para conferir as equacoes, ver o PDF. Aqui apenas foi criado
    o gráfico da mesma.

    Observações:
        - Foram adicionados alguns pontos aos arrays, de forma que o plot
    ficasse correto via matplotlib

    :return: O gráfico do Tem em função do tempo
    """

    ## Inicialização de variáveis
    EM_torque_array = [
        77,77,
        0,0,
        -77,-77,
        0,0]

    time_array = [
        0,1,
        1,2,
        2,3,
        3,4
    ]

    ## Cálculo do Tem
    plt.plot(time_array,EM_torque_array)
    plt.xlabel("time")
    plt.ylabel("EM Torque")
    plt.title("EM Torque as a function of time")

    print("Resultado questão 3:")
    print("Observar o gráfico")

    plt.show()

def questao_4():
    """
    Para calcular a máxima potência requirida de cada motor, iremos usar,
    do enunciado, as seguintes variáveis:
        :parameter mass: O peso total do veículo, sendo de 2000 kg.
        :parameter speed: A velocidade, em km/h, que posteriormente
        será transformada em m/s, que tem o valor de 96,54 km/h ou
        26,8 m/s após conversão
    As equacoes que usaremos para resolução serão para cálculo da força, e
    também da aceleração

    :return: A potência máxima requirida para cada motor
    """

    ## Inicialização de variáveis
    mass = 2000 # kg
    time = 10 # s
    speed = 26.8 # m/s
    initial_speed = 0 # m/s

    ## Calculo da aceleração
    acceleration = (speed-initial_speed)/time

    ## Calculo da Força
    Force = mass*acceleration

    ## Calculo da potência total
    Power = Force*speed # N*m/s = W

    ## Conversao da potência para cada motor
    single_motor_power = round(Power/4,1)

    ## print do resultado em tela
    print("Resultado questão 4:")
    print("A máxima potência requirida para cada motor é de: {} W".format(single_motor_power))

def questao_5():
    """
    Para calcular o ciclo médio de trabalho, basta fazer um cálculo similar
    ao de uma média ponderada, multiplicando cada valor da potência (descrito
    pela variável 'HP_array') pela sua duração correspondente no tempo
    (variavel 'time_array'), e depois dividir isso pelo somatório do tempo.

    Justamente por isso, se usou uma função da bilbioteca numpy, chamada
    'average', que já faz esse cálculo, recebendo dois parâmetros de entrada:
        :parameter a: o vetor contendo os valores que se quer a média
        :parameter weights: o vetor contendo os pesos

    :return: O ciclo medio de trabalho, expressado pela variavel
    'average_work_cycle'
    """

    ## Inicialização de variáveis

    HP_array = [
        40,80,30,45,0
    ]

    time_array = [
        6,10,3,10,16
    ]

    ## Cálculo do ciclo médio de trabalho

    average_work_cycle = np.average(a=HP_array, weights=time_array)

    ## print do resultado em tela

    print("Resultado questão 5:")
    print("O ciclo médio de trabalho é {} HP".format(round(average_work_cycle,2)))
    print("A potência mais próxima desta no enunciado é a de 40 HP")

## Digite aqui qual questão vocẽ quer executar
## Exemplo: questao_1()
questao_5()