import networkx as nx
import matplotlib.pyplot as plt 
import pickle as pkl


class DrawMap(object):
    def __init__(self, line_path='./source/lines_out.txt', cp_path='./source/points_out.txt'):
        """
        line_path: lines.out.txt
        cp_path: constraint points points_out.txt
        """
        self.lp = line_path
        self.cpp = cp_path

    def drawSingleLine(self, points_pos):
        G = nx.Graph()
        len = points_pos.__len__()
        for i in xrange(len):
            G.add_node(i)
        for i in xrange(len-1):
            G.add_edge(i, i+1)
        nx.draw(G, points_pos, node_size=0.2)

    def drawLines(self):
        lines = {}
        with open(self.lp) as f:
            lines_info = f.readlines()
            for li in lines_info:
                t1 = li.split('>')
                line_id = t1[0].split(':')[0]
                d_str = t1[2].split('<')[0][:-1]
                x_y = d_str.split(' ')
                coordinates = []
                for xy in x_y:
                    temp = xy.split(',')
                    coordinates.append((float(temp[0]), float(temp[1])))
                lines[line_id] = coordinates
        
        for k in lines:
            self.drawSingleLine(lines[k])
        
        return lines # dict: key(line id) value(a series of coordinates of points)
        
    def drawCP(self):
        G = nx.Graph()
        pos = []
        with open(self.cpp) as f:
            lines = f.readlines()
            for line in lines:
                x1 = line.split('>')[2].split('<')[0][:-1]
                d = x1.split(',')
                pos.append((float(d[0]), float(d[1])))
        for i in xrange(pos.__len__()):
            G.add_node(i)
        nx.draw(G, pos, node_size=1, node_color='black')

        # position of all constraint points
        return pos

    def draw(self, pic_name):
        lines = self.drawLines()
        cps = self.drawCP()

        plt.gca().set_aspect(1)
        plt.savefig(pic_name)
        #plt.show()

        return (lines, cps)


if __name__ == '__main__':
    dm = DrawMap('./source/lines_out.txt', './source/points_out.txt')
    (lines, cps) = dm.draw('./result/complex.png')
    """
    lines # dict: key(line id) value(a series of coordinates of points)
    cps   # list: coordinates of all constraint points
    """
    with open('graph.pkl', 'w') as f:
        pkl.dump((lines, cps), f)
