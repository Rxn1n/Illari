"""Reproduce the ILLARI October 2026 NISAR case from two GCOVs or four dB GeoTIFFs."""
import argparse
import json
import tempfile
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

GRANULES = {
    "20261007": "NISAR_L2_PR_GCOV_032_112_D_090_4005_DHDH_A_20261007T233944_20261007T234018_P05023_N_F_J_001",
    "20261019": "NISAR_L2_PR_GCOV_033_112_D_090_4005_DHDH_A_20261019T233944_20261019T234018_P05023_N_F_J_001",
}
BANDS = {"HH": "HHHH", "HV": "HVHV"}
ROWS, COLS = 1327, 1335
EPSG = 32717
TRANSFORM = from_origin(615650, 9766740, 10, 10)
# Half-open ranges counted from the northwestern corner of the crop.
EXAMPLE = np.s_[400:450, 450:500]
NODATA = -9999.0


def read_gcov(path, granule_id):
    import h5py

    with h5py.File(path, "r") as file:
        actual = file["/science/LSAR/identification/granuleId"][()].decode()
        if actual != granule_id:
            raise ValueError(f"Unexpected GCOV granule: {actual}")
        grid = file["/science/LSAR/GCOV/grids/frequencyA"]
        if int(grid["projection"][()]) != EPSG:
            raise ValueError("Expected WGS 84 / UTM zone 17S")
        # GCOV coordinates denote pixel centers; the GeoTIFF origin denotes a corner.
        x, y = grid["xCoordinates"][:], grid["yCoordinates"][:]
        x0 = TRANSFORM.c + TRANSFORM.a / 2
        y0 = TRANSFORM.f + TRANSFORM.e / 2
        col = int(np.argmin(abs(x - x0)))
        row = int(np.argmin(abs(y - y0)))
        window = np.s_[row:row + ROWS, col:col + COLS]
        if not (np.array_equal(x[col:col + COLS], x0 + 10 * np.arange(COLS))
                and np.array_equal(y[row:row + ROWS], y0 - 10 * np.arange(ROWS))):
            raise ValueError("Crop and GCOV pixel centers do not coincide")
        mask = grid["mask"][window]
        output = {}
        for pol, band in BANDS.items():
            power = grid[band][window].astype("float32")
            valid = (mask > 0) & (mask < 255) & np.isfinite(power) & (power > 0)
            db = np.full(power.shape, np.nan, dtype="float32")
            db[valid] = 10 * np.log10(power[valid])
            output[pol] = db
        return output


def read_tiffs(folder, date):
    output = {}
    for pol, band in BANDS.items():
        path = folder / f"GCOV_{date}_{band}_dB.tif"
        with rasterio.open(path) as image:
            if (image.crs is None or image.crs.to_epsg() != EPSG or image.count != 1
                    or (image.height, image.width) != (ROWS, COLS)
                    or image.transform != TRANSFORM):
                raise ValueError(f"Unexpected CRS, dimensions, band count or pixel grid: {path}")
            output[pol] = image.read(1, masked=True).astype("float32").filled(np.nan)
    return output


def statistics(delta):
    values = delta[np.isfinite(delta)]
    if not values.size:
        raise ValueError("No valid paired pixels")
    return {"valid_pixels": int(values.size), "median_delta_db": float(np.median(values))}


def write_band(path, delta):
    with rasterio.open(path, "w", driver="GTiff", height=ROWS, width=COLS, count=1,
                       dtype="float32", crs=f"EPSG:{EPSG}", transform=TRANSFORM,
                       nodata=NODATA, compress="deflate", predictor=3) as image:
        image.write(np.where(np.isfinite(delta), delta, NODATA), 1)
        image.set_band_unit(1, "dB")
        image.update_tags(before=GRANULES["20261007"], after=GRANULES["20261019"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--gcov-dir", type=Path, help="Directory containing both original .h5 files")
    source.add_argument("--tiff-dir", type=Path, help="Directory containing all four dB GeoTIFF crops")
    parser.add_argument("--out", type=Path, required=True, help="New directory for output rasters and JSON")
    args = parser.parse_args()
    if args.out.exists():
        parser.error(f"Output directory already exists: {args.out}")
    scenes = {}
    for date, granule in GRANULES.items():
        if args.gcov_dir is not None:
            scenes[date] = read_gcov(args.gcov_dir / (granule + ".h5"), granule)
        else:
            scenes[date] = read_tiffs(args.tiff_dir, date)

    results = {"granules": GRANULES, "input": "GCOV" if args.gcov_dir else "GeoTIFF_dB",
               "crs": "EPSG:32717", "size_pixels": [COLS, ROWS],
               "example_window": {"rows_half_open": [400, 450], "columns_half_open": [450, 500]},
               "bands": {}}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.out.parent) as temp:
        stage = Path(temp) / "results"
        stage.mkdir()
        for pol in BANDS:
            delta = scenes["20261019"][pol] - scenes["20261007"][pol]
            results["bands"][pol] = {"crop": statistics(delta), "example": statistics(delta[EXAMPLE])}
            write_band(stage / f"delta_{pol}_dB.tif", delta)
        report = json.dumps(results, indent=2, allow_nan=False)
        (stage / "results.json").write_text(report + "\n", encoding="utf-8")
        stage.rename(args.out)
    print(report)


if __name__ == "__main__":
    main()
