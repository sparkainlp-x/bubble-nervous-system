# Bubble Nervous System — Public Reproducibility and Release Guide

This guide describes the reproducibility checks and public-release requirements for **Bubble Nervous System v0.1.0**. It is suitable for inclusion in a public repository. It does not contain private operational instructions.

## Source and version

Use the release archive for **bubble-nervous-system v0.1.0** and verify that the package directory is `bubble-nervous-system/`.

Do not mix files from older archives, drafts, or exports. The release should be built from one clean extraction of the v0.1.0 archive.

## Repository contents

The package includes the vendored files `nervous.py`, `human.py`, `injection.py`, and `LICENSE`, together with the project files `bubble.py`, `observer.py`, `calibrator.py`, `sweep.py`, `optimizer.py`, `passport.py`, `demo.py`, `tests.py`, `PREREG.md`, `README.md`, `DESIGN.md`, `CITATION.cff`, and `.zenodo.json`.

Do not add, remove, or rename files as part of the v0.1.0 release unless the release documentation is updated accordingly.

## Reproducibility checks

From a clean extraction of the archive, in the package directory, run:

```bash
python3 -m unittest tests -v
python3 demo.py
```

The expected test result is **12/12 tests passing**, with no failures and no skipped tests.

The demo should reproduce the documented v0.1.0 results, including the frozen-gate values, observer routing values, frequency acceptance values, injection comparison, and the calibration review/signoff behavior described in `README.md` and `DESIGN.md`.

The documented sweep and optimizer results must also match the release documentation. In particular, the optimizer result must be described accurately as a degenerate equivalent point, not as an improvement over the frozen gate.

If any documented result differs, stop the release and investigate the discrepancy rather than changing code, guards, thresholds, or measured values solely to make a test pass.

## Credits and attribution

Credit the project author and any inspirations exactly as specified in `README.md`, `CITATION.cff`, and `.zenodo.json`. Do not add authorship claims, credentials, or affiliations that are not supported by the project metadata.

Private or unpublished work must not be imported, named, or linked in the public repository unless its owner has explicitly authorized public disclosure.

## License and archival release

The repository should use the **AGPL-3.0-only** license. Verify that the `LICENSE` file begins with the GNU Affero General Public License v3 text.

Before creating a version tag, verify that the archival metadata is configured correctly. The Zenodo metadata must identify the correct creators, title, version, and license. The license field should use the SPDX identifier `AGPL-3.0-only` in the format required by Zenodo.

After tagging, verify the resulting archive and DOI metadata. If a DOI is added to project files, update only the designated citation and README fields, and do not create a second release merely to correct metadata.

## Public limitations

Keep these limitations visible in every public-facing project description:

- This is not a human nervous system, neuroscience study, medical device, diagnosis, or measurement of any real person.
- It is a synthetic classical toy model.
- Calibration improves the assumed model; it does not establish facts about a true biological or physical system.
- The reported injection result at sigma 0.30 and 7 Hz is negative and should remain visible in the record.
- A lesion that breaks the reflex route is a graph property of the toy model, not a claim about real lesions.
- Results are based on synthetic, observer-reported data only.

## Public release checklist

- [ ] Build from a clean v0.1.0 archive.
- [ ] Confirm all expected files are present.
- [ ] Run the unit tests and confirm 12/12 passing.
- [ ] Run the demo and compare results with the release documentation.
- [ ] Confirm the optimizer result is not presented as an improvement.
- [ ] Verify the AGPL-3.0-only license and attribution metadata.
- [ ] Verify archival metadata before tagging.
- [ ] Verify the DOI and archived metadata after tagging.
- [ ] Confirm that no private or unpublished material is included.
- [ ] Confirm that all public claims include the limitations above.
