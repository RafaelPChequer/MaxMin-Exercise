import os
import networkx as nx
import matplotlib.pyplot as plt


def maxmin_select(arr, low, high, G=None, parent=None, level=0):
    """
    Algoritmo recursivo para encontrar o maior e o menor elementos em uma sequência.
    Gera um diagrama da árvore de recursão com networkx.
    """
    if G is None:
        G = nx.DiGraph()

    # Nome do nó com underscores
    node_name = f"{level}_{low}_{high}"
    # Rótulo detalhado com os elementos do array
    node_label = f"Level {level}\\n[{low}-{high}]\\n{arr[low:high+1]}"
    G.add_node(node_name, label=node_label)
    if parent is not None:
        G.add_edge(parent, node_name)

    # Caso base: apenas um elemento
    if low == high:
        return arr[low], arr[low], G

    # Caso base: dois elementos
    if high == low + 1:
        comparisons = 1
        if arr[low] < arr[high]:
            min_val, max_val = arr[low], arr[high]
        else:
            min_val, max_val = arr[high], arr[low]
        combine_name = f"combine_{level}_{low}_{high}"
        G.add_node(combine_name, label=f"min={min_val} max={max_val}\\nComp={comparisons}")
        G.add_edge(node_name, combine_name)
        return min_val, max_val, G

    # Divisão e conquista
    mid = (low + high) // 2
    min1, max1, G = maxmin_select(arr, low, mid, G, node_name, level + 1)
    min2, max2, G = maxmin_select(arr, mid + 1, high, G, node_name, level + 1)

    # Combinação dos resultados
    minimum = min(min1, min2)
    maximum = max(max1, max2)
    comparisons = 2

    combine_name = f"combine_{level}_{low}_{high}"
    G.add_node(combine_name, label=f"min={minimum} max={maximum}\\nComp={comparisons}")
    G.add_edge(node_name, combine_name)

    return minimum, maximum, G


def generate_puml(G, filename):
    """
    Gera um arquivo .puml baseado no grafo networkx com rótulos mais compreensivos.
    """
    with open(filename, 'w') as f:
        f.write("@startuml\n")
        f.write("skinparam monochrome true\n")
        f.write("skinparam nodesep 50\n")  # Aumenta a separação entre nós
        f.write("skinparam ranksep 50\n")  # Aumenta a separação entre níveis
        for node, data in G.nodes(data=True):
            label = data['label'].replace('\n', '\\n')
            f.write(f"{node} : \"{label}\"\n")
        for edge in G.edges():
            f.write(f"{edge[0]} --> {edge[1]}\n")
        f.write("@enduml\n")
    print(f"Diagrama PlantUML salvo em '{filename}'")


def main():
    # Array com 8 elementos
    arr = [23, 12, 45, 9, 78, 3, 56, 27]
    n = len(arr)

    # Chama o algoritmo e obtém o grafo
    minimum, maximum, G = maxmin_select(arr, 0, n - 1)

    # Exibe os resultados
    print(f"Sequência: {arr}")
    print(f"Menor elemento: {minimum}")
    print(f"Maior elemento: {maximum}")

    # Cria a pasta 'assets' se não existir
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Gera e salva o diagrama PNG
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Ajusta o layout para melhor separação
    labels = nx.get_node_attributes(G, 'label')
    plt.figure(figsize=(14, 10))  # Aumenta o tamanho da figura
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue',
            node_size=5000, font_size=10, arrows=True, edge_color='gray',
            font_weight='bold')
    plt.title("Árvore de Recursão do Algoritmo MaxMin Select", fontsize=14, pad=20)
    plt.savefig('assets/diagrama_maxmin.png', format='png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Diagrama PNG salvo em 'assets/diagrama_maxmin.png'")

    # Gera e salva o diagrama PlantUML
    generate_puml(G, 'assets/diagrama_maxmin.puml')


if __name__ == "__main__":
    main()