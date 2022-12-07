from collections import defaultdict
import csv
import sys

class Graph:

    def __init__(self, vertices) -> None:
        self.e = vertices #no of vertices
        self.graph = [] #blank list to add adjacency list to
        self.edges = {} #blank dictionary to add components to
        self.mst = []
        

    def add_edge(self, n1, n2, weight) -> None:
        self.graph.append([n1,n2,weight]) #Adds start, finish and weight to the graph dictionary 

    #Finds the set (start, finish and weight) of the edge
    def search_edges(self, edge):
        if self.edges[int(edge)] == int(edge): #checks if the edge is the same as a key in the edge dictionary
            return edge
        return self.search_edges(self.edges[edge])

    #Sets the edge
    def set_edges(self, edge) -> None:
        
        if self.edges[edge] == edge: #checks if the edge is the same as a key in the edge dictionary 
            return
        else:
            for i in self.edges.keys(): #iterates through a list of edge keys
                self.edges[i] = self.search_edges(i) #adds each edge to the dictionary in the correct order 



    #Joins components together
    def join(self, total_edges, edge1, edge2):
        if total_edges[edge1] <= total_edges[edge2]:
            self.edges[edge1] = edge2
            total_edges[edge2] = total_edges[edge1]
        
        elif total_edges[edge1] >= total_edges[edge2]:
            self.edges[edge2] = self.search_edges(edge1)
            total_edges[edge1] += total_edges[edge2]
        

    def boruvka(self):
        component_size = []
        cheapest_edge = []
        min_span_tree_weight = 0
        

        cheapest_edge = [-1] * self.e #creates a list of -1 the length of the number of verticies

        # Initialises all the components as singular vertexs
        for vertex in range(self.e):
            self.edges.update({vertex : vertex}) 
            component_size.append(1) # adds the component size of 1 for each vertex in the graph

        #sets the number of components to the number vertices
        no_components = self.e
        #while loop to iterate through the process until only 1 component (the minimum spanning tree) remains
        while no_components > 1:
            for i in range(len(self.graph)):
                #each edge in G is tested against the others to find the smallest connecting edge for each component

                start = int(self.graph[i][0]) # start 
                end = int(self.graph[i][1]) # end
                weight = int(self.graph[i][2]) # weight

                self.set_edges(start)
                self.set_edges(end)

                start_edge = self.edges[start]
                end_edge = self.edges[end]

                #if the edge connects 2 components
                if start_edge != end_edge :
                    #if the component hasnt been connected or the current connection has a larger weight replace
                    #connecting vertex with the new component for both the start and the finish vertices
                    if cheapest_edge[start_edge] == -1 or cheapest_edge[start_edge][2] > weight:
                        cheapest_edge[start_edge] = [start,end,weight]
                    if cheapest_edge[end_edge] == -1 or cheapest_edge[end_edge][2] > weight:
                        cheapest_edge[end_edge] = [start,end,weight]

            #if a edge has been found between vertices    
            for vertex in range(self.e):
                if cheapest_edge[vertex] != -1:
                    start = cheapest_edge[vertex][0]
                    end = cheapest_edge[vertex][1]
                    weight = cheapest_edge[vertex][2]

                    self.set_edges(start)
                    self.set_edges(end)
                    
                    start_edge = self.edges[start]
                    end_edge = self.edges[end]

                    #merge the 2 components together
                    if start_edge != end_edge:
                        #adds the edge weight to the minimum spanning tree
                        min_span_tree_weight += weight
                        self.join(component_size, start_edge, end_edge)
                        self.mst.append([str(start), str(end)])
                        print ("Edge " + str(start) + " - " + str(end) + " with weight " + str(weight) + " is included in the Minimum Spanning Tree.")

                        #reduce the number of components by 1
                        no_components -= 1

            cheapest_edge = [-1] * self.e
                      
        print("The weight of Minimum Spanning Tree is " + str(min_span_tree_weight))  

    #Visually plots the graph and minimum spanning tree
    def plotMST(self):
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
        except:
            print ("Required libraries are not installed to plot graphs.")
            sys.exit()

        plt.clf()
        G = nx.Graph()

        edges_all = []
        for e in range(len(self.graph)):
            G.add_node(self.graph[e][0])
            
            G.add_node(self.graph[e][1])
            
            G.add_edge(self.graph[e][0], self.graph[e][1], weight = self.graph[e][2])
            edges_all.append((self.graph[e][0], self.graph[e][1]))
           

        edges_route = []
        for e in range(len(self.mst)):
            
            edges_route.append((self.mst[e][0], self.mst[e][1]))
            

        pos = nx.spring_layout(G, k=4)
        edge_labels = dict([((u, v), d['weight']) for u,v,d in G.edges(data=True)])
        nx.draw_networkx_nodes(G, pos=nx.circular_layout(G), node_size=300)
        nx.draw_networkx_edges(G, pos=nx.circular_layout(G), edgelist=edges_all, width=2, alpha=0.5, style='dashed')
        nx.draw_networkx_edges(G, pos=nx.circular_layout(G), edgelist=edges_route, width=3, edge_color='b')
        nx.draw_networkx_labels(G, pos=nx.circular_layout(G), font_size=10, font_family='sans-serif')
        nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=edge_labels)

        plt.axis('off')
        plt.show()


#Adds the graph into the graph class from the csv file 
def get_graph(filename, graph):
        size = 0 
        with open(filename) as csvfile:
            edgereader = csv.reader(csvfile)
            for r in edgereader:
                graph.add_edge(r[0], r[1], r[2])
        return graph  

#Adds the number of verticies to the graph class from the csv file 
def get_size(filename):
        size = 0 
        with open(filename) as csvfile:
            edgereader = csv.reader(csvfile)
            for r in edgereader:
                if int(r[0]) > size and int(r[0]) > int(r[1]):
                     size = int(r[0])
                elif int(r[1]) > size and int(r[1]) > int(r[0]):
                    size = int(r[1])
                else:
                    size = size
            size = size + 1
        return size 

def main():

    try:
        print( "Welcome to the boruvka minumum spanning tree app. \nYou wiil be asked to input a file name and the number of nodes the file contains." 
        + "The program will return a list of the nodes in the minimum spanning tree, the total weight of the minimum spanning tree "
         + "and a graphical representation. \nNodes should be numbered from 0 upwards. \nTo end the program close the graphical figure."  )
        filename = input("Enter csv file e.g. 'example.csv' :")
        

    except:
       print ("\nNo input file specified.")
       sys.exit()
    gr = get_size(filename)
    graph = Graph(gr)
    g = get_graph(filename, graph)
    g.boruvka()
    g.plotMST()


if __name__=="__main__":
    main()

        


