#! /usr/bin/env python3

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

writefiles = ["results/mariadb/julea-DBDO-mariadb-1node-write-79029.tsv","results/sqlite/julea-DBDO-sqlite-1node-write-79037.tsv",
         "results/bp3/bp3-local-write-79056.tsv","results/bp3/bp3-1node-lustre-write-79027.tsv","results/bp4/bp4-local-write-79055.tsv","results/bp4/bp4-1node-lustre-write-79058.tsv"]

readfiles = ["results/mariadb/julea-DBDO-mariadb-1node-read-79029.tsv","results/sqlite/julea-DBDO-sqlite-1node-read-79037.tsv",
         "results/bp3/bp3-local-read-79056.tsv","results/bp3/bp3-1node-lustre-read-79027.tsv","results/bp4/bp4-local-read-79055.tsv","results/bp4/bp4-1node-lustre-read-79058.tsv"]

steps = 10

labels = ['1', '3', '6', '12', '24', '48']
# N = 6 # number x-labels
# xlocationLabels = np.arange(N)

# https://regexr.com/5d7ug
pattern = re.compile(r"MPI_Comm_size:\s(\d+)\n.*\n\d+\s+\d+\s+(\d+).*\n\n# "\
                     + r"Mean.*\n((?:\d+.*\n){11})Total runtime = (\d+\.\d+)s")


def get_mean_datarates(data, size):
    datarates = []

    matches = pattern.finditer(data)
    for match in matches:
        n_procs = int(match.group(1))
        if (size != int(match.group(2))):
            continue

        means = np.asarray(match.group(3).split(),
                            dtype=np.int).reshape(steps+1, n_procs+2)[:,0]

        mean_datarate = (4 * size * size * n_procs) / means

        # convert from byte per microsecond to MB / s
        mean_datarate *= 1e6 / (1024 * 1024)

        datarates.append(mean_datarate)

    return datarates


writeRates = []
readRates = []

for f in writefiles:
    data = ""
    with open(f, 'r') as fi:
        data = fi.read()
    # writeRates.append(get_mean_datarates(data, 1024))
    # writeRates.append(get_mean_datarates(data, 2048))
    writeRates.append(get_mean_datarates(data, 4096))

for f in readfiles:
    data = ""
    with open(f, 'r') as fi:
        data = fi.read()
    # readRates.append(get_mean_datarates(data, 1024))
    # readRates.append(get_mean_datarates(data, 2048))
    readRates.append(get_mean_datarates(data, 4096))


# fig, ax = plt.subplots()
fig, ax = plt.subplots(1, 2, sharey="row")

positions0 = [5.7 * i - 2.0 for i in range(len(writeRates[0]))]
positions1 = [5.7 * i - 1.2 for i in range(len(writeRates[0]))]
positions2 = [5.7 * i - 0.4 for i in range(len(writeRates[0]))]
positions3 = [5.7 * i + 0.4 for i in range(len(writeRates[0]))]
positions4 = [5.7 * i + 1.2 for i in range(len(writeRates[0]))]
positions5 = [5.7 * i + 2.0 for i in range(len(writeRates[0]))]

fontsize = 16
fontdict = {"fontsize": fontsize}

ax[0].set_xticks([5.7 * i for i in range(len(writeRates[0]))])
ax[0].set_xticklabels(labels, fontdict=fontdict)
ax[0].set_ylabel('MB/s', fontdict=fontdict)
ax[0].set_xlabel('# Processes', fontdict=fontdict)
ax[0].set_title('Write performance for 1 node', fontdict=fontdict)

ax[1].set_xticks([5.7 * i for i in range(len(writeRates[0]))])
ax[1].set_xticklabels(labels, fontdict=fontdict)
# ax[1].set_ylabel('MB/s', fontdict=fontdict)
ax[1].set_xlabel('# Processes', fontdict=fontdict)
ax[1].set_title('Read performance for 1 node', fontdict=fontdict)

barwidth=0.6

ax[0].bar(positions0, np.mean(writeRates[0], axis=1), width=barwidth,
          hatch="*", label="MariaDB",
          color="cornflowerblue", edgecolor="black")
ax[0].bar(positions1, np.mean(writeRates[1], axis=1), width=barwidth,
          hatch="O", label="SQLite",
          color="lavender", edgecolor="black")
ax[0].bar(positions2, np.mean(writeRates[2], axis=1), width=barwidth,
          hatch="//", label="BP3 local",
          color="orange", edgecolor="black")
ax[0].bar(positions3, np.mean(writeRates[3], axis=1), width=barwidth,
          hatch="//", label="BP3 Lustre",
          color="orange", edgecolor="black")
ax[0].bar(positions4, np.mean(writeRates[4], axis=1), width=barwidth,
          hatch="\\", label="BP4 local",
          color="indianred", edgecolor="black")
ax[0].bar(positions5, np.mean(writeRates[5], axis=1), width=barwidth,
          hatch="\\", label="BP4 Lustre",
          color="indianred", edgecolor="black")


ax[1].bar(positions0, np.mean(readRates[0], axis=1), width=barwidth, hatch="*",
          label="MariaDB",
          color="cornflowerblue", edgecolor="black")
ax[1].bar(positions1, np.mean(readRates[1], axis=1), width=barwidth, hatch="O",
          label="SQLite",
          color="lavender", edgecolor="black")
ax[1].bar(positions2, np.mean(readRates[2], axis=1), width=barwidth,
          hatch="//", label="BP3 local",
          color="orange", edgecolor="black")
ax[1].bar(positions3, np.mean(readRates[3], axis=1), width=barwidth,
          hatch="//", label="BP3 Lustre",
          color="orange", edgecolor="black")
ax[1].bar(positions4, np.mean(readRates[4], axis=1), width=barwidth,
          hatch="\\", label="BP4 local",
          color="indianred", edgecolor="black")
ax[1].bar(positions5, np.mean(readRates[5], axis=1), width=barwidth,
          hatch="\\", label="BP4 Lustre",
          color="indianred", edgecolor="black")



ax[0].tick_params(axis="y", labelsize=fontsize)
#ax[1].tick_params(axis="y", labelsize=fontsize)

#ax[0].set_ylim(ax[1].get_ylim())
ax[0].legend(loc="upper left", fontsize=fontsize)
# ax[1].legend()

# plt.xticks(xlocationLabels, labels)
# plt.set_loglevel("info")
# plt.show()

# print(ax[0].margins())
ax[0].set_xmargin(0.01)
ax[1].set_xmargin(0.01)



fig.set_dpi(300)
fig.set_size_inches(15, 5)
fig.set_tight_layout("pad")

#fig.savefig('test_plot.pdf')
# fig.savefig('1node_write_read_1024_new.pdf')
# fig.savefig('1node_write_read_2048_new_without_legend.pdf')
# fig.savefig('1node_write_read_4096_new_without_legend.pdf')
fig.savefig('1node_write_read_4096_systor_legend.pdf')
