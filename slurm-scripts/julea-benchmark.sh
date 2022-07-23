#!/bin/bash

#SBATCH -N 1 
#SBATCH --partition=parcio
# SBATCH --error=/home/urz/kduwe/thesis_eval/output/benchmark-%j.err --output=/home/urz/kduwe/thesis_eval/output/benchmark-%j.out

# ---------------- Parameters ----------------------------------------
runtime="1 10"
# runtime="1 10 60"
iterations=1
# iterations=10

kvServer="lmdb leveldb rocksdb sqlite sqlite-memory"
# kvClient="mongodb sqlite"

dbClient="sqlite mariadb"

# ---------------- Cluster Setup ----------------------------------------
export JULEA_PREFIX="/home/urz/kduwe/julea-install"

. /home/urz/kduwe/mein-julea/scripts/environment.sh
echo ". /home/urz/kduwe/mein-julea/scripts/environment.sh"
# echo ". /home/urz/kduwe/original-julea/scripts/environment.sh"

spack load mysql

mkdir -p /tmp/kduwe/localdb

singularity run --writable-tmpfs -B /tmp/kduwe/localdb:/var/lib/mysql --env MARIADB_RANDOM_ROOT_PASSWORD=yes --env MARIADB_DATABASE=julea_db --env MARIADB_USER=julea_user --env MARIADB_PASSWORD=julea_pw  mariadb.sif &


# ---------------- KV Server ---
for server in $kvServer
do 

    if [ "${server}" == "sqlite-memory" ];
    then
         julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=sqlite --kv-component=server --kv-path=":memory:" \
        --db-backend=sqlite --db-component=server --db-path="/tmp/julea-${SLURM_JOBID}/sqlite-db"

        echo "julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=sqlite --kv-component=server --kv-path=":memory" \
        --db-backend=sqlite --db-component=server --db-path="/tmp/julea-${SLURM_JOBID}/sqlite-db""
    else
        julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=${server} --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/${server}" \
        --db-backend=sqlite --db-component=server --db-path="/tmp/julea-${SLURM_JOBID}/sqlite-db"

        echo "julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=${server} --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/${server}" \
        --db-backend=sqlite --db-component=server --db-path="/tmp/julea-${SLURM_JOBID}/sqlite-db""
    fi
    

    for time in $runtime
    do 
        # ---------------- Output ----------------------------------------
        #  results-jbench/kv/kv-lmdb-jobid.tsv
        kvServerFile="/home/urz/kduwe/thesis_eval/results-jbench/kv/kv-${server}-$(hostname)-${SLURM_JOBID}.tsv"

        echo "${kvServerFile}"

        echo " " >> "${kvServerFile}"
        echo "# Runtime = $time" >> "${kvServerFile}"
        
        # for iteration in $iterations
        for ((it = 0; it < $iterations; it++))
        do
            echo "Runtime = $time    Iteration = $it"
            echo " " >> "${kvServerFile}" 
            echo "# Iteration = $it" >> "${kvServerFile}"  
            julea-server &

            /home/urz/kduwe/original-julea/scripts/benchmark.sh -p /kv --duration=$time -v 2 -m  >> "${kvServerFile}"

            killall julea-server
            rm -rf /tmp/julea-${SLURM_JOBID}
        done
    done
done

# # ---------------- KV Server ---
# for server in $kvClient
# do 
#     if [ "${server}" == "mongodb" ];
#     then
#         # julea-config --user \
#         # --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
#         # --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
#         # --kv-backend=${server} --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/${server}" \
#         # --db-backend=sqlite --db-component=server --db-path=":memory:"

#         # echo "julea-config --user \
#         # --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
#         # --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
#         # --kv-backend=${server} --kv-component=client --kv-path="/tmp/julea-${SLURM_JOBID}/${server}" \
#         # --db-backend=sqlite --db-component=server --db-path=":memory:""
#     else

#     fi
        
#     for time in $runtime
#     do 
#         # ---------------- Output ----------------------------------------
#         #  results-jbench/kv/kv-lmdb-jobid.tsv
#         kvServerFile="/home/urz/kduwe/thesis_eval/results-jbench/kv/kv-${server}-$(hostname)-${SLURM_JOBID}.tsv"

#         echo " " >> "${kvServerFile}"
#         echo "# Runtime = $time" >> "${kvServerFile}"
        
#         # for iteration in $iterations
#         for ((it = 0; it < $iterations; it++))
#         do
#             echo " " >> "${kvServerFile}"  
#             echo "# Iteration = $it" >> "${kvServerFile}"  
#             julea-server &

#             /home/urz/kduwe/original-julea/scripts/benchmark.sh -p /kv --duration=$time -v 2 -m  >> "${kvServerFile}"

#             killall julea-server
#             rm -rf /tmp/julea-${SLURM_JOBID}
#         done
#     done
# done

# ---------------- DB ---
for server in $dbClient
do 
    if [ "${server}" == "sqlite" ];
    then
        julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=leveldb --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/leveldb" \
        --db-backend=${server} --db-component=server --db-path=":memory:"
            
        echo " julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=leveldb --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/leveldb" \
        --db-backend=${server} --db-component=server --db-path=":memory:""
    else
         julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=leveldb --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/leveldb" \
        --db-backend=${server} --db-component=client --db-path="/tmp/kduwe/localdb:julea_db:julea_user:julea_pw"
        # --db-backend=${server} --db-component=client --db-path="$(hostname):julea_db:root"

        echo "julea-config --user \
        --object-servers="$(hostname)" --kv-servers="$(hostname)" --db-servers="$(hostname)" \
        --object-backend=posix --object-component=server --object-path="/tmp/julea-${SLURM_JOBID}/posix" \
        --kv-backend=leveldb --kv-component=server --kv-path="/tmp/julea-${SLURM_JOBID}/leveldb" \
        --db-backend=${server} --db-component=client --db-path="/tmp/kduwe/localdb:julea_db:julea_user:julea_pw""
    fi
    
        
    for time in $runtime
    do 
        # ---------------- Output ----------------------------------------
        #  results-jbench/kv/kv-lmdb-jobid.tsv
        dbServerFile="/home/urz/kduwe/thesis_eval/results-jbench/db/db-${server}-$(hostname)-${SLURM_JOBID}.tsv"

         echo "${dbServerFile}"
        echo " " >> "${dbServerFile}"
        echo "# Runtime = $time" >> "${kvServerFile}"
        
        # for iteration in $iterations
        for ((it = 0; it < $iterations; it++))
        do
            echo "Runtime = $time    Iteration = $it"
            echo " " >> "${dbServerFile}" 
            echo "# Iteration = $it" >> "${dbServerFile}"  
            julea-server &

            /home/urz/kduwe/original-julea/scripts/benchmark.sh -p /db --duration=$time -v 2 -m  >> "${dbServerFile}"

            killall julea-server
            rm -rf /tmp/julea-${SLURM_JOBID}
        done
    done
done