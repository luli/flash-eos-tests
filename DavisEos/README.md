# Davis-Guardone (DG) tests for a non-convex EoS with the FLASH code

This folder contains the Davis-Guardone (DG) tests for the FLASH code using a non-convex EoS, discussed in further details in section 3.3.2 of the PhD thesis by Yurchak (2015). 

### Creating the EoS table

(optional) The `eos-vdv-davis.cn4` table containing the Van der Waals EoS for this test can be generated with:

    python make_table.py

this requires [`pyEOSPAC`](https://github.com/luli/pyeospac) and the LULI fork of [`opacplot2`](https://github.com/luli/opacplot2).


### Setting up and running the tests


The Davis-Guardone tests `DG1`, `DG2`, `DG3` can be setup in 1D with,

    bash setup1D.sh
    EOS_TEST=DG1 bash run1D.sh

this requires `flmake`.


Similarly one can setup and run the 2D test cases with:

    bash setup2D.sh
    EOS_TEST=DG1 bash run2D.sh


### Analysis of the results

The simulation output are parsed with `yt` and compared with the reference solution under `./data/DenseGas1DCases/` with,

    cd yt-viz/
    EOS_TEST=DG1 python analyse_vdw.py

