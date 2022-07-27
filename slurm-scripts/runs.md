# Final Runs

## JULEA Benchmark

### DB

### KV

### OS

### MISC



# Job List

JobID       Nodes       Final Run?      Script
-----------------------------------------------------------------------------------------------------

551444      ant11       ?              srun -p parcio -N 1 -w ant11 slurm-scripts/julea-benchmark.sh       
551449      ant11                      srun -p parcio -N 1 -w ant11 slurm-scripts/julea-benchmark.sh
551451      ant19                      srun -p parcio -N 1 -w ant19 slurm-scripts/julea-benchmark.sh
551452      ant11                      srun -p parcio -N 1 -w ant11 slurm-scripts/julea-benchmark.sh
551453      ant11                      sbatch -p parcio -w ant11 -N 1 thesis_eval/slurm-scripts/julea-benchmark.slurm 



## Configs & Notes

- 551444: runtime="1 10" runtimeDB="1 10 60" iterations=10 kvServer="lmdb leveldb rocksdb sqlite sqlite-memory" dbClient="sqlite mariadb" osServer="posix-local posix-ceph"

<!-- Everything on weaker node -->
- 551451: runtime="1 10" runtimeDB="1 10 60" iterations=10 kvServer="lmdb leveldb rocksdb sqlite sqlite-memory" dbClient="sqlite mariadb" osServer="posix-local posix-ceph"

<!-- Just measure db and following -->
- 551452: runtime="1 10" runtimeDB="1 10 60" iterations=10 kvServer="" dbClient="sqlite mariadb" osServer="posix-local posix-ceph"
<!-- Just measure db and following (fixed outputfile for duration in db)-->
- 551453: runtime="1 10" runtimeDB="1 10 60" iterations=10 kvServer="" dbClient="sqlite mariadb" osServer="posix-local posix-ceph"