"""Reference data for Ln(3+) / hydroxide / water model building.

Spin multiplicities are the free-ion Hund's-rule (high-spin) ground states of the
4f^n configuration.  This matches OMol25, where only high-spin states were
computed for lanthanide complexes, so all three MLIPs (UMA-omol, MACE-OMOL,
MACE-POLAR-1) expect the high-spin value.

Ln-O distances are first-shell EXAFS/XRD values for the aqua ions; the hydroxide
distance is shorter than the aqua distance because OH- is the stronger donor.
Coordination numbers follow the experimental series: CN = 9 (tricapped trigonal
prism) for the light Ln, CN = 8 (square antiprism) from Dy onwards.
"""

# 4f^n -> number of unpaired electrons (high spin, n <= 7 -> n; n > 7 -> 14 - n)
_N_UNPAIRED = {0: 0, 3: 3, 7: 7, 9: 5, 11: 3, 14: 0}

LN_DATA = {
    #        Z    4f^n  CN  d(Ln-OH)  d(Ln-OH2)   Shannon r (CN of row)
    "La": dict(Z=57, nf=0, cn=9, d_oh=2.40, d_ow=2.54, r_ion=1.216),
    "Nd": dict(Z=60, nf=3, cn=9, d_oh=2.35, d_ow=2.49, r_ion=1.163),
    "Gd": dict(Z=64, nf=7, cn=9, d_oh=2.27, d_ow=2.41, r_ion=1.107),
    "Dy": dict(Z=66, nf=9, cn=8, d_oh=2.23, d_ow=2.37, r_ion=1.027),
    "Er": dict(Z=68, nf=11, cn=8, d_oh=2.20, d_ow=2.34, r_ion=1.004),
    "Lu": dict(Z=71, nf=14, cn=8, d_oh=2.16, d_ow=2.30, r_ion=0.977),
}

for _sym, _d in LN_DATA.items():
    _d["n_unpaired"] = _N_UNPAIRED[_d["nf"]]
    _d["multiplicity"] = _d["n_unpaired"] + 1
    _d["S"] = _d["n_unpaired"] / 2.0

# --- composition of every system -------------------------------------------
N_WATER = 128
N_HYDROXIDE = 3
LN_OXIDATION = +3
NET_CHARGE = LN_OXIDATION - N_HYDROXIDE  # 0, deliberately neutral

# --- molecular geometry (gas phase experimental) ----------------------------
R_OH_WATER = 0.9572  # A
ANGLE_HOH = 104.52  # deg
R_OH_HYDROXIDE = 0.964  # A, free OH-
ANGLE_LN_O_H = 130.0  # deg, H of a coordinated OH- tilts away from the metal

# --- liquid water reference (298 K, 1 bar) ---------------------------------
RHO_WATER_MASS = 0.9970  # g/cm3
RHO_WATER_NUM = 0.033327  # molecules / A^3  == 0.9970 g/cm3 for M = 18.0153

# --- packing acceptance criteria (A) ---------------------------------------
MIN_OO = 2.65  # bulk-bulk oxygen-oxygen
MIN_OO_SHELL = 2.55  # involving a first-shell ligand oxygen
MIN_OH_INTER = 1.60  # intermolecular O...H (H-bond contact)
MIN_HH_INTER = 1.80  # intermolecular H...H
# Floor on the Ln-O distance of a non-coordinated water.  It only has to keep
# the first shell unambiguous (well beyond the 3.10 A coordination cutoff) and
# stay inside the experimental first minimum of g(Ln-O), ~3.3-3.5 A.  Excluding
# a larger sphere would be wrong: the first shell is a polyhedron, not a shell
# of uniform density, so a spherical cut-out leaves artificial voids in the
# pockets between ligands where second-shell water belongs.
MIN_LN_O_BULK = 3.70
MIN_LN_H_BULK = 3.00  # Ln to any non-coordinated H
