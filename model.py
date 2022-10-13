from automata.fa.dfa import DFA
import igraph as ig
import matplotlib.pyplot as plt


class AppAutomata:

    automata_kleene = DFA(
        states={'q0', 'q1', 'q2', 'q3'},
        input_symbols={'a', 'b', 'c', 'd'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q1', 'c': 'q2', 'd': 'q3'},
            'q1': {'a': 'q1', 'b': 'q1', 'c': 'q2', 'd': 'q3'},
            'q2': {'c': 'q2', 'd': 'q3'}
        },
        initial_state='q0',
        final_states={'q3'},
        allow_partial=True
    )

    automata_a_la_5 = DFA(
        states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11'},
        input_symbols={'a', 'b', 'c', 'd'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q1', 'c': 'q6', 'd': 'q11'},
            'q1': {'a': 'q2', 'b': 'q2', 'c': 'q6', 'd': 'q11'},
            'q2': {'a': 'q3', 'b': 'q3', 'c': 'q6', 'd': 'q11'},
            'q3': {'a': 'q4', 'b': 'q4', 'c': 'q6', 'd': 'q11'},
            'q4': {'a': 'q5', 'b': 'q5', 'c': 'q6', 'd': 'q11'},
            'q5': {'c': 'q6', 'd': 'q11'},
            'q6': {'c': 'q7', 'd': 'q11'},
            'q7': {'c': 'q8', 'd': 'q11'},
            'q8': {'c': 'q9', 'd': 'q11'},
            'q9': {'c': 'q10', 'd': 'q11'},
            'q10': {'d': 'q11'}
        },
        initial_state='q0',
        final_states={'q11'},
        allow_partial=True
    )

    graph_kleene = ig.Graph(
        4,
        [(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3)],
        directed = True
    )
    graph_kleene["title"] = "Automata Clausura de Kleene"
    graph_kleene.vs["name"] = ["q0", "q1", "q2", "q3"]

    graph_a_la_5 = ig.Graph(
        12,
        [(0, 1), (0, 6), (0, 11),
         (1, 2), (1, 6), (1, 11),
         (2, 3), (2, 6), (2, 11),
         (3, 4), (3, 6), (3, 11),
         (4, 5), (4, 6), (4, 11),
         (5, 6), (5, 6), (5, 11),
         (6, 7),(6, 11),
         (7, 8),(7, 11),
         (8, 9),(8, 11),
         (9, 10),(9, 11),
         (10, 11)],
        directed = True
    )
    graph_a_la_5["title"] = "Automata Clausura de Kleene"
    graph_a_la_5.vs["name"] = ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11"]

    def __init__(self):

        self.language = 'es'
        self.active_automata = self.automata_kleene
        self.active_graph = self.graph_kleene
        self.active_automata_tag = 'automata_kleene'
        self.speed = 'normal'
        self.fig, self.ax = plt.subplots(figsize=(9, 7))

    def reset_graph(self):
        graph = self.active_graph
        plt.cla()
        ig.plot(
            graph,
            target=self.ax,
            layout="circle",
            vertex_size=0.4,
            vertex_color=["steelblue" if name == "q0" else "light blue" for name in graph.vs["name"]],
            vertex_frame_width=[5.0 if name in self.active_automata.final_states else 1.0 for name in graph.vs["name"]],
            vertex_frame_color="black",
            vertex_label=graph.vs["name"],
            vertex_label_size=20.0
        )

        self.fig.savefig('./img/graph.png')

    def update_graph(self, last):
        graph = self.active_graph
        plt.cla()
        ig.plot(
            graph,
            target=self.ax,
            layout="circle",
            vertex_size=0.4,
            vertex_color=["green" if name == last else "steelblue" if name == 'q0' else "light blue" for name in graph.vs["name"]],
            vertex_frame_width=[5.0 if name in self.active_automata.final_states else 1.0 for name in graph.vs["name"]],
            vertex_frame_color="black",
            vertex_label=graph.vs["name"],
            vertex_label_size=20.0
        )

        self.fig.savefig('./img/graph.png')

    def update_graph_error(self, last):
        graph = self.active_graph
        plt.cla()
        ig.plot(
            graph,
            target=self.ax,
            layout="circle",
            vertex_size=0.4,
            vertex_color=["red" if name == last else "steelblue" if name == 'q0' else "light blue" for name in graph.vs["name"]],
            vertex_frame_width=[5.0 if name in self.active_automata.final_states else 1.0 for name in graph.vs["name"]],
            vertex_frame_color="black",
            vertex_label=graph.vs["name"],
            vertex_label_size=20.0
        )

        self.fig.savefig('./img/graph.png')

    def validate_word(self, word):
        result = self.active_automata.read_input_stepwise(word)
        return result



