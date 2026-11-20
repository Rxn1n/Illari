# Reproduce the GCOV measurements / Reproducir las mediciones GCOV

[English guide](guide-en.md) · [Guía Spanish](README.md) · [Calculation script / Código](../../tools/reproduce_guayaquil.py)

## English

Run this calculation from the repository root to regenerate the two calibrated change maps. It reads small spatial windows from the two original HDF5 granules, or accepts four already extracted GeoTIFFs in dB. Downloading the originals from ASF DAAC requires Earthdata Login. Keep the published granule filenames, including the extension `.h5`.

- **2026-10-07** · [NISAR_L2_PR_GCOV_032_112_D_090_4005_DHDH_A_20261007T233944_20261007T234018_P05023_N_F_J_001](https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_032_112_D_090_4005_DHDH_A_20261007T233944_20261007T234018_P05023_N_F_J_001/NISAR_L2_PR_GCOV_032_112_D_090_4005_DHDH_A_20261007T233944_20261007T234018_P05023_N_F_J_001.h5)
- **2026-10-19** · [NISAR_L2_PR_GCOV_033_112_D_090_4005_DHDH_A_20261019T233944_20261019T234018_P05023_N_F_J_001](https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_033_112_D_090_4005_DHDH_A_20261019T233944_20261019T234018_P05023_N_F_J_001/NISAR_L2_PR_GCOV_033_112_D_090_4005_DHDH_A_20261019T233944_20261019T234018_P05023_N_F_J_001.h5)

Use a Python environment with NumPy, Rasterio and h5py. Put both HDF5 files in a local directory named `gcov`. Choose a new output directory for each run.

```sh
python -m pip install numpy rasterio h5py
python tools/reproduce_guayaquil.py --gcov-dir gcov --out results-h5
```

Alternatively, put `GCOV_20261007_HHHH_dB.tif`, `GCOV_20261007_HVHV_dB.tif`, `GCOV_20261019_HHHH_dB.tif` and `GCOV_20261019_HVHV_dB.tif` in a directory named `crops`. This option expects the exact study grid, co-registered and already expressed in dB.

```sh
python tools/reproduce_guayaquil.py --tiff-dir crops --out results-tiff
```

**Method.** Read `/science/LSAR/GCOV/grids/frequencyA/HHHH` and `HVHV` on the common grid, verify the granule ID, projection and pixel centres, and retain finite positive power where the original extraction mask is greater than 0 and less than 255. Compute `10 × log10(power)` at each date and subtract 7 October from 19 October at each valid paired cell. The reported medians use these differences before any smoothing, clipping or display resampling. This script reproduces the NISAR signal comparison. The separate [exploratory OPERA analysis](../../CASO_NISAR_OPERA_GUAYAQUIL.md) uses additional dates and classification rules.

[Reference results from the original GCOV pair / Resultados de referencia](gcov-results.json)

**Output.** Each run writes `delta_HH_dB.tif`, `delta_HV_dB.tif` and `results.json`. The GeoTIFFs use 10 m pixels, EPSG:32717, northwest corner (615650 E, 9766740 N), 1,335 columns and 1,327 rows. Box A uses zero-based columns 450–499 and rows 400–449. Its centre is (620400 E, 9762490 N). Both input routes were run on the original pair and its four dB subsets; the output rasters matched byte for byte in the tested environment.

| Area / Área | Paired cells / Celdas | HH median (dB) | HV median (dB) |
|---|---:|---:|---:|
| Urban crop / Recorte | 1,771,545 | +0.2297 | +0.1335 |
| Window / Ventana A | 2,500 | +0.6697 | +0.6441 |

## Spanish

Descarga los dos GCOV de ASF DAAC enlazados arriba con tu cuenta Earthdata. Conserva sus nombres originales y ubícalos en `gcov`. Desde la raíz del repositorio, ejecuta los dos comandos del primer bloque. Si ya tienes los cuatro GeoTIFF en dB, colócalos en `crops` y usa el segundo bloque. Elige una carpeta de salida nueva.

El programa verifica la identidad y la malla de los GCOV, selecciona las bandas HHHH y HVHV de frecuencia A y convierte la potencia válida a dB antes de restar las fechas. La ruta GeoTIFF comprueba la proyección, el tamaño y el alineamiento de las cuatro bandas. Los mapas resultantes conservan la resolución de 10 m. El informe JSON contiene las medianas del recorte y de la ventana A, elegida como ejemplo local. Las dos formas de cálculo produjeron los mismos rásteres en la verificación. La tabla anterior permite comprobar los valores antes del redondeo a dos decimales.

Para investigar la tormenta del 26 de octubre haría falta un intervalo distinto. Las dos observaciones de este análisis son anteriores.
