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




## Configs & Notes

- 551444: runtime="1 10" runtimeDB="1 10 60" iterations=10 kvServer="lmdb leveldb rocksdb sqlite sqlite-memory" dbClient="sqlite mariadb" osServer="posix-local posix-ceph"