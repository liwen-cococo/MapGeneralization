import pickle as pkl
import matplotlib.pyplot as plt 
from TopoPartition import TopologyPartition
from helper import checkSC1, checkSC2, GenLinesSimpleOutTxt
from draw import DrawMap


if __name__ == '__main__':
    # draw complex map and get map info --------------------------------------------
    dp_complex = DrawMap(line_path='./source/lines_out.txt', cp_path='./source/points_out.txt')
    (lines, cps) = dp_complex.draw('./result/complex.png')
    sc1, sc2 = checkSC1(lines), checkSC2(lines)

    # run simplifying algorithm to get simplified map -----------------------------
    tp = TopologyPartition(lines, cps, sc1, sc2)
    results = tp.simplify()

    # draw simplified map ---------------------------------------------------------
    plt.clf()
    dm = DrawMap()
    for k in results:
        dm.drawSingleLine(results[k])
    dm.drawCP()
    plt.gca().set_aspect(1)
    plt.savefig('./result/simple.png')
    #plt.show()

    # generate lines_simple_out.txt -----------------------------------------------
    GenLinesSimpleOutTxt(results, file_name='./result/lines_simple_out.txt')

    print 'successfully done'
