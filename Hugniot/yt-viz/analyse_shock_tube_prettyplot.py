#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./')
sys.path.append('../../../../')
import numpy as np
from figure_size import update_mpl_rc, get_figsize
update_mpl_rc({'backend': 'Agg'})
#update_mpl_rc({'backend': 'pgf'})
import eospac as eos
import matplotlib as mpl
from hedp.math.derivative import savgol
#print mpl.rcParams
#mpl.use('Agg')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         r'\usepackage{tikz}',
         r'\usepackage{pgfplots}'
         ]
}
mpl.rcParams.update(pgf_with_pdflatex)

from scipy.constants import N_A
import matplotlib.pyplot as plt
import os.path, os
from scipy.constants import physical_constants
eV2K_cst = physical_constants['electron volt-kelvin relationship'][0]
import pandas as pd

import yt.mods


units = {'pres': 1e10, 'pele': 1e10, 'pion': 1e10, 'prad': 1e10,
         'eint': 1e10, 'eele': 1e10, 'eion': 1e10, 'erad': 1e10,
         'temp': eV2K_cst, 'tele': eV2K_cst, 'tion': eV2K_cst, 'trad': eV2K_cst,
         'dens': 1., 'velx': 1e5}
#units = {'pres': 1, 'pele': 1, 'pion': 1, 'prad': 1,
#         'eint': 1, 'eele': 1, 'eion': 1, 'erad': 1,
#         'temp': eV2K_cst, 'tele': eV2K_cst, 'tion': eV2K_cst, 'trad': eV2K_cst,
#         'dens': 1.}

def get_state(r, x0, dx=2e-4):
    states = []
    for sidx in range(2):
        x_vect  = r['x'] - (x0 + np.sign((sidx - 0.5))*dx)
        if x_vect.max()*x_vect.min()<0:
            # there is a solution
            solution = 1.0
        else:
            solution = np.nan
        ridx = np.argmin(np.abs(x_vect))
        states.append({key: solution*r[key][ridx]/units[key] for key in  units.keys()})
    return pd.DataFrame(states)


def eos_check_consistency(s, mat):
    print 'dens: {0:.3e}  tele: {1:.3e}  tion: {2:.3e}'.format(s['dens'], s['tele'], s['tion'])
    for Ylbl, Flbl, Ftab in [( 'tele', 'pele', 'Pe_DT'),
                             ( 'tion', 'pion', 'Piz_DT'),
                             ( 'tele', 'eele', 'Ue_DT'),
                             ( 'tion', 'pion', 'Uiz_DT'),
                             ]:
        Fval1 = s[Flbl]
        Fval2 =  mat.get_table(Ftab)(s['dens'], s[Ylbl]*eV2K_cst)
        print  '{0:6} | {1:.3e} {2:.3e} {3}'.format(Ftab, Fval1, float(Fval2), np.allclose(Fval1, Fval2, rtol=1e-3))

def get_shock_position(d):
    if (d['pres'].max() - d['pres'].min())/d['pres'].mean() < 0.2:
        return np.nan
    else:
        idx = np.nanargmin(savgol( d['x'], d['pres'], window_size=5, order=2, deriv=1))
        return d['x'][idx]

matf = eos.EosMaterial(83719, tables=['Piz_DT', 'Uiz_DT', 'Pe_DT', 'Ue_DT', 'Zfc_DT'],
                options={'.*': {'linear': True}},
                units='eospac', backend='eospac')

feosid = 83719
material = 'Al'

feos_opts ={'use_maxwell': True, 'use_softspheres': True,
                'maxwell_temp_arr': None, 'max_materials': 2,
                        'grid_subsample_default': 0}

#mat2 = eos.EosMaterial(3719, tables=['Piz_DT', 'Uiz_DT', 'Pe_DT', 'Ue_DT', 'Zfc_DT'],
#              options=feos_opts,
#                    units='cgs', backend='feos')



RUN_NAME = os.environ['SOURCE_TEMP']
EOS_TABLE = os.environ['EOS_TABLE']
FNAME = "../frun_{0}/solidhugoniot_hdf5_chk_{1}"

res = {}


pf = yt.mods.load(FNAME.format(RUN_NAME, '0000')) 
r0 = pf.h.ortho_ray(0, (0, 0))
state0 =  get_state(r0, 1e-4, 0.5e-4)
res = {'temp_source': state0.tele[0]}

print 'Using eospac tables...'
for idx in range(2):
    eos_check_consistency(state0.ix[idx], matf)
print '='*80 +'\n'

storage = {}
ts = yt.mods.TimeSeriesData.from_filenames(FNAME.format(RUN_NAME, '*'), parallel = False)
for sto, pf in ts.piter(storage=storage):
    sl = pf.h.ortho_ray(0, (0, 0))
    t = pf.current_time*1e9
    x_s = get_shock_position(sl)
    vals = get_state(sl, x_s)
    state0 = vals.ix[0]
    state1 = vals.ix[1]
    state0['t'] = t
    state1['t'] = t
    state0['x'] = x_s
    state1['x'] = x_s
    sto.result = (state0, state1)#t, get_shock_position(sl), get_state(r0, 10e-4))
#t,x = np.array(storage.values()).T
state0 = []
state1 = []
for val0, val1 in storage.values():
    state0.append(val0)
    state1.append(val1)

df0 = pd.DataFrame(state0)
df1 = pd.DataFrame(state1)


fig = plt.figure(figsize=get_figsize(wf=0.5, hf=0.5))
ax = [plt.subplot(111)]

for dfi in [df0,df1]:
    dfi['u_s'] = savgol(np.array(dfi['t']), np.array(dfi['x']), window_size=5, order=2, deriv=1)*1e4
ax[0].plot(df0['t'],df0['x']*1e4, 'k')

ax[0].set_xlabel('Time (t) [ns]')
ax[0].set_ylabel('Shock position (x) [$\mathrm{\mu m}$]')
ax[0].xaxis.set_ticks([0, 1, 2, 3])
ax[0].yaxis.set_ticks([0, 30, 60, 90])
ax[0].set_xlim(0, 3)
ax[0].set_ylim(0, 90)
ax[0].grid(which='both')

fig.savefig('hugoniot_{0}_{1}.pdf'.format(EOS_TABLE, RUN_NAME), bbox_inches='tight')
