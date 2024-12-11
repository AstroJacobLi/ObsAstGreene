import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import copy
import matplotlib
import matplotlib.pyplot as plt
from astropy.visualization import (AsymmetricPercentileInterval,
                                   ZScaleInterval, make_lupton_rgb)
from astropy import visualization as aviz
from astropy.nddata.blocks import block_reduce
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable

IMG_CMAP = copy.copy(matplotlib.cm.get_cmap("viridis"))
IMG_CMAP.set_bad(color='black')


def format_object_name(ra=None, dec=None, skycoordobj=None, unit="deg"):
    """
    Given a `skycoordobj` object, returns a string representing the object name in the standard form:
    J{RAhms}{+/-}{DECdms}

    Parameters:
    -----------
    ra: float
        The right ascension of the object in decimal degrees.
    dec: float
        The declination of the object in decimal degrees.
    skycoordobj: `astropy.coordinates.SkyCoord` object
        The SkyCoord object representing the object. If not provided, it will be created from `ra` and `dec`.
    unit: str
        The unit of the input `ra` and `dec`. Default is "deg".

    Returns:
    --------
    cname: str
        A string representing the name of the object in the standard form.
    """
    if skycoordobj is None:
        skycoordobj = SkyCoord(ra, dec, unit=unit)
    rastring = skycoordobj.ra.to_string(unit=u.hourangle, sep="", precision=2, pad=True)
    decstring = skycoordobj.dec.to_string(unit=u.deg, sep="", precision=2, pad=True)
    sign = "+" if skycoordobj.dec > 0 else ""
    cname = f"J{rastring}{sign}{decstring}"
    return cname



def pad_psf(psf, size=65):
    """
    Zero-pad a PSF image such that it has the square shape of `size`.
    
    Parameters
    ----------
    psf: numpy array
        The PSF image.
    size: int
        The size of the padded PSF.
    
    Returns
    -------
    padded_psf: numpy array
        The padded PSF image.
    """
    padding = np.array(size)
    padding -= np.asarray(psf.shape)
    if not (padding % 2 == 0).all():
        raise ValueError("Padding requires a non-integer pixel count!")
    padding = [(pad // 2, pad // 2) for pad in padding]
    return np.pad(psf, padding)


def calc_PSF_FWHM(psfs=None):
    """
    Measure the FWHM of the PSF by fitting a 2D Moffat profile to each PSF cutout.
    
    Parameters
    ----------
    psfs: dict
        A dictionary containing the PSF images for each band.
    
    Returns
    -------
    fwhm: dict
        A dictionary containing the FWHM of the PSF for each band (in pixels).
    """
    from astropy.modeling import models, fitting
    bands = list(psfs.keys())

    fit_p = fitting.LevMarLSQFitter()
    fwhms = {}
    for ix, band in enumerate(bands):
        z = psfs[band]
        mid = np.array(z.shape) // 2
        y, x = np.mgrid[: z.shape[0], : z.shape[1]]
        p_init = models.Moffat2D(x_0=mid[0], y_0=mid[1], amplitude=z[mid[0], mid[1]])
        p = fit_p(p_init, x, y, z)
        fwhms[band] = p.fwhm

    return fwhms
