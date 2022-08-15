#! /usr/bin/env python3

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl

files1node =  ["results/mariadb/julea-DBDO-mariadb-1node-query-julea-79029_fixed.tsv","results/mariadb/julea-DBDO-mariadb-1node-query-adios-79029.tsv",
        "results/sqlite/julea-DBDO-sqlite-1node-query-julea-79037_fixed.tsv","results/sqlite/julea-DBDO-sqlite-1node-query-adios-79037.tsv",
         "results/bp3/bp3-1node-lustre-query-79027.tsv","results/bp4/bp4-1node-lustre-query-79058.tsv"]

files2nodes =  ["results/mariadb/julea-DBDO-mariadb-2c-2s-query-julea-79054_fixed.tsv","results/mariadb/julea-DBDO-mariadb-2c-2s-query-adios-79054.tsv",
        "results/sqlite/julea-DBDO-sqlite-2c-2s-query-julea-79038_fixed.tsv","results/sqlite/julea-DBDO-sqlite-2c-2s-query-adios-79038.tsv",
         "results/bp3/bp3-2node-lustre-query-79042.tsv","results/bp4/bp4-2node-lustre-query-79053.tsv"]


files4nodes =  ["results/mariadb/julea-DBDO-mariadb-4cs-query-julea-79021_fixed.tsv","results/mariadb/julea-DBDO-mariadb-4cs-query-adios-79021.tsv",
        "results/sqlite/julea-DBDO-sqlite-4cs-query-julea-79040_fixed.tsv","results/sqlite/julea-DBDO-sqlite-4cs-query-adios-79040.tsv",
         "results/bp3/bp3-4node-lustre-query-79032.tsv","results/bp4/bp4-4node-lustre-query-79050.tsv"]


steps = 10

labels1 = ['1', '3', '6', '12', '24', '48']
labels2 = [str(2 * int(i)) for i in labels1]
labels4 = [str(2 * int(i)) for i in labels2]

width = 0.5

pattern = re.compile(r"MPI_Comm_size:\s(\d+)\n.*\n\d+\s+\d+\s+(\d+).*\n\n*.*"\
                        + r"\n.*\nTotal runtime = (\d+\.\d+)s")


def get_query_times(data, size):
    query_times = []

    matches = pattern.finditer(data)
    for match in matches:
        n_procs = int(match.group(1))
        if (size != int(match.group(2))):
            continue

        query_time = float(match.group(3))
        query_times.append(query_time)

    return query_times


times_1node = []
times_2nodes = []
times_4nodes = []

for f in files1node:
    data = ""
    with open(f, 'r') as fi:
        data = fi.read()
    times_1node.append(get_query_times(data, 4096))

for f in files2nodes:
    data = ""
    with open(f, 'r') as fi:
        data = fi.read()
    times_2nodes.append(get_query_times(data, 4096))

for f in files4nodes:
    data = ""
    with open(f, 'r') as fi:
        data = fi.read()
    times_4nodes.append(get_query_times(data, 4096))

# fig, ax = plt.subplots()
fig, ax = plt.subplots(1, 3, sharey="row")

positions0 = [5.7 * i - 2.0 for i in range(len(times_4nodes[0]))]
positions1 = [5.7 * i - 1.2 for i in range(len(times_4nodes[0]))]
positions2 = [5.7 * i - 0.4 for i in range(len(times_4nodes[0]))]
positions3 = [5.7 * i + 0.4 for i in range(len(times_4nodes[0]))]
positions4 = [5.7 * i + 1.2 for i in range(len(times_4nodes[0]))]
positions5 = [5.7 * i + 2.0 for i in range(len(times_4nodes[0]))]


# def log_10_product(x, pos):
#     """The two args are the value and tick position.
#     Label ticks with the product of the exponentiation"""
#     return '%1i' % (x)

ax[0].set_yscale('log')
#ax[1].set_yscale('log')
#ax[2].set_yscale('log')

# formatter = ticker.FuncFormatter(log_10_product)
# ax[2].yaxis.set_major_formatter(formatter)
# ax[2].set_ylim(1e-2, 1e3)

fontsize = 14
fontdict = {"fontsize": fontsize}

ax[0].set_xticks([5.7 * i for i in range(len(times_1node[0]))])
ax[0].set_xticklabels(labels1, fontdict=fontdict)
ax[0].set_ylabel('s', fontdict=fontdict)
ax[0].set_xlabel('# Blocks', fontdict=fontdict)
ax[0].set_title('Query time for 1 node', fontdict=fontdict)

