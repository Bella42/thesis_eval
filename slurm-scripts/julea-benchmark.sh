#!/bin/bash

#SBATCH -N 1 --ntasks-per-node=48
#SBATCH --partition=parcio
# SBATCH --error=../../results/output/dbdo-mariadb-1node-%j.err --output=../../results/output/dbdo-mariadb-1node-%j.out

# ---------------- Parameters ----------------------------------------
runtime="1 10 60"
benchmarkType="kv db os"
iterations=10

kvServer="lmdb leveldb rocksdb"
kvClient="mongodb sqlite "

dbClient="sqlite mariadb"

dbClientFile="/home/urz/kduwe/thesis_eval/results-jbench/${benchmarkType}/${benchmarkType}-${dbClient}-${SLURM_JOBID}.tsv"

kvClientFile="/home/urz/kduwe/thesis_eval/results-jbench/${benchmarkType}/${benchmarkType}-${kvClient}-${SLURM_JOBID}.tsv"



# ---------------- Cluster Setup ----------------------------------------

. /home/urz/kduwe/original-julea/scripts/environment.sh
echo ". /home/urz/kduwe/original-julea/scripts/environment.sh"


# ---------------- KV ---
for server in $kvServer
do 
    # config call
    julea-config --user \
    --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
    --object-backend=posix --object-component=server --object-path="/tmp/julea-$(id -u)/posix" \
    --kv-backend=${server} --kv-component=server --kv-path="/tmp/julea-$(id -u)/${server}" \
    --db-backend=sqlite --db-component=server --db-path="/tmp/julea-$(id -u)/sqlite"
            
    echo "julea-config --user \
    --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
    --object-backend=posix --object-component=server --object-path="/tmp/julea-$(id -u)/posix" \
    --kv-backend=${server} --kv-component=server --kv-path="/tmp/julea-$(id -u)/${server}" \
    --db-backend=sqlite --db-component=server --db-path="/tmp/julea-$(id -u)/sqlite""
        
    for time in $runtime
    do 
        # ---------------- Output ----------------------------------------
        #  results-jbench/kv/kv-lmdb-jobid.tsv
        kvServerFile="/home/urz/kduwe/thesis_eval/results-jbench/${benchmarkType}/${benchmarkType}-${kvServer}-${SLURM_JOBID}.tsv"

   

        echo "# Runtime = $time" >> $kvServerFile
        for iteration in $iterations
        do
            echo "# Iteration = $iteration" >> $kvServerFile
            # benchmark call
            # ./scripts/benchmark.sh -p /kv --duration=10 -v 2      
            ./scripts/benchmark.sh -p /kv --duration=$time -v 2  >> $kvServerFile
        done
    done
done