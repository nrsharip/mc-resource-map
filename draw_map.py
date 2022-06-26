import multiprocessing                      
import math
import numpy as np
import re
import sys
# https://stackoverflow.com/questions/12236566/setting-different-color-for-each-series-in-scatter-plot-on-matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def distance(x1, y1, x2, y2):
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# see pool.starmap below
def iterate_over_x_y_range(xr1, xr2, yr1, yr2, radius, array_of_dots):
  max_in_circle = 0
  current = 0

  dots_dict = {}
  
  for x1 in range(xr1, xr2):
    for y1 in range(yr1, yr2):

      dots_in = set()

      for (x2,y2,z2) in array_of_dots:
        if abs(x2-x1) > radius or abs(z2-y1) > radius:
          continue
        if distance(x1, y1, x2, z2) < radius:
          current += 1
          dots_in.add((x2,y2,z2))

      # https://stackoverflow.com/questions/28566797/is-it-safe-to-use-frozen-set-as-dict-key/28566901
      if current == max_in_circle:
        if frozenset(dots_in) in dots_dict:
          dots_dict.get(frozenset(dots_in)).append([x1, y1])
        else:
          dots_dict[frozenset(dots_in)]=[[x1, y1]]
      if current > max_in_circle:
        dots_dict = {}
        dots_dict[frozenset(dots_in)]=[[x1, y1]]
        max_in_circle = current
      current = 0

    # https://stackoverflow.com/questions/10190981/get-a-unique-id-for-worker-in-python-multiprocessing-pool
    print(multiprocessing.current_process().name, 100*(x1-xr1)/(xr2-xr1), '%',sep=' ', end='\n', flush=True)
  print(multiprocessing.current_process().name, 'MAX:', max_in_circle, sep=' ')

#  return (max_in_circle, circles)
  return (max_in_circle, dots_dict)

if __name__ == "__main__":
  #print ('Number of arguments:', len(sys.argv), 'arguments.')
  #print ('Argument List:', str(sys.argv))

  if len(sys.argv) < 3:
    print("USAGE:   python draw_map.py <coord_file.txt> <ore>[ <ore>...]")
    print("EXAMPLE: python draw_map.py resourses_326_516_size_30.txt copper tetrahedrite redstone")
    print("         OR")
    print("         python draw_map.py resourses_326_516_size_30.txt -circle 325 516")
    sys.exit()

  #-------------------------------------------------------
  calculate = True

  xrange1 =  2^63 - 1
  xrange2 = -2^63 + 1
  yrange1 =  2^63 - 1
  yrange2 = -2^63 + 1

  # Ore Drilling Plant I   - radius is 48 blocks
  # Ore Drilling Plant II  - radius is 64 blocks
  # Ore Drilling Plant III - radius is 96 blocks
  # Ore Drilling Plant IV  - radius is 144 blocks
  RADIUS = 96
  #-------------------------------------------------------

  f = open(sys.argv[1], 'r')
  lines = f.readlines()
  f.close()

  coord_dict = {}
  for line in lines:
    #                      1        2        3            4            5
    search = re.search('(-?\d+)\s(-?\d+)\s(-?\d+)\s([0-9a-z\.]+)\s*(<-skip)?', line.strip(), re.IGNORECASE)
  
    if search:
      if search.group(5): # skip present
        print(line.strip())
        continue

      x = int(search.group(1))
      y = int(search.group(2))
      z = int(search.group(3))
      ore = search.group(4)

      if x < xrange1:
        xrange1 = x
      if x > xrange2:
        xrange2 = x
      if z < yrange1:
        yrange1 = z
      if z > yrange2:
        yrange2 = z

      if ore in coord_dict:
        coord_dict.get(ore).append([x,y,z])
      else:
        coord_dict[ore] = [[x,y,z]]

  print ("Ores Available: ")
  index = 1
  for ore in coord_dict:
    print(index, ore, '(',len(coord_dict[ore]),')')
    index += 1
  print()

  if (sys.argv[2] == '-circle'):
    calculate = False

  # Algorithms:
  # https://www.quora.com/What-is-an-algorithm-for-enclosing-the-maximum-number-of-points-in-a-2-D-plane-with-a-fixed-radius-circle
  # https://math.stackexchange.com/questions/1650793/algorithm-to-cover-maximal-number-of-points-with-one-circle-of-given-radius
  # https://stackoverflow.com/questions/3229459/algorithm-to-cover-maximal-number-of-points-with-one-circle-of-given-radius
  # !!!  https://www.geeksforgeeks.org/angular-sweep-maximum-points-can-enclosed-circle-given-radius/
  results = []
  if calculate:
    dots = []
    # https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python
    for ore in sys.argv[2:]:
      dots += coord_dict[ore]
    # https://realpython.com/python-concurrency/
    with multiprocessing.Pool() as pool:
      # https://stackoverflow.com/questions/20353956/get-number-of-workers-from-process-pool-in-python-multiprocessing-module
      print('Number of CPUs: ', pool._processes)

      # https://stackoverflow.com/questions/47374944/linspace-generates-a-float-values-but-int-is-required
      # UNCOMMENT FOR THE FULL RANGE
      ranges = np.linspace(xrange1 + RADIUS, xrange2 - RADIUS, pool._processes + 1, dtype='int')
      # example: ABS MAX:  6
      # example: frozenset({(408, 112, -168), (408, 109, -216), (408, 10, -264), (456, 92, -216), (456, 34, -264), (504, 14, -216)}) :  [442, -222]
      #ranges = np.linspace(350, 650, pool._processes + 1, dtype='int')
      step = ranges[1] - ranges[0]

      # print([(x,  x+step, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS) for x in ranges[:-1]])
      #
      # For example, for 8 CPUs the following will be invoked for the X range of -1136:1936 :
      # CPU 0: iterate_over_x_y_range(-1136, -752, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots)
      # CPU 1: iterate_over_x_y_range( -752, -368, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) 
      # CPU 2: iterate_over_x_y_range( -368,   16, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) 
      # CPU 3: iterate_over_x_y_range(   16,  400, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) 
      # CPU 4: iterate_over_x_y_range(  400,  784, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) 
      # CPU 5: iterate_over_x_y_range(  784, 1168, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) 
      # CPU 6: iterate_over_x_y_range( 1168, 1552, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) 
      # CPU 7: iterate_over_x_y_range( 1552, 1936, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots)

      # https://docs.python.org/dev/library/multiprocessing.html#multiprocessing.pool.Pool.starmap
      results = pool.starmap(iterate_over_x_y_range, [
        (x,  x+step, yrange1 + RADIUS, yrange2 - RADIUS, RADIUS, dots) for x in ranges[:-1]
      ])

  # Looking for the MAX number of dots in the circles returned from CPU workers (results)
  abs_max_in_circle = 0
  for (max_in_circle, dots_dict) in results:
    if max_in_circle > abs_max_in_circle:
      abs_max_in_circle = max_in_circle
  print('ABS MAX: ', abs_max_in_circle)

  # Of those circles with MAX dots composing the dictionary:
  # each dot tuple is associated with the array of circles they contained in
  # ( (dot, dot, ...) -> [circle1, circle2, ..., circleN] )
  abs_dots_dict = {}
  for (max_in_circle, dots_dict) in results:
    if max_in_circle == abs_max_in_circle:
      for dots, circles in dots_dict.items():
        if dots in abs_dots_dict:
          abs_dots_dict[dots] += circles
        else:
          abs_dots_dict[dots] = circles
