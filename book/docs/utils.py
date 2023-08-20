import numpy as np
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


def display_single(img,
                   xsize=10,
                   ysize=10,
                   ax=None,
                   stretch='arcsinh',
                   scale='zscale',
                   contrast=0.25,
                   alpha=1.0,
                   no_negative=False,
                   lower_percentile=1.0,
                   upper_percentile=99.0,
                   cmap=IMG_CMAP,
                   norm=None,
                   color_bar=False,
                   color_bar_fontsize=18,
                   color_bar_color='w'):
    """
    Display single image using ``arcsinh`` stretching, "zscale" scaling, 
    and ``viridis`` colormap as default.

    Parameters
    ----------
    img (numpy 2-D array): The image array.
    xsize (int): Width of the image, default = 8.
    ysize (int): Height of the image, default = 8.
    ax (``matplotlib.pyplot.axes`` object): The user could provide axes on which the figure will be drawn.
    stretch (str): Stretching schemes. Options are "arcsinh", "log", "log10" and "linear".
    scale (str): Scaling schemes. Options are "zscale" and "percentile".
    contrast (float): Contrast of figure.
    no_negative (bool): If true, all negative pixels will be set to zero.
    lower_percentile (float): Lower percentile, if using ``scale="percentile"``.
    upper_percentile (float): Upper percentile, if using ``scale="percentile"``.
    cmap (str): Colormap.
    color_bar (bool): Whether show colorbar or not.

    Returns
    -------
    fig (``matplotlib.pyplot.figure`` object): The figure object.

    """

    if ax is None:
        fig = plt.figure(figsize=(xsize, ysize), dpi=100)
        ax1 = fig.add_subplot(111)
    else:
        ax1 = ax

    # Stretch option
    if stretch.strip() == 'arcsinh':
        img_scale = np.arcsinh(img)
    elif stretch.strip() == 'log':
        if no_negative:
            img[img <= 0.0] = 1.0E-10
        img_scale = np.log(img)
    elif stretch.strip() == 'log10':
        if no_negative:
            img[img <= 0.0] = 1.0E-10
        img_scale = np.log10(img)
    elif stretch.strip() == 'linear':
        img_scale = img
    else:
        raise Exception("# Wrong stretch option.")

    # Scale option
    if scale.strip() == 'zscale':
        try:
            zmin, zmax = ZScaleInterval(
                contrast=contrast).get_limits(img_scale)
        except IndexError:
            # TODO: Deal with problematic image
            zmin, zmax = -1.0, 1.0
    elif scale.strip() == 'percentile':
        try:
            zmin, zmax = AsymmetricPercentileInterval(
                lower_percentile=lower_percentile,
                upper_percentile=upper_percentile).get_limits(img_scale)
        except IndexError:
            # TODO: Deal with problematic image
            zmin, zmax = -1.0, 1.0
    else:
        zmin, zmax = np.nanmin(img_scale), np.nanmax(img_scale)

    show = ax1.imshow(img_scale, origin='lower', cmap=cmap, norm=norm,
                      vmin=zmin, vmax=zmax, alpha=alpha)

    # Hide ticks and tick labels
    ax1.tick_params(
        labelbottom=False,
        labelleft=False,
        axis=u'both',
        which=u'both',
        length=0)

    if color_bar:
        divider = make_axes_locatable(ax1)
        ax_cbar = divider.append_axes("right", size="5%", pad=0.05)
        # ax_cbar = inset_axes(ax1,
        #                      width=color_bar_width,
        #                      height=color_bar_height,
        #                      loc=color_bar_loc)
        cbar = plt.colorbar(show, ax=ax1, cax=ax_cbar)

        cbar.ax.xaxis.set_tick_params(color=color_bar_color)
        cbar.ax.yaxis.set_tick_params(color=color_bar_color)
        cbar.outline.set_edgecolor(color_bar_color)
        plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'),
                 color=color_bar_color, fontsize=color_bar_fontsize)
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'),
                 color=color_bar_color, fontsize=color_bar_fontsize)

    if ax is None:
        return fig
    return ax1


