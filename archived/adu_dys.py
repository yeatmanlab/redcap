import pandas as pd
import numpy as np


# load data
data = pd.read_csv('/Users/douglasstrodtman/Downloads/nlr.csv')

# select adult rows
adults = data[250:]

# build list of dyslexic adults
dys = adults[adults.TWRE_INDEX <= 90]
dys = dys.combine_first(adults[adults.TWRE_SWE_SS <= 90])
dys = dys.combine_first(adults[adults.TWRE_PDE_SS <= 90])
dys = dys.combine_first(adults[adults.CTOPP_PM <= 90])
dys = dys.combine_first(adults[adults.CTOPP_RAPID <= 90])

# extract unique subs
subs = pd.unique(dys.Subject)


# exclude teens and elders
exclude = np.array(['401_JB', '402_RB', 'NB249', '601_CC', '602_JK'])

adu_dys = dys

for sub in exclude:
	adu_dys = adu_dys[adu_dys.Subject != sub]
	


# select only the columns that are pertinent to the current evaluations
final = adu_dys.ix[:, ['Subject', 'Visit', 'TWRE_SWE_SS', 'TWRE_PDE_SS', 'TWRE_INDEX', 'CTOPP_PM', 'CTOPP_RAPID']]

final.to_csv('~/Downloads/adu_dys.csv')