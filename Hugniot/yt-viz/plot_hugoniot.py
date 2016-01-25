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
from eospac.rh import RankineHugoniot
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
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
from glob import glob

import yt.mods

df = {'IONMIX, FLASH': pd.read_hdf('hugoniot_al-imx-003.h5', 'df'),
      'FEOS, FLASH': pd.read_hdf('hugoniot_Al_feos_83719_eoffset_-2.h5', 'df')


}

plot_pars = {'IONMIX, FLASH': {'marker': 'o', 'ms': 4.5, 'color': 'r'},
             'FEOS, FLASH': {'marker': 'd', 'ms': 4.5, 'color': 'g'},
             'ref': {'color':'k', 'ls': 'solid'}}
for key in df:
    df[key] = df[key].sort(columns='temp_source')

df['IONMIX, FLASH'].drop_duplicates(inplace=True)
df['FEOS, FLASH'].drop_duplicates(subset='temp_source', inplace=True)

eos_pars = {'.*': {'linear': True}}
matid = 83719
matf = eos.EosMaterial(matid, tables=['Piz_DT', 'Uiz_DT', 'Pe_DT', 'Ue_DT', 'Zfc_DT'],
                options=eos_pars,
                units='eospac', backend='eospac')

state0 = {"temp": 298, "rho": 2.7}
state1 = {"pres": np.logspace(-0.2, 2.2, 100)*100}  # GPa

rh = RankineHugoniot.solve(state0, state1, backend='eospac',
                        eos_pars=eos_pars, material=matid,
                                        root_opts={'method': 'lm'})


fig = plt.figure(figsize=get_figsize(wf=1.1, hf=0.6))
plt.subplots_adjust(wspace=0.3, hspace=0.3)
ax = [plt.subplot(221), plt.subplot(222), plt.subplot(223), plt.subplot(224)]
axins2 = inset_axes(ax[2], width="15%", height='12%', loc=4,
                 bbox_to_anchor=(-0.553, 0.13, 1, 1), bbox_transform=ax[2].figure.transFigure) # no zoom
axins1 = inset_axes(ax[1], width="15%", height='12%', loc=2,
                 bbox_to_anchor=(0.623, -0.12, 1, 1), bbox_transform=ax[1].figure.transFigure) # no zoom

for key, idf in df.iteritems():
    ax[0].plot(idf.temp_source, idf.pres_0/100,'--', **plot_pars[key])
    ax[1].plot(idf.pres_0/100, idf.u_s, '--',  **plot_pars[key])
    axins1.plot(idf.pres_0/100, idf.u_s, '--',  **plot_pars[key])
    ax[2].plot(idf.pres_0/100, idf.tion_0, '--',  **plot_pars[key])
    axins2.plot(idf.pres_0/100, idf.tion_0, '--', **plot_pars[key])
    ax[3].plot(idf.velx_0, idf.u_s, '--', label='{0}'.format(key), **plot_pars[key])
ax[1].plot(rh.pres1/100, rh.u_s,   **plot_pars['ref'])
axins1.plot(rh.pres1/100, rh.u_s,   **plot_pars['ref'])

axins1.set_xlim(11,22)
axins1.set_ylim(22,33)
axins1.xaxis.set_ticks([12, 16, 20])
axins1.yaxis.set_ticks([24,28, 32])


axins2.set_xlim(11,22)
axins2.set_ylim(4,24)
axins2.xaxis.set_ticks([12, 16, 20])
for axins in [axins1, axins2]:
    for tick in axins.xaxis.get_major_ticks():
        tick.label.set_fontsize(7)
    for tick in axins.yaxis.get_major_ticks():
        tick.label.set_fontsize(7)




mark_inset(ax[2], axins2, loc1=1, loc2=3, fc="none", ec="0.5")
mark_inset(ax[1], axins1, loc1=1, loc2=3, fc="none", ec="0.5")


plim = (2e-1, 250)

ax[2].plot(rh.pres1/100, rh.temp1/11640.,  **plot_pars['ref'])
axins2.plot(rh.pres1/100, rh.temp1/11640., **plot_pars['ref'])

idf = df['FEOS, FLASH']

ax[3].plot(rh.u_p, rh.u_s, label='FEOS: steady state',**plot_pars['ref'])

ax[3].legend(loc=4)
for idx, lbl in enumerate(['a', 'b', 'c', 'd']):
    ax[idx].text(0.07, 0.90, '({})'.format(lbl), ha='center', va='center', transform=ax[idx].transAxes)

ax[0].set_xlabel('Source temperature [eV]')
ax[0].set_ylabel('Shock pressure [MBar]')
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlim(4,400)
ax[0].set_ylim(*plim)


ax[1].set_xlabel('Shock pressure [MBar]')
ax[1].set_ylabel('Shock velocity [km/s]')
ax[1].set_xscale('log')

#ax[1].set_xscale('log')
ax[1].set_ylim(0, 115)
ax[1].set_xlim(*plim)
#ax[1].set_yscale('log')
ax[1].set_ylim(0, 115)

ax[2].set_xlim(*plim)
ax[2].set_yscale('log')
ax[2].set_xscale('log')
ax[2].set_xlabel('Shock pressure [MBar]')
ax[2].set_ylabel('Temperature [eV]')

ax[3].set_xlim(0,95)
ax[3].set_xlim(0,75)
ax[3].set_xlabel('Particle velocity [km/s]')
ax[3].set_ylabel('Shock velocity [km/s]')

fig.savefig('hugoniot_dynamics.pdf', bbox_inches='tight')




