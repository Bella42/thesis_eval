# Benchmark setup

runtime 1 10 60
backends 
wiederholung 10
benchmark-typ os,kv,db, 
h5-stuff    h5-kv, h5-db, h5dai-kv, h5dai-db


## Option 1
for all db-backends
    for all kv-backends
        for all benchmark-types
            for all runtimes

                run benchmark 10 times

alle ergebnisse von mariadb mit lmdb für kv benchmark für alle 


## Option 2
for all benchmark-types
    for all db-backends
        for all kv-backends
            for all runtimes

                run benchmark 10 times


## Option 3 (winner)

### Standard Benchmark
kv benchmark
    for all kv-backends
        for all runtimes
            10 times

db benchmark
    for all db backends
        for all runtimes
            10 times

os benchmark
    for all os backends
        for all runtimes
            10 times

rest of benchmarked functions


### H5