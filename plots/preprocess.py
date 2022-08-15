#! /usr/bin/env python3

import sys
import re
import numpy as np
import matplotlib.pyplot as plt


pattern = re.compile(r"MPI_Comm_size:\s(\d+)\n.*\n\d+\s+\d+\s+(\d+).*\n\n# "\
                     + r"Mean.*\n((?:\d+.*\n){11})Total runtime = (\d+\.\d+)s")

data = sys.stdin.read()

matches = pattern.finditer(data)

print("n_procs\tmean[1024]\tstd[1024]\tmin[1024]\tmax[1024]"\
      + "\tmean[2048]\tstd[2048]\tmin[2048]\tmax[2048]"\
      + "\tmean[4096]\tstd[4096]\tmin[4096]\tmax[4096]")

fig, ax_list = plt.subplots(1, 6)

steps = 10

i = 0
j = 0
plot_data = []
sizes = []
for match in matches:
    n_procs = int(match.group(1))
    if (i == 0):
        plot_data = []
        sizes = []
        print(n_procs, end="\t")
    # print(n_procs)
    size = int(match.group(2))
    sizes.append(str(size))
    # print(size)
    values = np.asarray(match.group(3).split(),
                        dtype=np.int).reshape(steps+1, n_procs+2)[1:,2:]
    means = np.asarray(match.group(3).split(),
                        dtype=np.int).reshape(steps+1, n_procs+2)[1:,0]
    # fig1, ax1 = plt.subplots()
    # ax1.set_title('n_procs: {0} size: {1}'.format(n_procs, size))
    # ax1.boxplot(means)
    # print(values)
    # plot_data.append(means)
    mean_datarate = (4 * size * size * n_procs) / means
    # convert from byte per microsecond to MB / s
    mean_datarate *= 1e6 / (1024 * 1024)
    plot_data.append(mean_datarate)
    mean = np.mean(values)
    print("{0:.2f}".format(mean), end="\t")
    std = np.std(values)
    print("{0:.2f}".format(std), end="\t")
    vmin = np.amin(values)
    print("{0:.2f}".format(vmin), end="\t")
    vmax = np.amax(values)
    print("{0:.2f}".format(vmax), end="\t")
    runtime = float(match.group(4))
    # print(runtime)
    i += 1
    if (i == 3):
        print(plot_data)
        print(sizes)
        ax_list[j].set_title("Processes: {0}".format(n_procs))
        #ax_list[j].set_xticks(list(range(1, len(sizes)+1)))
        ax_list[j].boxplot(plot_data, labels=sizes)
        #ax_list[j].set_xticklabels(sizes)
        print("")
        i = 0
        j += 1

plt.show()
