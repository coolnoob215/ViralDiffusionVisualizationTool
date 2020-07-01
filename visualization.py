import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import math
import xlrd
from simulation import do_timestep


def show():
    plt.show()


def get_circle_size(num_nodes):
    if num_nodes < 10:
        return 1
    return 1 / (num_nodes / 7)


def get_circle_x(num_nodes, cur_node):
    if num_nodes == 1:
        return 5
    if num_nodes <= 20:
        return 5 + (2.5 * math.cos((360 / num_nodes) * cur_node * (math.pi / 180)))
    return 5 + (2 + num_nodes / 40) * math.cos((360 / num_nodes) * cur_node * (math.pi / 180))


def get_circle_y(num_nodes, cur_node):
    if num_nodes == 1:
        return 5
    if num_nodes <= 20:
        return 5 + (2.5 * math.sin((360 / num_nodes) * cur_node * (math.pi / 180)))
    return 5 + (2 + num_nodes / 40) * math.sin((360 / num_nodes) * cur_node * (math.pi / 180))


def get_circle_xy(num_nodes, cur_node):
    return get_circle_x(num_nodes, cur_node), get_circle_y(num_nodes, cur_node)


class SliderProcessor(object):
    def __init__(self, node, axes, label, min_val, max_val, init_val, figure):
        self.node = node
        self.figure = figure
        self.circle = self.figure.circles[node]
        self.slider = Slider(axes, label, min_val, max_val, valinit=init_val)
        self.slider.on_changed(self.process)

    def process(self, val):
        self.circle.set_alpha(val)


class ButtonProcessor(object):
    def __init__(self, axes, label, figure):
        self.figure = figure
        self.button = Button(axes, label)
        self.first_click = True
        self.button.on_clicked(self.process)

    def process(self, event):
        if self.first_click:
            new_probabilities = [0] * self.figure.num_nodes
            for node in range(self.figure.num_nodes):
                new_probabilities[node] = self.figure.sliders[node].slider.val
                self.figure.sliders[node].slider.ax.remove()
            self.figure.update_probabilities(new_probabilities)
            self.figure.fig.subplots_adjust(left=0.25, bottom=0.2)
            self.first_click = False

        transmission_rates = self.get_transmission_rates()

        next_probabilities = do_timestep(self.figure.probabilities, transmission_rates, self.figure.num_nodes)
        self.figure.update_probabilities(next_probabilities)
        for node in range(self.figure.num_nodes):
            self.figure.circles[node].set_alpha(next_probabilities[node])

    def get_transmission_rates(self):
        transmission_rates = []

        wb = xlrd.open_workbook('Transmission Rate Inputs.xls')
        sheet = wb.sheet_by_name("Transmission Rate Inputs")

        for node in range(self.figure.num_nodes):
            node_transmission_rates = sheet.row_values(node + 1)[1:]
            transmission_rates.append(node_transmission_rates)

        return transmission_rates


class Figure(object):
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, aspect='equal')

        plt.xlim(0, 10)
        plt.ylim(0, 10)

        self.fig.subplots_adjust(left=0.25, bottom=(0.25 + 0.05*num_nodes))

        self.circles = [None] * num_nodes
        self.sliders = [None] * num_nodes

        self.probabilities = [1.0] * num_nodes

        for cur_node in range(num_nodes):
            circle = plt.Circle(get_circle_xy(num_nodes, cur_node), get_circle_size(num_nodes), color='r')
            self.ax.add_artist(circle)
            self.circles[cur_node] = circle

            slider_axes = plt.axes([0.25, 0.05 * (num_nodes + 2 - cur_node), 0.65, 0.03])
            slider = SliderProcessor(cur_node, slider_axes, "Infection Probability {}".format(cur_node),
                                     0.0, 1.0, 1.0, self)
            self.sliders[cur_node] = slider

        button_axes = plt.axes([0.5, 0.05, 0.1, 0.075])
        self.button = ButtonProcessor(button_axes, "Timestep", self)

    def update_probabilities(self, probabilities):
        self.probabilities = probabilities