def show_image(image,
               percl=99, percu=None, vmin=None, vmax=None,
               is_mask=False, figsize=(10, 10),
               cmap='viridis', log=False, clip=True,
               show_colorbar=True, show_ticks=False,
               fig=None, ax=None, input_ratio=None):
    """
    Show an image in matplotlib with some basic astronomically-appropriate stretching.
    From https://github.com/astropy/ccd-reduction-and-photometry-guide/blob/main/notebooks/convenience_functions.py

    Parameters
    ----------
    image (numpy array): The image array.
    percl (float): The percentile for the lower edge of the stretch (or both edges if ``percu`` is None).
    percu (float): The percentile for the upper edge of the stretch (or None to use ``percl`` for both).
    is_mask (bool): Set to ``True`` if the image is a mask, i.e. all values are either zero or one.
    figsize (tuple): The size of the matplotlib figure in inches.
    cmap (str): Colormap.
    log (bool): If true, use log stretch.
    clip (bool): If true, clip the image.
    show_colorbar (bool): Whether show colorbar or not.
    show_ticks (bool): Whether show ticks or not.
    fig (``matplotlib.pyplot.figure`` object): The figure object.
    ax (``matplotlib.pyplot.axes`` object): The axes object.
    input_ratio (float): The ratio of the input image size to the output image size.

    Returns
    -------
    fig (``matplotlib.pyplot.figure`` object): The figure object.
    """
    if percu is None:
        percu = percl
        percl = 100 - percl

    if (fig is None and ax is not None) or (fig is not None and ax is None):
        raise ValueError('Must provide both "fig" and "ax" '
                         'if you provide one of them')
    elif fig is None and ax is None:
        if figsize is not None:
            # Rescale the fig size to match the image dimensions, roughly
            image_aspect_ratio = image.shape[0] / image.shape[1]
            figsize = (max(figsize), max(figsize) / image_aspect_ratio)

        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=100)

    # To preserve details we should *really* downsample correctly and
    # not rely on matplotlib to do it correctly for us (it won't).

    # So, calculate the size of the figure in pixels, block_reduce to
    # roughly that,and display the block reduced image.

    # Thanks, https://stackoverflow.com/questions/29702424/how-to-get-matplotlib-figure-size
    fig_size_pix = fig.get_size_inches() * fig.dpi

    ratio = (image.shape // fig_size_pix).max()

    if ratio < 1:
        ratio = 1

    ratio = input_ratio or ratio

    reduced_data = block_reduce(image, ratio)

    if not is_mask:
        # Divide by the square of the ratio to keep the flux the same in the
        # reduced image. We do *not* want to do this for images which are
        # masks, since their values should be zero or one.
        reduced_data = reduced_data / ratio**2

    # Of course, now that we have downsampled, the axis limits are changed to
    # match the smaller image size. Setting the extent will do the trick to
    # change the axis display back to showing the actual extent of the image.
    extent = [0, image.shape[1], 0, image.shape[0]]

    if log:
        stretch = aviz.LogStretch()
    else:
        stretch = aviz.LinearStretch()

    if vmin is not None and vmax is not None:
        interval = aviz.ManualInterval(vmin, vmax)
    else:
        interval = aviz.AsymmetricPercentileInterval(percl, percu)
    norm = aviz.ImageNormalize(reduced_data,
                               interval=interval,
                               stretch=stretch, clip=clip)

    if is_mask:
        # The image is a mask in which pixels should be zero or one.
        # block_reduce may have changed some of the values, so reset here.
        reduced_data = reduced_data > 0
        # Set the image scale limits appropriately.
        scale_args = dict(vmin=0, vmax=1)
    else:
        scale_args = dict(norm=norm)

    im = ax.imshow(reduced_data, origin='lower',
                   cmap=cmap, extent=extent, aspect='equal', **scale_args)

    if show_colorbar:
        divider = make_axes_locatable(ax)
        ax_cbar = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, ax=ax, cax=ax_cbar)
        plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), fontsize=11)
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), fontsize=11)

    if not show_ticks:
        ax.tick_params(
            labelbottom=False,
            labelleft=False,
            axis=u'both',
            which=u'both',
            length=0)

    if ax is None:
        return fig
    return ax
