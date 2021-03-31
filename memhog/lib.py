#!/usr/bin/env python
import os
import resource
import time


def allocate(length):
    print('Allocating chunk... ', end='', flush=True)
    x = list(range(length))
    print('done.')
    return x


def get_current_rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def pretty_mem(kb):
    return '{:d} MiB'.format(round(kb / 1024.0))


def total_system_memory_bytes():
    """Get total system physical memory in bytes. Linux only."""
    return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')


def chunk_size_for_system(total_mem_mb=None):
    if total_mem_mb is None:
        total_mem_mb = total_system_memory_bytes() / 1024.0 / 1024.0
    # Using arrays that are 150x the system memory in MB by experiment appears
    # to result in each chunk being about 0.6% of the total system memory.
    return round(total_mem_mb * 150)


def hog_memory(interval=0.1, interactive=False, cap=None, chunk_length=None,
               total_mem=None):
    db = []
    if chunk_length is None:
        chunk_length = chunk_size_for_system(total_mem_mb=total_mem)
    print('Memhog starting up, PID:', os.getpid())
    print('Using chunks of length:', chunk_length)

    while True:
        db.append(allocate(chunk_length))
        print('Chunks total:', len(db))
        mem = get_current_rss()
        print('Memory used:', pretty_mem(mem))
        if cap and mem / 1024.0 >= cap:
            print('Reached memory cap, sleeping forever...')
            while True:
                time.sleep(86400)
        if interactive:
            input('Press enter to continue...')
        else:
            time.sleep(interval)



"""
p = optparse.OptionParser(usage='%prog [options]\n'+__doc__.rstrip(),
                  version='%prog ' + VERSION)
p.add_option('-c', '--cap', dest='cap', metavar='MB', type='int',
     default=512, help='Maximum memory to allocate, default 512')
p.add_option('-u', '--unlimited', dest='cap', action='store_const',
     const=False, help='Place no limit on allocated memory')
p.add_option('-w', '--wait', dest='interval', metavar='SEC',
     help='time to sleep between chunk allocations',
     type='float', default=0.1)
p.add_option('--sys-total-mem', dest='total_mem', metavar='MB',
     type='int', help='set total mem used to infer chunk size')
p.add_option('-i', '--interactive', dest='interactive',
     action='store_true', help='Prompt between chunk allocations')
p.add_option('-l', '--chunk-length', dest='chunk_length', metavar='LEN',
     type='int', help='set length of chunk array')

opts, args = p.parse_args()
"""