ax[1].set_xticks([5.7 * i for i in range(len(times_2nodes[0]))])
ax[1].set_xticklabels(labels2, fontdict=fontdict)
#ax[1].set_ylabel('s', fontdict=fontdict)
ax[1].set_xlabel('# Blocks', fontdict=fontdict)
ax[1].set_title('Query time for 2 nodes', fontdict=fontdict)

ax[2].set_xticks([5.7 * i for i in range(len(times_4nodes[0]))])
ax[2].set_xticklabels(labels4, fontdict=fontdict)
#ax[2].set_ylabel('s', fontdict=fontdict)
ax[2].set_xlabel('# Blocks', fontdict=fontdict)
ax[2].set_title('Query time for 4 nodes', fontdict=fontdict)

barwidth=0.6

# ax[0].bar(positions0, times_1node[0], width=barwidth, hatch="*",
#           label="JULEA-Query MariaDB",
#           color="cornflowerblue", edgecolor="black")
# ax[0].bar(positions1, times_1node[1], width=barwidth, hatch="*",
#           label="ADIOS2-Query MariaDB",
#           color="cornflowerblue", edgecolor="black")
# ax[0].bar(positions2, times_1node[2], width=barwidth, hatch="O",
#           label="JULEA-Query SQLite",
#           color="lavender", edgecolor="black")
# ax[0].bar(positions3, times_1node[3], width=barwidth, hatch="O",
#           label="ADIOS2-Query SQLite",
#           color="lavender", edgecolor="black")
# ax[0].bar(positions4, times_1node[4], width=barwidth, hatch="//",
#           label="ADIOS2-Query BP3",
#           color="orange", edgecolor="black")
# ax[0].bar(positions5, times_1node[5], width=barwidth, hatch="\\",
#           label="ADIOS2-Query BP4",
#           color="indianred", edgecolor="black")

# ax[1].bar(positions0, times_2nodes[0], width=barwidth, hatch="*",
#           label="JULEA-Query MariaDB",
#           color="cornflowerblue", edgecolor="black")
# ax[1].bar(positions1, times_2nodes[1], width=barwidth, hatch="*",
#           label="ADIOS2-Query MariaDB",
#           color="cornflowerblue", edgecolor="black")
# ax[1].bar(positions2, times_2nodes[2], width=barwidth, hatch="O",
#           label="JULEA-Query SQLite",
#           color="lavender", edgecolor="black")
# ax[1].bar(positions3, times_2nodes[3], width=barwidth, hatch="O",
#           label="ADIOS2-Query SQLite",
#           color="lavender", edgecolor="black")
# ax[1].bar(positions4, times_2nodes[4], width=barwidth, hatch="//",
#           label="ADIOS2-Query BP3",
#           color="orange", edgecolor="black")
# ax[1].bar(positions5, times_2nodes[5], width=barwidth, hatch="\\",
#           label="ADIOS2-Query BP4",
#           color="indianred", edgecolor="black")

# ax[2].bar(positions0, times_4nodes[0], width=barwidth, hatch="*",
#           label="JULEA-Query MariaDB",
#           color="cornflowerblue", edgecolor="black")
# ax[2].bar(positions1, times_4nodes[1], width=barwidth, hatch="*",
#           label="ADIOS2-Query MariaDB",
#           color="cornflowerblue", edgecolor="black")
# ax[2].bar(positions2, times_4nodes[2], width=barwidth, hatch="O",
#           label="JULEA-Query SQLite",
#           color="lavender", edgecolor="black")
# ax[2].bar(positions3, times_4nodes[3], width=barwidth, hatch="O",
#           label="ADIOS2-Query SQLite",
#           color="lavender", edgecolor="black")
# ax[2].bar(positions4, times_4nodes[4], width=barwidth, hatch="//",
#           label="ADIOS2-Query BP3",
#           color="orange", edgecolor="black")
# ax[2].bar(positions5, times_4nodes[5], width=barwidth, hatch="\\",
#           label="ADIOS2-Query BP4",
#           color="indianred", edgecolor="black")


# Different grouping
ax[0].bar(positions0, times_1node[0], width=barwidth, hatch="*",
          label="JULEA-Q MariaDB",
          # label="JULEA-Query MariaDB",
          color="cornflowerblue", edgecolor="black")
