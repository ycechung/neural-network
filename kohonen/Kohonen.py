import random
import math

class Kohonen(object):
    def __init__(self, width=3, height=3, outputs=4):
        #TODO: dodac bias!
        #TODO: ewentualnie ustawianie alfa
        self.alfa = 0.06
        #TODO: dodac ustawianie promienia sasiedztwa
        self.r = 1
        self.width = width
        self.height = height
        self.outputs = outputs
        self.freq = [1.0/self.outputs for i in range(self.outputs)]
        self.beta = 0.1

    def initialize(self):
        random.seed()
        self.weights = [[[random.random() for i in range(self.width)] for j in range(self.height)] for k in range(self.outputs)]
        self.print_network()

    #obliczanie odleglosci
    #na razie tylko dla 1D
    def G(self, win, k):
        #return math.exp(-(win-k)**2/(2*(self.r)**2))
        if abs(win-k) < self.r:
            return 1.0
        return 0.0

    def update_weights(self, pict, win):
        for k in range(self.outputs):
            for j in range(self.height):
                for i in range(self.width):
                    #print self.G(win,k)
                    self.weights[k][j][i] += self.alfa*self.G(win, k)*(pict[j][i]-self.weights[k][j][i])

    def adjust_dist(self, dist, k):
        bias = self.outputs * self.freq[k] - 1
        return dist + bias

    def update_freqs(self, win):
        for k in range(self.outputs):
            if k == win:
                self.freq[k] += self.beta*(1.0 - self.freq[k])
            else:
                self.freq[k] += self.beta*(0.0 - self.freq[k])

    def winner(self, pict):
        min_dist = float('infinity')
        min_dist_ind = -1
        for k, w in enumerate(self.weights):
            s = 0.0
            for j in range(self.height):
                for i in range(self.width):
                    s += (w[j][i] - pict[j][i])**2
            dist = math.sqrt(s)
            adj_dist = self.adjust_dist(dist, k)
            if adj_dist < min_dist:
                min_dist = adj_dist
                min_dist_ind = k
        return min_dist_ind

    #TODO: czy liczba epok nie powinna byc konfigurowalna?
    #TODO: czy przedzialy w ktorych alfa jest stale nie powinny byc konfigurowalne?
    def learn(self, X, epochs=32000):
        for i in range(4):
            print 'alfa =', self.alfa
            print 'r =', self.r
            for e in range(epochs/4):
                for pict in X:
                    win = self.winner(pict)
                    self.update_freqs(win)
                    self.update_weights(pict, win)
            self.alfa /= 2
            #self.r -= 2
        self.print_network()

    def print_network(self):
        for k in range(self.outputs):
            print
            for j in range(self.height):
                wagi = ''
                for i in range(self.width):
                    wagi += str(self.weights[k][j][i]) + ' '
                print wagi
                print
