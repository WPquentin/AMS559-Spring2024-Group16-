### NumericalDiffusionScheme
### Jake Aylmer
###
### Outer code used to generate a test run of the diffusion scheme for the case
### with constant diffusivity k(x,t) = k0 and S(x,t) = 0.
### ---------------------------------------------------------------------------

from __future__ import division
import matplotlib as mpl, matplotlib.pyplot as plt
import numpy as np
import diffusion_scheme as dif, plotting as pl


def ConstantDiffusivity(x, k0=2.5E-3):
    """Return the constant diffusivity at position x."""
    return k0


def AnalyticSolution(x, t, k0=0.25, L=2.0, q_max=4.0, truncate=20):
    """The analytic solution to the diffusion equation with constant
    diffusivity k=k0, zero sources/sinks (S=0), Neumann boundary conditions and
    initial conditions q(x,0) = q_max*x*(L-x). See repository documentation for
    details.
    
    --Arguments (optional ones in round brackets)--
    x          : NumPy array, x-coordinates.
    t          : float, time at which to return the solution.
    (k0)       : float, constant value of diffusivity (default 0.25).
    (q_max)    : float, maximum of initial q profile.
    (truncate) : integer, where to truncate the series expansion.
    """
    q_an = np.zeros(len(x)) + (L**2*q_max/6)
    
    for n in np.arange(2, truncate+1, 2):
        coeff = (-4*q_max*L**2/((n*np.pi)**2))
        q_an += coeff*np.exp(-k0*(n*np.pi/L)**2*t)*np.cos(n*np.pi*x/L)
    
    return q_an


def main(L=2.0, N=60, t_tot=60.0, nt=60, q_max=4.0):
    """Main routine which is run on start-up of the program. It may be re-run
    with different arguments in a Python interpretter.
    
    --Optional arguments--
    L     : float, upper domain limit in m (so that 0 < x < L).
    N     : int, number of grid cells to split the domain into.
    t_tot : float, total integration time (s).
    nt    : int, number of time steps (this determines the time-step through
            dt = t_tot / nt).
    q_max : float, sets the overall magnitude of the initial conditions.
    """
    h = L/N # width of grid cells [m]
    k0 = ConstantDiffusivity(0)
    dt = t_tot/nt # time step [s]

    x = np.linspace(h/2, L-h/2, N) # grid cell centres [m]
    q_init = q_max*x*(L - x) # initial conditions
    S = np.zeros(N) # source (0 everywhere)
    q_an = AnalyticSolution(x, nt*dt, k0, L, q_max)
    q_old_CN = q_init.copy(); q_old_BE = q_init.copy()
    
    int_q_CN = np.zeros(nt); int_q_BE = np.zeros(nt)
    
    for i in range(nt):
        
        int_q_CN[i] = np.sum(q_old_CN) * h
        int_q_BE[i] = np.sum(q_old_BE) * h
        
        q_new_CN = dif.SolveDiffusionEquation(q_old_CN, S, S,
            ConstantDiffusivity, dt, L, 0.5) # Crank-Nicolson (CN)
        q_new_BE = dif.SolveDiffusionEquation(q_old_BE, S, S,
            ConstantDiffusivity, dt, L, 1.0) # Backward-Euler (BE)
        q_old_CN = q_new_CN.copy()
        q_old_BE = q_new_BE.copy()
    
    fig1, ax1 = pl.MakePlots(
        x, q_init, q_an, q_new_CN, q_new_BE, nt, dt, k0,
        xlim=[0,L], ylim=[0,q_max])
    fig2, ax2 = pl.EnergyPlot(
        np.linspace(0, nt*dt, nt), int_q_CN, int_q_BE,
        xlim=[0,L], ylim=[5,6])
    fig1.show()
    fig2.show()
    pass


if __name__ == '__main__':
    pl.SetRCParams()
    main()