#        print(dots, ': ', circles)

  # Of all circles for each tuple of dots find the one circle which 
  # has the minimum sum of distances from it's center to each dot
  # ( (dot, dot, ...) -> circle_with_min_distance )
  abs_dots_circle_dict = {}
  for dots, circles in abs_dots_dict.items():
#    print(dots, ': ', circles)
#    print('DOTS: ', dots)
    min_distance = 9999
    for (x1, y1) in circles:
      sum_dist = 0
      for (x2, y2, z2) in dots:
        sum_dist += distance(x1, y1, x2, z2)
#      print(x1, y1, dist, '(',min_distance, ')', sep=' ')
      if (sum_dist < min_distance):
        min_distance = sum_dist
        # if the circle with the lesser sum is found update the dictionary with it
        abs_dots_circle_dict[frozenset(dots)] = [x1, y1]

  # Print the final results
  for dots, circle in abs_dots_circle_dict.items():
    print(dots, ': ', circle)

  # Adding all ores within a circle
  additional = {}
  for dots, circle in abs_dots_circle_dict.items():
    print('CIRCLE:',circle[0], ',',circle[1])
    for ore in coord_dict:
      if ore in sys.argv[2:]:
        continue
      for x,y,z in coord_dict[ore]:
        if abs(x-circle[0]) > RADIUS or abs(z-circle[1]) > RADIUS:
          continue
        if distance(circle[0], circle[1], x, z) < RADIUS:
          print('    DOT:',x,',',y,',',z,' (', ore, ')')
          if ore in additional:
            additional[ore].append([x,y,z])
          else:
            additional[ore] = [[x,y,z]]

  within_circle_dict = {}
  if (sys.argv[2] == '-circle'):
    print('CIRCLE:',sys.argv[3], ',',sys.argv[4])
    cx = int(sys.argv[3])
    cy = int(sys.argv[4])

    for ore in coord_dict:
      for x,y,z in coord_dict[ore]:
        if abs(x-cx) > RADIUS or abs(z-cy) > RADIUS:
          continue
        if distance(cx, cy, x, z) < RADIUS:
          print('    DOT:', x,',', y,',', z,' (', ore, ')')
          if ore in within_circle_dict:
            within_circle_dict[ore].append([x,y,z])
          else:
            within_circle_dict[ore] = [[x,y,z]]


  #*************** PLOT CONFIG ******************
  fig, ax = plt.subplots()
  #ax = plt.subplot()

  # https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels-in-matplotlib
  # Major ticks every 2*RADIUS, minor ticks every chunk (16)
  major_ticks_x = np.arange(xrange1, xrange2, RADIUS*2)
  major_ticks_y = np.arange(yrange1, yrange2, RADIUS*2)
  minor_ticks_x = np.arange(xrange1, xrange2, 16)
  minor_ticks_y = np.arange(yrange1, yrange2, 16)

  ax.set_xticks(major_ticks_x)
  ax.set_xticks(minor_ticks_x, minor=True)
  ax.set_yticks(major_ticks_y)
  ax.set_yticks(minor_ticks_y, minor=True)

  # https://stackoverflow.com/questions/10998621/rotate-axis-text-in-python-matplotlib
  plt.xticks(rotation=90)

  # https://stackoverflow.com/questions/7965743/how-can-i-set-the-aspect-ratio-in-matplotlib
  ax.set_aspect('equal')

  # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.grid.html
  # linestyle or ls {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
  # http://jonathansoma.com/lede/data-studio/matplotlib/adding-grid-lines-to-a-matplotlib-chart/
  # Customize the major grid
  ax.grid(which='major', linestyle='-', linewidth='0.3', color='red')
  # Customize the minor grid
  ax.grid(which='minor', linestyle=':', linewidth='0.1', color='black')

  #*************** PLOT CONFIG END ******************

  colors = []
  if (sys.argv[2] == '-circle'):
    #https://stackoverflow.com/questions/12236566/setting-different-color-for-each-series-in-scatter-plot-on-matplotlib
    colors = cm.rainbow(np.linspace(0, 1, len(within_circle_dict.items())))
  else:
    #https://stackoverflow.com/questions/12236566/setting-different-color-for-each-series-in-scatter-plot-on-matplotlib
    colors = cm.rainbow(np.linspace(0, 1, len(sys.argv) - 2 + len(additional.items())))

  #https://stackoverflow.com/questions/47684652/how-to-customize-marker-colors-and-shapes-in-scatter-plot
  #markers = ["." , "," , "o" , "v" , "^" , "<", ">"]
  # excluding "." since it is confused with "o"
  markers = ["," , "o" , "v" , "^" , "<", ">"]

  ###################################################
  # !!! https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib

  index = 0

  if (sys.argv[2] == '-circle'):
    for ore, dots in within_circle_dict.items():
      #x, y, z = np.array(dots).T
      x, y, z = np.array(coord_dict[ore]).T
      ax.scatter(x, z, s=16, marker=markers[index % len(markers)], color=colors[index % len(colors)], label = ore)
      index += 1

    cx = int(sys.argv[3])
    cy = int(sys.argv[4])
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html
    ax.text(cx, cy + RADIUS + 10, 'x:' + str(cx) + ' z:' + str(cy))
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Circle.html
    ax.add_artist(plt.Circle((cx, cy), RADIUS, fill=False))

  else:
    for ore in sys.argv[2:]:
      x, y, z = np.array(coord_dict[ore]).T
      ax.scatter(x, z, s=16, marker=markers[index % len(markers)], color=colors[index % len(colors)], label = ore)
      index += 1

    for ore, dots in additional.items():
      x, y, z = np.array(dots).T
      ax.scatter(x, z, s=16, marker=markers[index % len(markers)], color=colors[index % len(colors)], label = ore)
      index += 1

#  x, y, z = np.array(coord_dict['copper']).T
#  ax.scatter(x,z, s=16, marker=markers[0], color=colors[0], label = 'copper')

  for dots, circle in abs_dots_circle_dict.items():
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html
    ax.text(circle[0], circle[1] + RADIUS + 10, 'x:' + str(circle[0]) + ' z:' + str(circle[1]))
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Circle.html
    ax.add_artist(plt.Circle((circle[0], circle[1]), RADIUS, fill=False))

#    UNCOMMENT BELOW TO SEE ALL CIRCLES FOR CURRENT DOTS:
#    for circle in abs_dots_dict[dots]:
#      # https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Circle.html
#      ax.add_artist(plt.Circle((circle[0], circle[1]), RADIUS, fill=False, linestyle=':', linewidth='0.1'))
  ###################################################

  ax.legend()
  plt.show()