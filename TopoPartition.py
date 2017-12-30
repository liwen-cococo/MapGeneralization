import math
from helper import getBoundingBox, getCPNumInBox

class TopologyPartition(object):
    def __init__(self, lines, cps, sc1, sc2):
        self.lines = lines
        self.cps = cps
        self.sc1 = sc1
        self.sc2 = sc2

    def simplify(self):
        results = {}
        for k in self.lines:
            if k in self.sc1:
                # the first point after starting point will never be removed
                results[k] = self.simplifySingleLine(self.lines[k], 1)
            elif k in self.sc2:
                results[k] = self.simplifySingleLine(self.lines[k], 2)
            else:
                results[k] = self.simplifySingleLine(self.lines[k], 0)
        
        return results

    def simplifySingleLine(self, points, flag):
        results = []
        if flag == 0: # it is a common line
            (x_min, x_max, y_min, y_max) = getBoundingBox(points)
            (cp_num, inside_cps) = getCPNumInBox(self.cps, x_min, x_max, y_min, y_max)
            if cp_num == 0:
                return [points[0], points[-1]]

            #Else: there are some constraint points
            p_num = points.__len__()
            MBR = int(math.ceil((p_num+0.0)/(cp_num+1)))

            for i in xrange(cp_num+1):
                final_index = min((i+1)*MBR, p_num)
                temp = points[i*MBR:final_index]

                if temp.__len__() >= 2:
                    (temp_x_min, temp_x_max, temp_y_min, temp_y_max) = getBoundingBox(temp)
                    (temp_cp_num, temp_inside_cps) = getCPNumInBox(inside_cps, temp_x_min, temp_x_max, temp_y_min, temp_y_max)
                    if temp_cp_num == 0:
                        results.extend([temp[0], temp[-1]])
                    else:
                        temp_result = self.constraintRecognition(temp, temp_inside_cps)
                        results.extend(temp_result)
                else:
                    results.extend(temp)
                    break
            try:
                assert results[-1] == points[-1]
            except AssertionError:
                results.append(points[-1])
                    
            return results

        elif flag== 1: # special case:cannot remove first points
            results = [points[0]]
            results.extend(self.simplifySingleLine(points[1:], 0))
        else:
            assert flag == 2
            results = [points[0], points[1]]
            results.extend(self.simplifySingleLine(points[2:], 0))
        
        return results

    def constraintRecognition(self, points, cps):
        results = [points[0]]
        p_len = points.__len__()
        for i in xrange(1, p_len-1):
            triangle = [points[i-1], points[i], points[i+1]]
            (x1, x2, y1, y2) = getBoundingBox(triangle)
            (x, _) = getCPNumInBox(cps, x1, x2, y1, y2)
            if x > 0: # as long as cp is in the rectangle.
                results.append(points[i])
            # else: remove this point
        return results
