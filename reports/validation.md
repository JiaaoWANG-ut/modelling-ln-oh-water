# Structure validation

24 structures, 0 failed checks, 0 warnings

## Dy box/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Dy | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.230 - 2.370` |  | target OH 2.23 / H2O 2.37 |
| nearest 2nd-shell O (A) | `4.129` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.944` |  |  |
| OH-...OH- O-O (A) | `2.711 3.833 4.212` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.711` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.909` | ok |  |
| H-bonds per solvent molecule | `2.05` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `52%` |  | 134 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0643` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.02752` | ok | 31 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.981` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1373` | ok |  |
| spin multiplicity | `6` | ok | 4f^9 high spin, 5 unpaired |
| electron-count parity | `1373 e-, 2S+1 = 6` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Dy box/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Dy | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.230 - 2.370` |  | target OH 2.23 / H2O 2.37 |
| nearest 2nd-shell O (A) | `4.129` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.944` |  |  |
| OH-...OH- O-O (A) | `2.711 3.833 4.212` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.711` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.909` | ok |  |
| H-bonds per solvent molecule | `3.01` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `76%` |  | 197 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0643` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.02752` | ok | 31 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.981` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell (A) | `15.782 15.782 15.782` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1373` | ok |  |
| spin multiplicity | `6` | ok | 4f^9 high spin, 5 unpaired |
| electron-count parity | `1373 e-, 2S+1 = 6` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Dy droplet/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Dy | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.230 - 2.370` |  | target OH 2.23 / H2O 2.37 |
| nearest 2nd-shell O (A) | `4.114` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.944` |  |  |
| OH-...OH- O-O (A) | `2.711 3.833 4.212` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.711` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.920` | ok |  |
| H-bonds per solvent molecule | `2.53` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `64%` |  | 166 bonds |
| droplet radius (A) | `9.753` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03371` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0341 4-6.0:0.0393 6-8.0:0.0282 8-9.8:0.0356` |  |  |
| N(O) within 3.10 A of Ln | `8` |  |  |
| N(O) within 5.50 A of Ln | `19` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03107` | ok | 35 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.990` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1373` | ok |  |
| spin multiplicity | `6` | ok | 4f^9 high spin, 5 unpaired |
| electron-count parity | `1373 e-, 2S+1 = 6` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Dy droplet/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Dy | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.230 - 2.370` |  | target OH 2.23 / H2O 2.37 |
| nearest 2nd-shell O (A) | `4.114` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.944` |  |  |
| OH-...OH- O-O (A) | `2.711 3.833 4.212` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.711` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.920` | ok |  |
| H-bonds per solvent molecule | `2.53` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `64%` |  | 166 bonds |
| droplet radius (A) | `9.753` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03371` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0341 4-6.0:0.0393 6-8.0:0.0282 8-9.8:0.0356` |  |  |
| N(O) within 3.10 A of Ln | `8` |  |  |
| N(O) within 5.50 A of Ln | `19` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03107` | ok | 35 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.990` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| vacuum gap (A) | `22.00` | ok | >= 18.0 A (MACE-POLAR-1-L receptive field) |
| cell (A) | `42.218 42.218 42.218` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1373` | ok |  |
| spin multiplicity | `6` | ok | 4f^9 high spin, 5 unpaired |
| electron-count parity | `1373 e-, 2S+1 = 6` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Er box/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Er | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.200 - 2.340` |  | target OH 2.20 / H2O 2.34 |
| nearest 2nd-shell O (A) | `4.115` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.915` |  |  |
| OH-...OH- O-O (A) | `2.675 3.781 4.155` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.675` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.907` | ok |  |
| H-bonds per solvent molecule | `2.05` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `52%` |  | 134 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0663` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03374` | ok | 38 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.988` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1375` | ok |  |
| spin multiplicity | `4` | ok | 4f^11 high spin, 3 unpaired |
| electron-count parity | `1375 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Er box/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Er | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.200 - 2.340` |  | target OH 2.20 / H2O 2.34 |
| nearest 2nd-shell O (A) | `4.115` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.915` |  |  |
| OH-...OH- O-O (A) | `2.675 3.781 4.155` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.675` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.907` | ok |  |
| H-bonds per solvent molecule | `2.78` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `70%` |  | 182 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0663` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03374` | ok | 38 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.988` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell (A) | `15.782 15.782 15.782` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1375` | ok |  |
| spin multiplicity | `4` | ok | 4f^11 high spin, 3 unpaired |
| electron-count parity | `1375 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Er droplet/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Er | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.200 - 2.340` |  | target OH 2.20 / H2O 2.34 |
| nearest 2nd-shell O (A) | `4.025` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.915` |  |  |
| OH-...OH- O-O (A) | `2.675 3.781 4.155` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.675` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.928` | ok |  |
| H-bonds per solvent molecule | `2.38` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `60%` |  | 156 bonds |
| droplet radius (A) | `9.794` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03329` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0341 4-6.0:0.0393 6-8.0:0.0339 8-9.8:0.0307` |  |  |
| N(O) within 3.10 A of Ln | `8` |  |  |
| N(O) within 5.50 A of Ln | `23` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03285` | ok | 37 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.986` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1375` | ok |  |
| spin multiplicity | `4` | ok | 4f^11 high spin, 3 unpaired |
| electron-count parity | `1375 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Er droplet/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Er | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.200 - 2.340` |  | target OH 2.20 / H2O 2.34 |
| nearest 2nd-shell O (A) | `4.025` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.915` |  |  |
| OH-...OH- O-O (A) | `2.675 3.781 4.155` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.675` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.928` | ok |  |
| H-bonds per solvent molecule | `2.38` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `60%` |  | 156 bonds |
| droplet radius (A) | `9.794` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03329` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0341 4-6.0:0.0393 6-8.0:0.0339 8-9.8:0.0307` |  |  |
| N(O) within 3.10 A of Ln | `8` |  |  |
| N(O) within 5.50 A of Ln | `23` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03285` | ok | 37 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.986` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| vacuum gap (A) | `22.00` | ok | >= 18.0 A (MACE-POLAR-1-L receptive field) |
| cell (A) | `41.653 41.653 41.653` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1375` | ok |  |
| spin multiplicity | `4` | ok | 4f^11 high spin, 3 unpaired |
| electron-count parity | `1375 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Gd box/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Gd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.270 - 2.410` |  | target OH 2.27 / H2O 2.41 |
| nearest 2nd-shell O (A) | `4.182` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.983` |  |  |
| OH-...OH- O-O (A) | `3.932 3.932 3.932` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.910` | ok |  |
| H-bonds per solvent molecule | `2.00` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `51%` |  | 131 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0621` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03018` | ok | 34 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.958` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1371` | ok |  |
| spin multiplicity | `8` | ok | 4f^7 high spin, 7 unpaired |
| electron-count parity | `1371 e-, 2S+1 = 8` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Gd box/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Gd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.270 - 2.410` |  | target OH 2.27 / H2O 2.41 |
| nearest 2nd-shell O (A) | `4.182` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.983` |  |  |
| OH-...OH- O-O (A) | `3.932 3.932 3.932` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.901` | ok |  |
| H-bonds per solvent molecule | `2.79` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `71%` |  | 183 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0621` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03018` | ok | 34 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.958` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell (A) | `15.782 15.782 15.782` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1371` | ok |  |
| spin multiplicity | `8` | ok | 4f^7 high spin, 7 unpaired |
| electron-count parity | `1371 e-, 2S+1 = 8` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Gd droplet/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Gd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.270 - 2.410` |  | target OH 2.27 / H2O 2.41 |
| nearest 2nd-shell O (A) | `3.947` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.983` |  |  |
| OH-...OH- O-O (A) | `3.932 3.932 3.932` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.901` | ok |  |
| H-bonds per solvent molecule | `2.49` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `63%` |  | 163 bonds |
| droplet radius (A) | `9.729` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03396` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0426 4-6.0:0.0393 6-8.0:0.0339 8-9.7:0.0309` |  |  |
| N(O) within 3.10 A of Ln | `9` |  |  |
| N(O) within 5.50 A of Ln | `24` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03285` | ok | 37 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.993` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1371` | ok |  |
| spin multiplicity | `8` | ok | 4f^7 high spin, 7 unpaired |
| electron-count parity | `1371 e-, 2S+1 = 8` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Gd droplet/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Gd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.270 - 2.410` |  | target OH 2.27 / H2O 2.41 |
| nearest 2nd-shell O (A) | `3.947` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.983` |  |  |
| OH-...OH- O-O (A) | `3.932 3.932 3.932` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.901` | ok |  |
| H-bonds per solvent molecule | `2.49` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `63%` |  | 163 bonds |
| droplet radius (A) | `9.729` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03396` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0426 4-6.0:0.0393 6-8.0:0.0339 8-9.7:0.0309` |  |  |
| N(O) within 3.10 A of Ln | `9` |  |  |
| N(O) within 5.50 A of Ln | `24` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03285` | ok | 37 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.993` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| vacuum gap (A) | `22.00` | ok | >= 18.0 A (MACE-POLAR-1-L receptive field) |
| cell (A) | `40.994 40.994 40.994` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1371` | ok |  |
| spin multiplicity | `8` | ok | 4f^7 high spin, 7 unpaired |
| electron-count parity | `1371 e-, 2S+1 = 8` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## La box/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_La | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.400 - 2.540` |  | target OH 2.40 / H2O 2.54 |
| nearest 2nd-shell O (A) | `4.141` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.109` |  |  |
| OH-...OH- O-O (A) | `4.157 4.157 4.157` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.720` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.906` | ok |  |
| H-bonds per solvent molecule | `2.14` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `54%` |  | 140 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0544` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03107` | ok | 35 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.944` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1364` | ok |  |
| spin multiplicity | `1` | ok | 4f^0 high spin, 0 unpaired |
| electron-count parity | `1364 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## La box/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_La | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.400 - 2.540` |  | target OH 2.40 / H2O 2.54 |
| nearest 2nd-shell O (A) | `4.141` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.109` |  |  |
| OH-...OH- O-O (A) | `4.157 4.157 4.157` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.720` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.906` | ok |  |
| H-bonds per solvent molecule | `2.87` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `73%` |  | 188 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0544` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03107` | ok | 35 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.944` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell (A) | `15.782 15.782 15.782` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1364` | ok |  |
| spin multiplicity | `1` | ok | 4f^0 high spin, 0 unpaired |
| electron-count parity | `1364 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## La droplet/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_La | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.400 - 2.540` |  | target OH 2.40 / H2O 2.54 |
| nearest 2nd-shell O (A) | `4.218` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.109` |  |  |
| OH-...OH- O-O (A) | `4.157 4.157 4.157` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.720` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.911` | ok |  |
| H-bonds per solvent molecule | `2.56` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `65%` |  | 168 bonds |
| droplet radius (A) | `9.722` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03403` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0384 4-6.0:0.0298 6-8.0:0.0371 8-9.7:0.0329` |  |  |
| N(O) within 3.10 A of Ln | `9` |  |  |
| N(O) within 5.50 A of Ln | `23` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03551` | ok | 40 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.918` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1364` | ok |  |
| spin multiplicity | `1` | ok | 4f^0 high spin, 0 unpaired |
| electron-count parity | `1364 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## La droplet/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_La | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.400 - 2.540` |  | target OH 2.40 / H2O 2.54 |
| nearest 2nd-shell O (A) | `4.218` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.109` |  |  |
| OH-...OH- O-O (A) | `4.157 4.157 4.157` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.720` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.911` | ok |  |
| H-bonds per solvent molecule | `2.56` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `65%` |  | 168 bonds |
| droplet radius (A) | `9.722` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03403` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0384 4-6.0:0.0298 6-8.0:0.0371 8-9.7:0.0329` |  |  |
| N(O) within 3.10 A of Ln | `9` |  |  |
| N(O) within 5.50 A of Ln | `23` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03551` | ok | 40 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.918` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| vacuum gap (A) | `22.00` | ok | >= 18.0 A (MACE-POLAR-1-L receptive field) |
| cell (A) | `41.263 41.263 41.263` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1364` | ok |  |
| spin multiplicity | `1` | ok | 4f^0 high spin, 0 unpaired |
| electron-count parity | `1364 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Lu box/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Lu | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.160 - 2.300` |  | target OH 2.16 / H2O 2.30 |
| nearest 2nd-shell O (A) | `3.795` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.876` |  |  |
| OH-...OH- O-O (A) | `2.626 3.713 4.080` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.908` | ok |  |
| H-bonds per solvent molecule | `2.08` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `53%` |  | 136 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0696` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03374` | ok | 38 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.970` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1378` | ok |  |
| spin multiplicity | `1` | ok | 4f^14 high spin, 0 unpaired |
| electron-count parity | `1378 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Lu box/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Lu | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.160 - 2.300` |  | target OH 2.16 / H2O 2.30 |
| nearest 2nd-shell O (A) | `3.795` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.876` |  |  |
| OH-...OH- O-O (A) | `2.626 3.713 4.080` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.908` | ok |  |
| H-bonds per solvent molecule | `2.84` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `72%` |  | 186 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0696` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03374` | ok | 38 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.970` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell (A) | `15.782 15.782 15.782` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1378` | ok |  |
| spin multiplicity | `1` | ok | 4f^14 high spin, 0 unpaired |
| electron-count parity | `1378 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Lu droplet/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Lu | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.160 - 2.300` |  | target OH 2.16 / H2O 2.30 |
| nearest 2nd-shell O (A) | `4.237` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.876` |  |  |
| OH-...OH- O-O (A) | `2.626 3.713 4.080` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.904` | ok |  |
| H-bonds per solvent molecule | `2.50` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `63%` |  | 164 bonds |
| droplet radius (A) | `9.631` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03501` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0341 4-6.0:0.0361 6-8.0:0.0355 8-9.6:0.0344` |  |  |
| N(O) within 3.10 A of Ln | `8` |  |  |
| N(O) within 5.50 A of Ln | `23` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03817` | ok | 43 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.984` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1378` | ok |  |
| spin multiplicity | `1` | ok | 4f^14 high spin, 0 unpaired |
| electron-count parity | `1378 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Lu droplet/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Lu | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `8` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.160 - 2.300` |  | target OH 2.16 / H2O 2.30 |
| nearest 2nd-shell O (A) | `4.237` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `2.876` |  |  |
| OH-...OH- O-O (A) | `2.626 3.713 4.080` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.626` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.904` | ok |  |
| H-bonds per solvent molecule | `2.50` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `63%` |  | 164 bonds |
| droplet radius (A) | `9.631` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03501` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0341 4-6.0:0.0361 6-8.0:0.0355 8-9.6:0.0344` |  |  |
| N(O) within 3.10 A of Ln | `8` |  |  |
| N(O) within 5.50 A of Ln | `23` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03817` | ok | 43 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.984` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| vacuum gap (A) | `22.00` | ok | >= 18.0 A (MACE-POLAR-1-L receptive field) |
| cell (A) | `41.661 41.661 41.661` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1378` | ok |  |
| spin multiplicity | `1` | ok | 4f^14 high spin, 0 unpaired |
| electron-count parity | `1378 e-, 2S+1 = 1` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Nd box/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Nd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.350 - 2.490` |  | target OH 2.35 / H2O 2.49 |
| nearest 2nd-shell O (A) | `3.975` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.060` |  |  |
| OH-...OH- O-O (A) | `4.070 4.070 4.070` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.716` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.919` | ok |  |
| H-bonds per solvent molecule | `2.11` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `53%` |  | 138 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0566` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03462` | ok | 39 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.959` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1367` | ok |  |
| spin multiplicity | `4` | ok | 4f^3 high spin, 3 unpaired |
| electron-count parity | `1367 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Nd box/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Nd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.350 - 2.490` |  | target OH 2.35 / H2O 2.49 |
| nearest 2nd-shell O (A) | `3.975` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.060` |  |  |
| OH-...OH- O-O (A) | `4.070 4.070 4.070` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.716` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.919` | ok |  |
| H-bonds per solvent molecule | `2.95` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `75%` |  | 193 bonds |
| cube edge (A) | `15.782` |  |  |
| solvent number density (1/A^3) | `0.03333` | ok | target 0.03333 |
| solution mass density (g/cm3) | `1.0566` |  | > 1 as expected for a Ln salt solution |
| L/2 (A) | `7.891` | ok | must exceed the per-layer MLIP cutoff (~6 A) |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03462` | ok | 39 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.959` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell (A) | `15.782 15.782 15.782` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1367` | ok |  |
| spin multiplicity | `4` | ok | 4f^3 high spin, 3 unpaired |
| electron-count parity | `1367 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Nd droplet/non-pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Nd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.350 - 2.490` |  | target OH 2.35 / H2O 2.49 |
| nearest 2nd-shell O (A) | `4.263` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.060` |  |  |
| OH-...OH- O-O (A) | `4.070 4.070 4.070` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.716` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.900` | ok |  |
| H-bonds per solvent molecule | `2.35` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `59%` |  | 154 bonds |
| droplet radius (A) | `9.719` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03406` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0384 4-6.0:0.0346 6-8.0:0.0355 8-9.7:0.0323` |  |  |
| N(O) within 3.10 A of Ln | `9` |  |  |
| N(O) within 5.50 A of Ln | `27` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03196` | ok | 36 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.948` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| cell is empty | `True` | ok |  |
| pbc | `(False, False, False)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1367` | ok |  |
| spin multiplicity | `4` | ok | 4f^3 high spin, 3 unpaired |
| electron-count parity | `1367 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |

