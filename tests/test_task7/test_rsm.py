import pytest
from pyformlang import cfg as c
from copy import deepcopy

from project.ecfg import ECFG
from project.rsm import RSM
from tests.utils import get_data


def _from_ecfg(rsm, ecfg):
    acc = True
    for var in ecfg.productions:
        actual = rsm.boxes[var]
        expected = ecfg.productions[var].to_epsilon_nfa()
        acc = acc and actual.is_equivalent_to(expected)

    return rsm.start == ecfg.start and len(rsm.boxes) == len(ecfg.productions) and acc


@pytest.mark.parametrize(
    "ecfg",
    get_data(
        "test_cfg",
        lambda d: (
            ECFG.from_cfg(
                c.CFG.from_text(d["cfg"], d["start"])
                if d["start"] is not None
                else c.CFG.from_text(d["cfg"])
            )
        ),
    ),
)
def test_rsm_ecfg(ecfg: ECFG):
    assert _from_ecfg(RSM.from_ecfg(ecfg), ecfg)


@pytest.mark.parametrize(
    "rsm",
    get_data(
        "test_cfg",
        lambda d: (
            RSM.from_ecfg(
                ECFG.from_cfg(
                    c.CFG.from_text(d["cfg"], d["start"])
                    if d["start"] is not None
                    else c.CFG.from_text(d["cfg"])
                )
            )
        ),
    ),
)
def test_minimization(rsm: RSM):
    actual = deepcopy(rsm).minimize()

    assert len(actual.boxes) == len(rsm.boxes)

    for var in rsm.boxes:
        assert actual.boxes[var].is_equivalent_to(rsm.boxes[var])
