import datetime
import numpy as np
import time
import pandas as pd

def handler(input, context):
    out = dict()
    timestamp = input['timestamp'][:19]
    out['timestamp'] = timestamp

    # the average utilization of each CPU
    CPUs = ['cpu_percent-0', 'cpu_percent-1', 'cpu_percent-2', 'cpu_percent-3']
    for CPU in CPUs:
        # last hour
        cpu_hr = context.env.get(CPU+'_hr', [])
        cpu_hr.append(input[CPU])
        if len(cpu_hr) > 12:
            cpu_hr.pop(0)
        out[f'avg-{CPU}-1hour'] = round(np.mean(cpu_hr), 2)
        context.env[CPU+'_hr'] = cpu_hr

        # last minute
        cpu_mi = context.env.get(CPU+'_mi', [])
        cpu_mi.append(input[CPU])
        if len(cpu_mi) > 720:
            cpu_mi.pop(0)
        out[f'avg-{CPU}-60sec'] = round(np.mean(cpu_mi), 2)
        context.env[CPU+'_mi'] = cpu_mi
    
    # the average utilization of each memory
    mem = context.env.get('memory_mi', [])
    mem.append(input['virtual_memory-percent'])
    if len(mem) > 12:
        mem.pop(0)
    out['avg-virtual_memory-60sec'] = round(np.mean(mem), 2)     
    context.env['memory_mi'] = mem

    return out