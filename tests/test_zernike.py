"""Tests for the Zernike submodule."""
import os

import pytest

import numpy as np

from prysm.coordinates import cart_to_polar
from prysm import zernike


SAMPLES = 32

X, Y = np.linspace(-1, 1, SAMPLES), np.linspace(-1, 1, SAMPLES)


@pytest.fixture
def rho():
    rho, phi = cart_to_polar(X, Y)
    return rho


@pytest.fixture
def phi():
    rho, phi = cart_to_polar(X, Y)
    return phi


@pytest.fixture
def fit_data():
    p = zernike.FringeZernike(Z9=1, samples=SAMPLES)
    return p.phase, p.coefs


def test_all_zernfcns_run_without_error_or_nans(rho, phi):
    for i in range(len(zernike.zernikes)):
        assert zernike.zcache(i, norm=False, samples=SAMPLES).all()


def test_all_zernfcns_run_without_errors_or_nans_with_norms(rho, phi):
    for i in range(len(zernike.zernikes)):
        assert zernike.zcache(i, norm=True, samples=SAMPLES).all()


def test_can_build_fringezernike_pupil_with_vector_args():
    abers = np.random.rand(48)
    p = zernike.FringeZernike(abers, samples=SAMPLES)
    assert p


def test_repr_is_a_str():
    p = zernike.FringeZernike()
    assert type(repr(p)) is str


def test_fringezernike_rejects_base_not_0_or_1():
    with pytest.raises(ValueError):
        zernike.FringeZernike(base=2)
    with pytest.raises(ValueError):
        zernike.FringeZernike(base=-1)


def test_fringezernike_takes_all_named_args():
    params = {
        'norm': True,
        'base': 1,
    }
    p = zernike.FringeZernike(**params)
    assert p


def test_fringezernike_will_pass_pupil_args():
    params = {
        'samples': 32,
        'wavelength': 0.5,
    }
    p = zernike.FringeZernike(**params)
    assert p


def test_fit_agrees_with_truth(fit_data):
    data, real_coefs = fit_data
    coefs = zernike.zernikefit(data, map_='fringe')
    real_coefs = np.asarray(real_coefs)
    assert coefs[8] == pytest.approx(real_coefs[8])


def test_fit_does_not_throw_on_normalize(fit_data):
    data, real_coefs = fit_data
    coefs = zernike.zernikefit(data, norm=True, map_='fringe')
    assert coefs[8] != 0


def test_fit_raises_on_too_many_terms(fit_data):
    data, real_coefs = fit_data
    with pytest.raises(ValueError):
        zernike.zernikefit(data, terms=100)
