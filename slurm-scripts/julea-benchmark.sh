#!/bin/bash

#SBATCH -N 1 
#SBATCH --partition=parcio
# SBATCH --error=/home/urz/kduwe/thesis_eval/output/benchmark-%j.err --output=/home/urz/kduwe/thesis_eval/output/benchmark-%j.out

# ---------------- Parameters ----------------------------------------
runtime="1 10 60"
iterations=10

kvServer="lmdb leveldb rocksdb"
kvClient="mongodb sqlite "

dbClient="sqlite mariadb"

# ---------------- Cluster Setup ----------------------------------------
export JULEA_PREFIX="/home/urz/kduwe/julea-install"

. /home/urz/kduwe/original-julea/scripts/environment.sh
echo ". /home/urz/kduwe/original-julea/scripts/environment.sh"


# ---------------- KV ---
for server in $kvServer
do 
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
        kvServerFile="/home/urz/kduwe/thesis_eval/results-jbench/kv/kv-${server}-$(hostname)-${SLURM_JOBID}.tsv"

        echo " " >> "${kvServerFile}"
        echo "# Runtime = $time" >> "${kvServerFile}"
        
        # for iteration in $iterations
        for ((it = 0; it < $iterations; it++))
        do
            echo "# Iteration = $it" >> "${kvServerFile}"  
            julea-server &

            /home/urz/kduwe/original-julea/scripts/benchmark.sh -p /kv --duration=$time -v 2 -m  >> "${kvServerFile}"

            killall julea-server
            rm -rf /tmp/julea-$(id -u)
        done
    done
done