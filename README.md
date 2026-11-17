# In-Band Slopes from LSST Broadband Photometry

This project recovers sub-band spectral information from LSST broadband photometry. LSSTCam's quantum efficiency varies across the focal plane by up to ±5–10% in u and g, so an object's measured magnitude shifts from visit to visit by an amount that depends on its SED shape within the band. Each passband is modeled as $S_{\rm std}(\lambda)\,[1 + \delta(\lambda, x)]$, with $\delta$ measured from monochromatic flats. Fitting the resulting mmag-level residuals across many visits yields a per-object in-band slope. The main challenge is detecting these residuals against roughly 5 mmag of u-band calibration noise in DP2.

## Goals

1. Produce u- and g-band slope estimates for the deep coadd object tables.
2. Test star–galaxy separation using DP2 cross-matched with Euclid Q1 morphologies.
3. Add in-band slope as a new feature for ML star–galaxy classifiers.
4. Assess any benefit for photometric redshifts and color-based deblending.

## Layout

* `notebooks/` analysis notebooks
* `python/` scripts (kept minimal)
* `data/` inputs and outputs (not tracked)
* `plots/` figures (not tracked)

## Monochromatic QE curves

`python/monochromatic_qe.py` reads the binned monochromatic flats (`cpMonochromaticFlatBinned`, DM-52142) for all LSSTCam science detectors and writes one table per detector to `data/monochromatic_qe/<scan>/`, with superpixels as rows and wavelengths (nm) as columns. Run once per scan at S3DF with the LSST stack set up:

```bash
python python/monochromatic_qe.py none
python python/monochromatic_qe.py u
```

Values are not yet normalized across the focal plane; that code is still pending.
