import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def get_graph():

    # Open the file
    with open('Graph1.txt', 'r') as f:
        # Read the first line to get the number of nodes
        N = int(f.readline().strip())
        
        # Create an empty adjacency matrix
        adj_matrix = np.full((N, N), np.inf)
        
        # Read the remaining lines
        for i in range(N):
            line = f.readline().strip()
            # Split the line into costs and convert them to float
            costs = [float(cost) if cost != 'INF' else 1e5 for cost in line.split()]
            # Fill the adjacency matrix
            adj_matrix[i] = costs

    return adj_matrix


def draw_graph():
    adj_matrix = get_graph()
    G = nx.from_numpy_array(np.array(adj_matrix))
    # print(G)

    # # Create a layout for the nodes
    # layout = nx.spring_layout(G)

    # # Draw the nodes
    # nx.draw_networkx_nodes(G, layout)

    # # Draw the edges
    # for u,v,d in G.edges(data=True):
    #     if d['weight'] != np.inf:
    #         nx.draw_networkx_edges(G, layout, edgelist=[(u, v)])

    # # Draw the labels
    # nx.draw_networkx_labels(G, layout)

    # # Display the plot
    # plt.show()

    # Determine NUM_LAYERS
    NUM_LAYERS = 4  # adjust as needed

    # Generate a 3D position layout
    layout = {}
    for node in G.nodes():
        # Determine the layer and position within the layer
        layer = node // NUM_LAYERS
        pos_in_layer = node % NUM_LAYERS
        # Generate a 2D layout for the layer
        submatrix = adj_matrix[layer*NUM_LAYERS:(layer+1)*NUM_LAYERS, layer*NUM_LAYERS:(layer+1)*NUM_LAYERS]
        layout_2d = nx.spring_layout(nx.from_numpy_array(np.array(submatrix)))
        # Assign the 3D position
        x, y = layout_2d[pos_in_layer]
        layout[node] = (x, y, layer)

    # Create 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw the nodes
    for node, (x, y, z) in layout.items():
        ax.scatter(x, y, z)

    # Draw the edges
    for u, v, d in G.edges(data=True):
        if np.isfinite(d['weight']):
            x1, y1, z1 = layout[u]
            x2, y2, z2 = layout[v]
            ax.plot([x1, x2], [y1, y2], [z1, z2], color='blue')  # customize color as needed

    plt.show()

   

if __name__ == "__main__":
    draw_graph()