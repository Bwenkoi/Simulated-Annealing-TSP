import matplotlib.pyplot as plt


def rota_caixeiro_viajante(arestas, vertices):
    # arestas: Lista com a Ordem dos Locais Vizitados
    # vertices: Coordenadas de Cada Local

    # Transforma o Caminho Para o Formato Usado no Gráfico
    x = []
    y = []
    for i in arestas[0]:
        x.append(vertices[i][0])
        y.append(vertices[i][1])

    plt.plot(x, y, 'co')

    # Define o Tamanho das Setas no Gráfico
    tamanho_seta = float(max(x))/float(80)

    # Desenha o Caminho do Caixeiro Viajante
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=tamanho_seta,
              color='g', length_includes_head=True)
    for i in range(0, len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width=tamanho_seta,
                  color='g', length_includes_head=True)

    # Formatação dos Eixos
    plt.xlim(min(x), max(x)*1.1)
    plt.ylim(min(y), max(y)*1.1)
    plt.show()
