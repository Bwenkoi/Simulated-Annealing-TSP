import math
import random
import tsp_view
import matplotlib.pyplot as plt


class RecozimentoSimulado(object):
    def __init__(self, coordenadas):
        # Definições Iniciais das Coordenadas e Tamanho do Espaço
        self.coords = coordenadas
        self.N = len(coordenadas)

        # Define a Temperatura de Maneira Dinamica
        self.T = math.sqrt(self.N)
        # Define o Resfriamento e o critério de parada
        self.taxa_resfriamento = 0.995
        self.temperatura_de_parada = 1e-10

        # Definição do Máximo de Iterações - Usado como Possível Critério de Parada
        self.iteracao = 1
        self.max_iteracoes = 1000000

        # Definições Adicionais
        self.vertices = [i for i in range(self.N)]
        self.melhor_solucao = None
        self.melhor_distancia = float("Inf")
        self.lista_distancias = []
        self.lista_todas_distancias = []

    # Distância Entre Dois Pontos (Distância Euclidiana)
    def dist(self, ponto_0, ponto_1):
        coord_0, coord_1 = self.coords[ponto_0], self.coords[ponto_1]
        # Equação: sqrt( (q1 - p1)^2 + (q2 - p2)^2 )
        return math.sqrt((coord_0[0] - coord_1[0]) ** 2 + (coord_0[1] - coord_1[1]) ** 2)

    # Verifica/Retorna Distância Total da Solução/Caminho Atual
    def distancia_solucao(self, solucao):
        dist = 0
        for i in range(self.N):
            dist += self.dist(solucao[i % self.N], solucao[(i + 1) % self.N])
        return dist

    # Probabilidade: (p) = Exp(X’- X / T)
    def probabilidade_aceitacao(self, distancia_candidato):
        return math.exp(-abs(distancia_candidato - self.distancia_atual) / self.T)

    # Função que Verifica se o Candidato Será Aceito
    def aceita_candidato(self, candidato):
        distancia_candidato = self.distancia_solucao(candidato)
        # Adiciona na Lista com Todas as Soluções Avaliadas
        self.lista_todas_distancias.append(distancia_candidato)
        # Aceita o Candidato se Ele for Melhor que o Melhor Atual
        if distancia_candidato < self.distancia_atual:
            self.distancia_atual, self.solucao_atual = distancia_candidato, candidato
            if distancia_candidato < self.melhor_distancia:
                self.melhor_distancia, self.melhor_solucao = distancia_candidato, candidato
        # Chama a Função Probabilistica se Ele for Pior que o Melhor Atual
        else:
            if random.random() < self.probabilidade_aceitacao(distancia_candidato):
                self.distancia_atual, self.solucao_atual = distancia_candidato, candidato

    # Define a Solução Inicial Através do Algoritmo de Vizinho Mais Próximo
    def solucao_inicial(self):
        # Iniciando de um Ponto Aleatório
        vertice_att = random.choice(self.vertices)
        solucao_att = [vertice_att]
        # Inicia a Partir do Ponto Aleatório Escolhido
        vertices_livres = set(self.vertices)
        vertices_livres.remove(vertice_att)
        while vertices_livres:
            # Encontra o Vizinho Mais Próximo
            prox_v = min(vertices_livres, key=lambda x: self.dist(vertice_att, x))
            # Remove da Lista de Vertices Não Usados e Insere na Solução
            vertices_livres.remove(prox_v)
            solucao_att.append(prox_v)
            vertice_att = prox_v

        distancia_att = self.distancia_solucao(solucao_att)
        # Se for a Melhor Solução, Então Atualiza a Melhor Solução
        if distancia_att < self.melhor_distancia:
            self.melhor_distancia = distancia_att
            self.melhor_solucao = solucao_att

        self.lista_distancias.append(distancia_att)
        # Adiciona na Lista com Todas as Soluções Avaliadas
        self.lista_todas_distancias.append(distancia_att)
        return solucao_att, distancia_att

    # Função de Execução do Recozimento Simulado
    def recozimento_simulado(self):
        # Inicializa a Função com a Solução Inicial
        self.solucao_atual, self.distancia_atual = self.solucao_inicial()
        print("Distancia Inicial: ", self.distancia_atual)
        # Para ver o Caminho da Solução Inicial
        self.apresenta_melhor_rota()
        print("------------------------")
        print("Aplicando Recozimento...")
        print("------------------------")

        # Enquanto os Critérios de Parada Não Forem Alcançados
        while self.T >= self.temperatura_de_parada and self.iteracao < self.max_iteracoes:
            # Define um Novo Candidato
            candidato = list(self.solucao_atual)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidato[i: (i + l)] = reversed(candidato[i: (i + l)])
            # Chama a Função Para Verificar se o Candidato Deve ser Aceito
            self.aceita_candidato(candidato)
            # Aplica a Taxa de Resfriamento
            # print("Temperatura: ", self.T)
            self.T *= self.taxa_resfriamento
            self.iteracao += 1
            # Adiciona na Lista de Resultados
            self.lista_distancias.append(self.distancia_atual)

        #Faz a Apresentação dos Resultados
        print("Melhor Distancia Obtida: ", self.melhor_distancia)
        # print("Melhor Rota: ", self.melhor_solucao)
        self.apresenta_melhoria_porcentagem()

    # Apresenta a Melhor Rota do Caixeiro
    def apresenta_melhor_rota(self):
        tsp_view.rota_caixeiro_viajante([self.melhor_solucao], self.coords)

    # Apresenta as Melhorias na Solução Durante as Iterações
    def apresenta_melhorias(self):
        plt.plot([i for i in range(len(self.lista_distancias))],
                 self.lista_distancias)
        plt.ylabel("Valor")
        plt.xlabel("Iteração")
        plt.show()

    # Apresenta Todas as Soluções Avaliadas
    def apresenta_todas_solucoes(self):
        plt.plot([i for i in range(len(self.lista_todas_distancias))],
                 self.lista_todas_distancias)
        plt.ylabel("Valor")
        plt.xlabel("Iteração")
        plt.show()

    # Aresenta a Melhoria Percentual em Relação a Solução Inicial
    def apresenta_melhoria_porcentagem(self):
        melhoria = 100 * \
            (self.lista_distancias[0] - self.melhor_distancia) / \
            (self.lista_distancias[0])
        print(f"Melhoria em Relação a Solução Inicial: {melhoria : .2f}%")
