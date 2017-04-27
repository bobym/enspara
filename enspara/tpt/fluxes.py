#author(s): TJ Lane (tjlane@stanford.edu) and Christian Schwantes
#            (schwancr@stanford.edu)
# Contributors: Vince Voelz, Kyle Beauchamp, Robert McGibbon, Maxwell Zimmerman
# Copyright (c) 2014, Stanford University
# All rights reserved.

"""
Functions for calculating the fluxes through an MSM for a
given set of source and sink states.

These are the canonical references for TPT. Note that TPT
is really a specialization of ideas very familiar to the
mathematical study of Markov chains, and there are many
books, manuscripts in the mathematical literature that
cover the same concepts.

References
----------
.. [1] Weinan, E. and Vanden-Eijnden, E. Towards a theory of
       transition paths. J. Stat. Phys. 123, 503-523 (2006).
.. [2] Metzner, P., Schutte, C. & Vanden-Eijnden, E.
       Transition path theory for Markov jump processes.
       Multiscale Model. Simul. 7, 1192-1219 (2009).
.. [3] Berezhkovskii, A., Hummer, G. & Szabo, A. Reactive
       flux and folding pathways in network models of
       coarse-grained protein dynamics. J. Chem. Phys.
       130, 205102 (2009).
.. [4] Noe, Frank, et al. "Constructing the equilibrium ensemble of folding
       pathways from short off-equilibrium simulations." PNAS 106.45 (2009):
       19011-19016.
"""
from __future__ import print_function, division, absolute_import
import numpy as np

from msmbuilder.tpt import committors

__all__ = ['fluxes', 'net_fluxes']

def fluxes(tprob, populations, sources, sinks, for_committors=None):
    """
    Compute the transition path theory flux matrix.

    Parameters
    ----------
    tprob : array, shape [n_states, n_states]
        Transition probability matrix.
    populations : array, shape [n_states, ]
        Equilibrium populations of each state.
    sources : array_like, int
        The set of unfolded/reactant states.
    sinks : array_like, int
        The set of folded/product states.
    for_committors : np.ndarray, optional
        The forward committors associated with `sources`, `sinks`, and `tprob`.
        If not provided, is calculated from scratch. If provided, `sources`
        and `sinks` are ignored.

    Returns
    -------
    flux_matrix : np.ndarray
        The flux matrix

    See Also
    --------
    net_fluxes

    References
    ----------
    .. [1] Weinan, E. and Vanden-Eijnden, E. Towards a theory of
           transition paths. J. Stat. Phys. 123, 503-523 (2006).
    .. [2] Metzner, P., Schutte, C. & Vanden-Eijnden, E.
           Transition path theory for Markov jump processes.
           Multiscale Model. Simul. 7, 1192-1219 (2009).
    .. [3] Berezhkovskii, A., Hummer, G. & Szabo, A. Reactive
           flux and folding pathways in network models of
           coarse-grained protein dynamics. J. Chem. Phys.
           130, 205102 (2009).
    .. [4] Noe, Frank, et al. "Constructing the equilibrium ensemble of folding
           pathways from short off-equilibrium simulations." PNAS 106.45 (2009):
           19011-19016.
    """
    sources = np.array(sources).reshape((-1,))
    sinks = np.array(sinks).reshape((-1,))

    n_states = len(populations)

    # check if we got the committors
    if for_committors is None:
        for_committors = committors(sources, sinks, msm)
    else:
        for_committors = np.array(for_committors)
        if for_committors.shape != (n_states,):
            raise ValueError(
                "Shape of committors %s should be %s" % \
                (str(for_committors.shape), str((n_states,))))

    rev_committors = 1 - for_committors

    # fij = pi_i * q-_i * Tij * q+_j
    fluxes = tprob*((populations*rev_committors)[:,None])*for_committors

    fluxes = np.dot(np.dot(X, tprob), Y)
    fluxes[(np.arange(n_states), np.arange(n_states))] = np.zeros(n_states)

    return fluxes
