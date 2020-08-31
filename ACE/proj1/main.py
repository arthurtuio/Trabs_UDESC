from math import sqrt, pi  # Importando a função raiz e o número pi
from numpy import arange # Para criar um vetor com steps iguais
from matplotlib import pyplot as plt, legend  # Para realizar os plots


class Proj_1():
    def __init__(self):
        """
        Dfinições das variáveis iniciais.
        """
        self.numero_polos = 4
        self.freq = 60  # [Hz]
        self.potencia = 2 * 745.7  # Potência [W] (2 hp)

        self.Vf = 220  # Velocidade Nominal[V]
        self.Vf_6_step = round((220 * sqrt(2)/pi), 4)
        self.Vf_PWM = round((220 * sqrt(2))/(pi * 0.6), 4)

        self.rot_nominal = 1720  # Velocidade Nominal [rpm]
        self.ws = 1800  #

        self.mom_inercia = 0.018  # [kgm²]
        self.coef_atr_visc = 0.0018  # Coeficiente atrito viscoso, [Nms]
        self.rs = 4.08 # Resistência do Estator [ohms]
        self.rr = 4.87 # Resistência do Rotor [ohms]

        self.Lm = 315 * (10 ** -3) # Indutância Mútua [H]
        self.Lls = 10.4 * (10 ** -3) # Indutância do Estator [H]
        self.Llr = 18.5 * (10 ** -3) # Indutância do Rotor [H]

        # Vetores
        self.Te = []
        self.Te6 = []
        self.Tep = []

        self.rpm = []
        self.Pmec = []
        self.Pmec6 = []
        self.Pmecp = []

        self.I1 = []
        self.I16 = []
        self.I1p = []

        self.I2 = []
        self.I26 = []
        self.I2p = []

        self.Pg = []
        self.Pg6 = []
        self.Pgp = []

        self.Prot = []
        self.Prot6 = []
        self.Protp = []

        self.Pest = []
        self.Pest6 = []
        self.Pestp = []

        self.Pe = []
        self.Pe6 = []
        self.Pep = []

        self.Pin = []
        self.Pin6 = []
        self.Pinp = []

        self.cos_phi = []
        self.cos_phi6 = []
        self.cos_phip = []

        self.Rend = []
        self.Rend6 = []
        self.Rendp = []

    #def get_values(self):

    def calculate(self):
        """
        Faz os cálculos.
        """
        X1 = 2 * pi * self.freq * self.Lls # Reatância Indutiva do Estator [ohms]
        X2 = 2 * pi * self.freq * self.Llr # Reatância Indutiva do Rotor [ohms]
        Xm = 2 * pi * self.freq * self.Lm # Reatância Indutiva Mútua [ohms]

        x12 = round(X1 + X2, 4)

        V1 = round(abs((self.Vf * 1j * Xm) / (self.rs + (X1 + Xm))), 4)
        V16 = round(abs((self.Vf_6_step * 1j * Xm) / (self.rs + (X1 + Xm))), 4)
        V1p = round(abs((self.Vf_6_step * 1j * Xm) / (self.rs + (X1 + Xm))), 4)

        Tmax = round((self.Vf ** 2) / (self.freq * 2 * x12), 4)

        T1 = round(((self.Vf ** 2) * self.rr) / (x12 ** 2), 4)

        s_max = round(((self.Vf ** 2) * self.rr) / (self.freq * (x12 ** 2) * Tmax), 4)

        # Inicializando os vetores
        array = arange(start=1, stop=0.00001, step=-0.001)
        i = 0

        for step in array:
            # Torque Elétrico
            self.Te.append(self.calc_Electric_Torque(self.Vf, step, x12))
            self.Te6.append(self.calc_Electric_Torque(self.Vf_6_step, step, x12))
            self.Tep.append(self.calc_Electric_Torque(self.Vf_PWM, step, x12))

            # RPM
            self.rpm.append(self.calc_Rpm(step))

            # Potência Mecânica # certo
            self.Pmec.append(self.calc_Mechanical_Power(self.Te[i], step))
            self.Pmec6.append(self.calc_Mechanical_Power(self.Te6[i], step))
            self.Pmecp.append(self.calc_Mechanical_Power(self.Tep[i], step))

            # Corrente 1
            self.I1.append(self.calc_Current_1(self.Vf, step, Xm))
            self.I16.append(self.calc_Current_1(self.Vf_6_step, step, Xm))
            self.I1p.append(self.calc_Current_1(self.Vf_PWM, step, Xm))

            # Corrente 2
            self.I2.append(self.calc_Current_2(self.Pmec[i], step))
            self.I26.append(self.calc_Current_2(self.Pmec6[i], step))
            self.I2p.append(self.calc_Current_2(self.Pmecp[i], step))

            # Potência Transferida do Entreferro
            self.Pg.append(self.calc_Tranferred_Power_across_AirGap(self.I2[i], step))
            self.Pg6.append(self.calc_Tranferred_Power_across_AirGap(self.I26[i], step))
            self.Pgp.append(self.calc_Tranferred_Power_across_AirGap(self.I2p[i], step))

            # Perdas no Rotor
            self.Prot.append(self.calc_Rotor_Losses(self.Pg[i], step))
            self.Prot6.append(self.calc_Rotor_Losses(self.Pg6[i], step))
            self.Protp.append(self.calc_Rotor_Losses(self.Pgp[i], step))

            # Perdas no Estator
            self.Pest.append(self.calc_Stator_Losses(self.I1[i]))
            self.Pest6.append(self.calc_Stator_Losses(self.I16[i]))
            self.Pestp.append(self.calc_Stator_Losses(self.I1p[i]))

            # Potência de Entrada
            self.Pin.append(self.Pg[i] + self.Pest[i])
            self.Pin6.append(self.Pg6[i] + self.Pest6[i])
            self.Pinp.append(self.Pgp[i] + self.Pestp[i])

            # Cosseno Phi
            self.cos_phi.append(V1/self.I1[i])
            self.cos_phi6.append(V16/self.I16[i])
            self.cos_phip.append(V1p/self.I1p[i])

            # Rendimento
            self.Rend.append(self.calc_Yield(self.Pin[i], self.Pest[i], self.Prot[i]))
            self.Rend6.append(self.calc_Yield(self.Pin6[i], self.Pest6[i], self.Prot6[i]))
            self.Rendp.append(self.calc_Yield(self.Pinp[i], self.Pestp[i], self.Protp[i]))

            i += 1

        self._create_plots()

    def _create_plots(self):
        """
        Cria os plots.
        """
        # Torque Elétrico
        plt.figure(1)
        plt.plot(self.rpm, self.Te, 'g', label='Normal')
        plt.plot(self.rpm, self.Te6, 'r', label='Six-step')
        plt.plot(self.rpm, self.Tep, 'b', label='PWM')
        plt.xlabel("rpm")
        plt.ylabel("Te[N.m]")
        plt.title("Torque elétrico x rpm")
        plt.legend()

        # Potência Elétrica
        plt.figure(2)
        plt.plot(self.rpm, self.Pin, 'g', label='Normal')
        plt.plot(self.rpm, self.Pin6, 'r', label='Six-step')
        plt.plot(self.rpm, self.Pinp, 'b', label='PWM')
        plt.xlabel("rpm")
        plt.ylabel("Pin")
        plt.title("Potência elétrica entrada x rpm")
        plt.legend()

        # Potência Mecânica
        plt.figure(3)
        plt.plot(self.rpm, self.Pmec, 'g', label='Normal')
        plt.plot(self.rpm, self.Pmec6, 'r', label='Six-step')
        plt.plot(self.rpm, self.Pmecp, 'b', label='PWM')
        plt.xlabel("rpm")
        plt.ylabel("Pmec")
        plt.title("Potência mecânica x rpm")
        plt.legend()

        # Rendimento
        plt.figure(4)
        plt.plot(self.rpm, self.Rend, 'g', label='Normal')
        plt.plot(self.rpm, self.Rend6, 'r', label='Six-step')
        plt.plot(self.rpm, self.Rendp, 'b', label='PWM')
        plt.xlabel("rpm")
        plt.ylabel("Rendimento")
        plt.title("Rendimento x rpm")
        plt.legend()

        # Cos Phi
        plt.figure(5)
        plt.plot(self.rpm, self.cos_phi6, 'r', label='Six-step')
        plt.plot(self.rpm, self.cos_phip, 'b', label='PWM')
        plt.xlabel("rpm")
        plt.ylabel("cos_phi")
        plt.title("Cos(\phi)")
        plt.legend()

        plt.show()

    @staticmethod
    def create_complex_num(input):
        """
        Funcao auxiliar pra criar numero complexo.
        Espera um parametro de entrada e retorna o numero complexo dessa entrada.
        :param input: A entrada, o valor que se quer converter para complexo.
        :return: O numero complexo da entrada
        """
        return complex(0, input)

    def calc_Electric_Torque(self, input_voltage, step, x12):
        """
        Calcula o torque equivalente data a tensão de entrada, o step do iterador, e o valor de x12
        :param input_tension: A tensão de entrada
        :return: O torque equivalente
        """
        num = ((input_voltage ** 2) * self.rr)
        den = (step * self.freq * ((x12 ** 2) + (self.rr/step) ** 2))
        return round(num/den, 4)

    def calc_Mechanical_Power(self, eletric_torque, step):
        """
        Calcula a Potência Mecânica dado o Torque Elétrico de entrada e o step do iterador.
        :param eletric_torque: Torque Elétrico
        :param step: Step do for
        :return: O valor da Potência mecânica
        """
        return round((1-step)*eletric_torque*(self.ws*pi/60), 4)

    def calc_Current_1(self, input_voltage, step, x12):
        """
        Calcula a Corrente 1 dada a tensão de entrada, o step do iterador, e x12.
        :param input_voltage: Tensão de entrada
        :param step: Step do for
        :param x12:
        :return: O valor da Corrente 1
        """
        den = sqrt(
            (x12 ** 2) + ((self.rr/step) ** 2)
        )
        return round(input_voltage/den, 4)

    def calc_Current_2(self, mech_power, step):
        """
        Calcula a Corrente 2 dada a Potência Mecânica e o step do iterador
        :param mech_power: A Potência Mecânica
        :param step: Step do for
        :return: O valor da Corrente 2
        """
        num = sqrt((mech_power*step))
        den = 3*self.rr*(1-step)
        return round(num/den, 4)

    def calc_Tranferred_Power_across_AirGap(self, I2, step):
        """
        Calcula a Potência Transferida do entreferro, com base na Corrente 2 e no step do iterador
        :param I2: A Corrente 2
        :param step: Step do for
        :return: O valor da Potência Transferida do entreferro
        """
        return round(
            (3*(I2 ** 2)*self.rr)/step, 4
        )

    def calc_Rotor_Losses(self, Pg, step):
        """
        Calcula as perdas no rotor, com base na Potência Transferida do Entreferro e o step do iterador.
        :param Pg: Potência Transferida do entreferro
        :param step: Step do for
        :return: O valor da perda no rotor
        """
        return round(step*Pg, 4)

    def calc_Stator_Losses(self, I1):
        """
        Calcula a Perda no Estator, com base na Corrente 1.

        :param I1: A Corrente 1
        :return: O valor da Potência no Estator
        """
        return round(
            (3*(I1 ** 2)*self.rs), 4
        )

    def calc_Rpm(self, step):
        """
        Calcula o rpm.
        :param step: Step do for
        :return: o Rpm
        """
        return self.ws*(1 - step)

    def calc_Cos_Phi(self, V1, I1):
        """
        Calcula o Cosseno de Phi, dada a tensão de entrada e a corrente de entrada.
        :param V1: A Tensão de entrada 1
        :param I1: A corrente de entrada 1
        :return: O valor do Cos.
        """
        return V1/I1

    def calc_Yield(self, Pin, Pest, Prot):
        """
        Calcula o Rendimento, com base na potência de entrada, perda no rotor e
        perda do estator.
        :param input_power: Potência de entrada
        :param rotor_loss: Perda no rotor
        :param shaft_power: Potência no estator
        :return: O valor do rendimento
        """

        den = Pin + Pest + Prot

        return round(Pin/den, 4)


obj = Proj_1()
obj.calculate()