ax[0].bar(positions1, times_1node[2], width=barwidth, hatch="*",
          label="JULEA-Q SQLite",
          # label="JULEA-Query SQLite",
          color="cornflowerblue", edgecolor="black")
ax[0].bar(positions2, times_1node[1], width=barwidth, hatch="O",
          label="ADIOS2-Q MariaDB",
          # label="ADIOS2-Query MariaDB",
          color="lavender", edgecolor="black")
ax[0].bar(positions3, times_1node[3], width=barwidth, hatch="O",
          label="ADIOS2-Q SQLite",
          # label="ADIOS2-Query SQLite",
          color="lavender", edgecolor="black")
ax[0].bar(positions4, times_1node[4], width=barwidth, hatch="//",
          label="ADIOS2-Q BP3",
          # label="ADIOS2-Query BP3",
          color="orange", edgecolor="black")
ax[0].bar(positions5, times_1node[5], width=barwidth, hatch="\\",
          label="ADIOS2-Q BP4",
          # label="ADIOS2-Query BP4",
          color="indianred", edgecolor="black")

ax[1].bar(positions0, times_2nodes[0], width=barwidth, hatch="*",
          label="JULEA-Query MariaDB",
          color="cornflowerblue", edgecolor="black")
ax[1].bar(positions1, times_2nodes[2], width=barwidth, hatch="*",
          label="JULEA-Query SQLite",
          color="cornflowerblue", edgecolor="black")
ax[1].bar(positions2, times_2nodes[1], width=barwidth, hatch="O",
          label="ADIOS2-Query MariaDB",
          color="lavender", edgecolor="black")
ax[1].bar(positions3, times_2nodes[3], width=barwidth, hatch="O",
          label="ADIOS2-Query SQLite",
          color="lavender", edgecolor="black")
ax[1].bar(positions4, times_2nodes[4], width=barwidth, hatch="//",
          label="ADIOS2-Query BP3",
          color="orange", edgecolor="black")
ax[1].bar(positions5, times_2nodes[5], width=barwidth, hatch="\\",
          label="ADIOS2-Query BP4",
          color="indianred", edgecolor="black")

ax[2].bar(positions0, times_4nodes[0], width=barwidth, hatch="*",
          label="JULEA-Query MariaDB",
          color="cornflowerblue", edgecolor="black")
ax[2].bar(positions1, times_4nodes[2], width=barwidth, hatch="*",
          label="JULEA-Query SQLite",
          color="cornflowerblue", edgecolor="black")
ax[2].bar(positions2, times_4nodes[1], width=barwidth, hatch="O",
          label="ADIOS2-Query MariaDB",
          color="lavender", edgecolor="black")
ax[2].bar(positions3, times_4nodes[3], width=barwidth, hatch="O",
          label="ADIOS2-Query SQLite",
          color="lavender", edgecolor="black")
ax[2].bar(positions4, times_4nodes[4], width=barwidth, hatch="//",
          label="ADIOS2-Query BP3",
          color="orange", edgecolor="black")
ax[2].bar(positions5, times_4nodes[5], width=barwidth, hatch="\\",
          label="ADIOS2-Query BP4",
          color="indianred", edgecolor="black")

ax[0].tick_params(axis="y", labelsize=fontsize)
#ax[1].tick_params(axis="y", labelsize=fontsize)
#ax[2].tick_params(axis="y", labelsize=fontsize)

# ax[0].legend(loc="best", fontsize=fontsize-2)
ax[0].legend(loc="best", fontsize=fontsize-3, ncol=2)
#ax[0].legend(loc="upper left", fontsize=fontsize)

ax[0].set_xmargin(0.01)
ax[1].set_xmargin(0.01)
ax[2].set_xmargin(0.01)

# suggested by formatting tool of hotcrp
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
#fig.set_dpi(300)
# fig.set_size_inches(15, 5)
fig.set_size_inches(15, 4)
fig.set_tight_layout("pad")

#fig.savefig('test_plot.pdf')
# fig.savefig('query_new.pdf')
# fig.savefig('query_new_regroup.pdf')
fig.savefig('query_new_regroup4.pdf')
# ax[0].set_ylim(ax[1].get_ylim())
# plt.set_loglevel("debug")

plt.show()