## Nd droplet/pbc

| check | value | status | note |
|---|---|---|---|
| n_atoms | `391` | ok |  |
| n_Nd | `1` | ok |  |
| n_O | `131` | ok |  |
| n_H | `259` | ok |  |
| n_OH- | `3` | ok |  |
| n_H2O | `128` | ok |  |
| unassigned H | `0` | ok |  |
| O with != 1,2 H | `0` | ok |  |
| O-H bond range (A) | `0.9572 - 0.9640` | ok |  |
| H-O-H angle range (deg) | `104.52 - 104.52` | ok |  |
| Ln coordination number | `9` | ok |  |
| OH- in first shell | `3` | ok |  |
| d(Ln-O) first shell (A) | `2.350 - 2.490` |  | target OH 2.35 / H2O 2.49 |
| nearest 2nd-shell O (A) | `4.263` | ok | first minimum of g(Ln-O) |
| nearest Ln-H (A) | `3.060` |  |  |
| OH-...OH- O-O (A) | `4.070 4.070 4.070` | ok | ligand-ligand contact |
| min intermol. O-O (A) | `2.716` | ok |  |
| min intermol. O-H (A) | `1.763` | ok |  |
| min intermol. H-H (A) | `1.900` | ok |  |
| H-bonds per solvent molecule | `2.35` | ok | bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions |
| O-H groups donating a H-bond | `59%` |  | 154 bonds |
| droplet radius (A) | `9.719` | ok | density target 9.790 |
| solvent number density (1/A^3) | `0.03406` | ok | target 0.03333, +-8% finite-size noise |
| radial O density by shell (1/A^3) | `0-2.0:0.0000 2-4.0:0.0384 4-6.0:0.0346 6-8.0:0.0355 8-9.7:0.0323` |  |  |
| N(O) within 3.10 A of Ln | `9` |  |  |
| N(O) within 5.50 A of Ln | `27` |  |  |
| O density in the 4.2-7.0 A annulus (1/A^3) | `0.03196` | ok | 36 oxygens, bulk would give 37.5 |
| largest interior cavity (A) | `2.948` | ok | biggest O-free sphere; ideal lattice at this density gives ~2.5 A |
| vacuum gap (A) | `22.00` | ok | >= 18.0 A (MACE-POLAR-1-L receptive field) |
| cell (A) | `41.302 41.302 41.302` |  |  |
| pbc | `(True, True, True)` |  |  |
| net charge | `0` | ok | Ln(3+) + 3 OH(-) |
| total electrons | `1367` | ok |  |
| spin multiplicity | `4` | ok | 4f^3 high spin, 3 unpaired |
| electron-count parity | `1367 e-, 2S+1 = 4` | ok | even electrons <-> odd multiplicity |
| info keys for MLIPs | `['charge', 'spin', 'spin_multiplicity']` | ok |  |
