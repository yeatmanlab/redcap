# This script is to fix the data imported from NLR that doesn't have
# quality judgments. All quality will be set to 3 for NLR so that it is
# easily distinguishable from later data that has quality ratings for
# each run.

import pandas as pd
import numpy as np

# Import data
data = pd.read_csv('/Users/douglasstrodtman/Downloads/RDRPRepository_DATA_2017-03-20_1510.csv')

# Set up arrays of variable names
scores = ['wj_lwid_ss' , 'wj_wa_ss' , 'wj_pc_ss' , 'wj_or_ss' , 'wj_srf_ss' ,
'wj_mff_ss' , 'wj_calc_ss' , 'twre_swe_ss' , 'twre_pde_ss' ,
'wasi_block_ts' , 'wasi_vocab_ts' , 'wasi_mr_ts' , 'wasi_sim_ts' ,
'ctopp_elision_ss' , 'ctopp_bw_ss' , 'ctopp_pi_ss' , 'ctopp_md_ss' ,
'ctopp_nr_ss' , 'ctopp_rd_ss' , 'ctopp_rl_ss']

runs = ['wj_lwid_run' , 'wj_wa_run' , 'wj_pc_run' , 'wj_or_run' ,
'wj_srf_run' , 'wj_mff_run' , 'wj_calc_run' ,
'towre_swe_run' , 'towre_pde_run' , 'wasi_block_run' , 'wasi_vocab_run' , 'wasi_mr_run' , 'wasi_sim_run' , 'ctopp_elision_run' , 'ctopp_bw_run', 'ctopp_pi_run' , 'ctopp_md_run' , 'ctopp_nr_run' , 'ctopp_rd_run' ,
'ctopp_rl_run']

# Find fields that have scores in them, mark the runs as imported from NLR
for score in scores:
    for sub in data.index[pd.notnull(eval('data.{}'.format(score)))]:
        if pd.isnull(eval('data.{}'.format(runs[scores.index(score)]))[data.index[sub]]):
            data.loc[data.index==[sub], '{}'.format(runs[scores.index(score)])] = 3

# Set forms for imported data for WJ and TOWRE to X
data.loc[data.index[data.wj_lwid_run == 3], 'wj_form'] = 'X'
data.loc[data.index[data.towre_swe_run ==3], 'towre_form'] = 'X'

# Write out csv
data.to_csv('~/Downloads/nlr_fixed.csv')