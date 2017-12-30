import pickle as pkl
import matplotlib.pyplot as plt 
from TopoPartition import TopologyPartition
from helper import checkSC1, checkSC2
from draw import DrawMap


if __name__ == '__main__':
    lines, cps = {}, []
    sc1, sc2 = [], []
    with open('graph.pkl') as f:
        (lines, cps) = pkl.load(f)
        sc1 = checkSC1(lines)
        sc2 = checkSC2(lines)
    
    tp = TopologyPartition(lines, cps, sc1, sc2)
    results = tp.simplify()
    print 'simplify done'

    l_len = 0
    for k in lines:
        l_len += 1
    print 'lines number =', l_len

    # draw
    cou = 0
    results_len = 0
    dm = DrawMap()
    for k in results:
        results_len += 1
        dm.drawSingleLine(results[k])
        if results[k].__len__ < 2:
            print '------------line id =', k
        cou += results[k].__len__()
    print 'results_len =', results_len
    dm.drawCP()
    plt.gca().set_aspect(1)
    plt.savefig('./result/simple.png')
    plt.show()

    print cou
    print 'all done'
