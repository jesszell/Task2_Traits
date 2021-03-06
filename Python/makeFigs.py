from __future__ import division
import os, re
import gomp as gp
#import gomp_death as gpd
import pandas as pd
import  matplotlib.pyplot as plt
from collections import Counter

mydir = os.path.expanduser("~/GitHub/Task2_Traits/")

def runAnalysis(gpd = False):
    raw_data = mydir + 'data/uMax/raw_data/'
    clean_data = mydir + 'data/uMax/clean_data/'
    for x in os.listdir(raw_data):
        if x == '.DS_Store':
            continue
        if x != 'Task2_48hr_48well_discon_180614_140037':
            continue
        path_IN = raw_data + x + '/' + x + '.txt'
        path_OUT = clean_data + x + '.txt'
        gp.cleanData(path_IN, path_OUT, wells = 48)
        #if gpd == True:
        #    gpd.modGompGrowth(path_OUT, smooth = True)
        #else:
        #    gp.modGompGrowth(path_OUT, smooth = True)



def getTransferTime(x):
    if x[1] == str(0):
        return 1
    elif x[1] == str(1):
        return 10
    elif x[1] == str(2):
        return 100

def mergeParams():
    params = mydir + 'data/uMax/params/'
    dfs = []
    for x in os.listdir(params):
        if x == '.DS_Store':
            continue
        params_IN = params + x
        IN = pd.read_csv(params_IN, sep = ' ')
        dfs.append(IN)

    dfs_merged = pd.concat(dfs, ignore_index = True)
    dfs_merged['TransferTime'] = dfs_merged['Sample'].apply(getTransferTime)
    dfs_merged['Strain'] = dfs_merged['Sample'].apply(lambda x: x[2])
    dfs_merged['Replicate'] = dfs_merged['Sample'].apply(lambda x: x[3])
    dfs_merged['Day'] = dfs_merged['Sample'].apply(lambda x: x[-3:])
    dfs_merged.to_csv(mydir + 'data/uMax/mergedParams.txt', sep = '\t', index = False)


def sample_summary():
    days = ['100', '200', '300', '400', '500']
    strains = ['B', 'C', 'D', 'F', 'J', 'P', 'S']
    transfers = ['0', '1', '2']
    reps = ['1', '2', '3', '4', '5']
    params = pd.read_csv(mydir + 'data/uMax/mergedParams.txt', sep = '\t')
    OUT = open(mydir + 'data/uMax/sample_summary.txt', 'w')
    count_reps =  dict(Counter(params.Sample.values))
    print>> OUT, 'Sample', 'Done'
    for day in days:
        for strain in strains:
            for transfer in transfers:
                for rep in reps:
                    sample = 'L' + transfer + strain + rep + '-' + day
                    if (sample in count_reps) and (count_reps[sample]) >= 3:
                        print>> OUT, sample, 'TRUE'
                    else:
                        print>> OUT, sample, 'FALSE'
    OUT.close()


runAnalysis()
#mergeParams()
#sample_summary()

#IN = pd.read_csv(mydir + 'data/uMax/mergedParams.txt', sep = '\t')
#IN = IN.loc[IN['Strain'] != 'S']
#IN_B = IN.loc[IN['Strain'] == 'B']
#print IN_B
#umax_mean = IN_B['umax'].groupby(IN_B['Sample']).mean().reset_index()
#umax_mean['TransferTime'] = umax_mean['Sample'].apply(getTransferTime)
#umax_mean['Strain'] = umax_mean['Sample'].apply(lambda x: x[2])
#umax_mean['Replicate'] = umax_mean['Sample'].apply(lambda x: x[3])
#umax_mean['Day'] = umax_mean['Sample'].apply(lambda x: x[-3:])
#umax_mean_100 = umax_mean.loc[umax_mean['Day'] == '100']


#A_mean = IN['A'].groupby(IN['Sample']).mean().values
#L_mean = IN['L'].groupby(IN['Sample']).mean().values
#print umax_mean_100
#fig = plt.figure()

#plt.scatter(umax_mean_100.TransferTime.values, umax_mean_100.umax.values, c='#87CEEB', marker='o', label='_nolegend_', s = 60)
#plt.title('100 day Pseudo', fontsize = 24)
#plt.xlabel('Transfer time', fontsize = 18)
#plt.ylabel('maximum growth rate', fontsize = 18)
#plt.xscale('log')
#fig_name = mydir + 'figs/P_umax.png'
#fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.close()

#fig = plt.figure()
#plt.scatter(x, A_mean, c='#87CEEB', marker='o', label='_nolegend_', s = 60)
#plt.title('100 day Janthino', fontsize = 24)
#plt.xlabel('Transfer time', fontsize = 18)
#plt.ylabel('Yield', fontsize = 18)
#plt.xscale('log')
#fig_name = mydir + 'figs/B_A.png'
#fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.close()


#fig = plt.figure()
#plt.scatter(x, L_mean, c='#87CEEB', marker='o', label='_nolegend_', s = 60)
#plt.title('100 day Janthino', fontsize = 24)
#plt.xlabel('Transfer time', fontsize = 18)
#plt.ylabel('Lag parameter (lambda)', fontsize = 18)
#plt.xscale('log')
#fig_name = mydir + 'figs/B_L.png'
#fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.close()
