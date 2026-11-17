"""Per-superpixel monochromatic flat response for LSSTCam science detectors.

Writes one parquet file per detector to data/monochromatic_qe/<scan>/, indexed by
superpixel (xd, yd) with one column per wavelength in nm.

    python python/monochromatic_qe.py none
    python python/monochromatic_qe.py u
"""

import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd
from lsst.daf.butler import Butler

COLLECTIONS = {
    "none": "u/erykoff/LSSTCam/calib/DM-52142/monochromatic-none-scan-0520/monochromaticQEGen.20260521a",
    "u": "u/erykoff/LSSTCam/calib/DM-52142/monochromatic-u-scan-0520/monochromaticQEGen.20260521a",
}

parser = argparse.ArgumentParser()
parser.add_argument("scan", choices=COLLECTIONS)
parser.add_argument("--repo", default="embargo")
args = parser.parse_args()

out_dir = Path(__file__).resolve().parents[1] / "data" / "monochromatic_qe" / args.scan
out_dir.mkdir(parents=True, exist_ok=True)

butler = Butler(args.repo)
refs = butler.query_datasets(
    "cpMonochromaticFlatBinned",
    collections=[COLLECTIONS[args.scan]],
    where="instrument = 'LSSTCam' AND detector.purpose = 'SCIENCE'",
    limit=None,
)

refs_by_detector = defaultdict(list)
for ref in refs:
    refs_by_detector[ref.dataId["detector"]].append(ref)

for detector, det_refs in sorted(refs_by_detector.items()):
    frames = []
    for ref in det_refs:
        binned = butler.get(ref, parameters={"strip_astropy_meta_yaml": False})
        frame = binned["xd", "yd", "value"].to_pandas()
        frame["wavelength"] = binned.meta["wavelength"]
        frames.append(frame)

    curves = pd.concat(frames).pivot_table(index=["xd", "yd"], columns="wavelength", values="value")
    curves.rename(columns=str).to_parquet(out_dir / f"detector_{detector:03d}.parquet")
    print(f"detector {detector}: {len(curves)} superpixels, {curves.shape[1]} wavelengths", flush=True)
