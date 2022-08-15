#! /usr/bin/env python3

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

writefiles = ["results/ht-q/bp4-4node-ceph-write-551849-small.tsv"]
# "results/sqlite/julea-DBDO-sqlite-4cs-write-79040.tsv",
        #  "results/bp3/bp3-4node-lustre-write-79032.tsv","results/bp4/bp4-4node-lustre-write-79050.tsv"]
readfiles = ["results/ht-q/bp4-4node-ceph-write-551849-small.tsv"]
# readfiles = ["results/mariadb/julea-DBDO-mariadb-4cs-read-79021.tsv","results/sqlite/julea-DBDO-sqlite-4cs-read-79040.tsv",
        #  "results/bp3/bp3-4node-lustre-read-79032.tsv","results/bp4/bp4-4node-lustre-read-79050.tsv"]

steps = 100

labels = ['4']
# labels = ['4', '12', '24', '48', '96', '192']
# N = 6 # number x-labels
# xlocationLabels = np.arange(N)

# https://regexr.com/5d7ug
pattern = re.compile(r"MPI_Comm_size:\s(\d+)\n.*\n\d+\s+\d+\s+(\d+).*\n\n# "\
                     + r"Mean.*\n((?:\d+.*\n)+)Total runtime = (\d+\.\d+)s")


def get_mean_datarates(data, size):
    datarates = []

    matches = pattern.finditer(data)
    for match in matches:
        n_procs = int(match.group(1))
        if (size != int(match.group(2))):
            continue

        means = np.asarray(match.group(3).split(),
                            dtype=np.int).reshape(steps, n_procs+2)[:,0]

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
    # rates.append(get_mean_datarates(data, 1024))
    writeRates.append(get_mean_datarates(data, 4096))

for f in readfiles:
    data = ""
    with open(f, 'r') as fi:
        data = fi.read()
    readRates.append(get_mean_datarates(data, 4096))


# fig, ax = plt.subplots()
fig, ax = plt.subplots(1, 2, sharey="row")

positions0 = [3 * i - 0.9 for i in range(len(writeRates[0]))]
positions1 = [3 * i - 0.3 for i in range(len(writeRates[0]))]
positions2 = [3 * i + 0.3 for i in range(len(writeRates[0]))]
positions3 = [3 * i + 0.9 for i in range(len(writeRates[0]))]

fontsize = 27
fontdict = {"fontsize": fontsize}

ax[0].set_xticks([3 * i for i in range(len(writeRates[0]))])
ax[0].set_xticklabels(labels, fontdict=fontdict)
ax[0].set_ylabel('MB/s', fontdict=fontdict)
ax[0].set_xlabel('# Processes', fontdict=fontdict)
ax[0].set_title('Write performance for 4 nodes', fontdict=fontdict)

ax[1].set_xticks([3 * i for i in range(len(writeRates[0]))])
ax[1].set_xticklabels(labels, fontdict=fontdict)
#ax[1].set_ylabel('MB/s', fontdict=fontdict)
ax[1].set_xlabel('# Processes', fontdict=fontdict)
ax[1].set_title('Read performance for 4 nodes', fontdict=fontdict)


barwidth=0.5

ax[0].bar(positions0, np.mean(writeRates[0], axis=1), width=barwidth,
          hatch="*", label="MariaDB",
          color="cornflowerblue", edgecolor="black")
# ax[0].bar(positions1, np.mean(writeRates[1], axis=1), width=barwidth,
#           hatch="O", label="SQLite",
#           color="lavender", edgecolor="black")
# ax[0].bar(positions2, np.mean(writeRates[2], axis=1), width=barwidth,
#           hatch="//", label="BP3",
#           color="orange", edgecolor="black")
# ax[0].bar(positions3, np.mean(writeRates[3], axis=1), width=barwidth,
#           hatch="//", label="BP4",
#           color="indianred", edgecolor="black")

ax[1].bar(positions0, np.mean(readRates[0], axis=1), width=barwidth, hatch="*",
          label="MariaDB",
          color="cornflowerblue", edgecolor="black")
# ax[1].bar(positions1, np.mean(readRates[1], axis=1), width=barwidth, hatch="O",
#           label="SQLite",
#           color="lavender", edgecolor="black")
# ax[1].bar(positions2, np.mean(readRates[2], axis=1), width=barwidth,
#           hatch="//", label="BP3",
#           color="orange", edgecolor="black")
# ax[1].bar(positions3, np.mean(readRates[3], axis=1), width=barwidth,
#           hatch="//", label="BP4",
#           color="indianred", edgecolor="black")


ax[0].tick_params(axis="y", labelsize=fontsize)
#ax[1].tick_params(axis="y", labelsize=fontsize)


#ax[0].set_ylim(ax[1].get_ylim())
ax[0].legend(loc="upper left", fontsize=fontsize-6, ncol=2)

# plt.xticks(xlocationLabels, labels)
# plt.set_loglevel("info")
plt.show()

ax[0].set_xmargin(0.01)
ax[1].set_xmargin(0.01)

fig.set_dpi(300)
fig.set_size_inches(15, 5)
fig.set_tight_layout("pad")

#fig.savefig('test_plot.pdf')
fig.savefig('4node_write_read_4096_new_larger_font.pdf')
