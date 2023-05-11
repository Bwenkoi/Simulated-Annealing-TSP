
# Breno de Oliveira Renó - brenooliveirareno@unifei.edu.br
# Aplicação do Recozimento Simulado no Problema do Caixeiro Viajante
# -------------------------------------------------------------------
# FONTE: Construído com base no código de Chncyhn
# Disponível em: https://github.com/chncyhn/simulated-annealing-tsp
# -------------------------------------------------------------------
# Observação:
# Usar as Bases no Formato que Estão no Projeto (Apenas Coordenadas)
# -------------------------------------------------------------------

from SimulatedAnneling import RecozimentoSimulado

# Abre e formata os dados vindos do arquivo indicado
def abre_arquivo_coordenadas(arquivo):
    coordenadas = []
    with open(arquivo, "r") as f:
        for linha in f.readlines():
            linha = [float(x.replace("\n", "")) for x in linha.split(" ")]
            coordenadas.append(linha)
    return coordenadas


# Inicio do Código
coordenadas = abre_arquivo_coordenadas("berlin52.txt")

# Inicializa a Classe
rs_classe = RecozimentoSimulado(coordenadas)

# Executa as Funções
rs_classe.recozimento_simulado()
# Para ver a Rota Final
rs_classe.apresenta_melhor_rota()
# Para ver Todas as Soluções Avaliadas
rs_classe.apresenta_todas_solucoes()
# Para ver as Melhorias
rs_classe.apresenta_melhorias()
