import numpy as np
from tqdm import tqdm
import scipy.optimize as optim

def loglikelihood(params, history, t):
        """
        Returns the loglikelihood of a Hawkes process with exponential kernel
        computed with a linear time complexity
            
        params   -- parameter tuple (p,beta) of the Hawkes process
        history  -- (n,2) numpy array containing marked time points (t_i,m_i)  
        t        -- current time (i.e end of observation window)
        """
        
        p,beta = params    
        
        if p <= 0 or p >= 1 or beta <= 0.: return -np.inf

        n = len(history)
        tis = history[:,0]
        mis = history[:,1]
        
        LL = (n-1) * np.log(p * beta)
        logA = -np.inf
        prev_ti, prev_mi = history[0]
        
        i = 0
        for ti,mi in history[1:]:
            if(prev_mi + np.exp(logA) <= 0):
                print("Bad value", prev_mi + np.exp(logA))
            
            logA = np.log(prev_mi + np.exp(logA)) - beta * (ti - prev_ti)
            LL += logA
            prev_ti,prev_mi = ti,mi
            i += 1
            
        logA = np.log(prev_mi + np.exp(logA)) - beta * (t - prev_ti)
        LL -= p * (np.sum(mis) - np.exp(logA))

        return LL


class Predictor:
    def __init__(self):
        self.alpha = 2.4
        self.mu = 10

    def compute_MLE(self, history, t,
                    init_params=np.array([0.0001, 1./60]), 
                    max_n_star = 1., display=False):
        """
        Returns the pair of the estimated loglikelihood and parameters (as a numpy array)

        history     -- (n,2) numpy array containing marked time points (t_i,m_i)  
        t           -- current time (i.e end of observation window)
        alpha       -- power parameter of the power-law mark distribution
        mu          -- min value parameter of the power-law mark distribution
        init_params -- initial values for the parameters (p,beta)
        max_n_star  -- maximum authorized value of the branching factor (defines the upper bound of p)
        display     -- verbose flag to display optimization iterations (see 'disp' options of optim.optimize)
        """
        
        # Define the target function to minimize as minus the loglikelihood
        target = lambda params : - loglikelihood(params, history, t)
        
        EM = self.mu * (self.alpha - 1) / (self.alpha - 2)
        eps = 1.E-8

        # Set realistic bounds on p and beta
        p_min, p_max       = eps, max_n_star/EM - eps
        beta_min, beta_max = 1/(3600. * 24 * 10), 1/(60. * 1)
        
        
        # Define the bounds on p (first column) and beta (second column)
        bounds = optim.Bounds(
            np.array([p_min, beta_min]),
            np.array([p_max, beta_max])
        )
        
        # Run the optimization
        res = optim.minimize(
            target, init_params,
            method='Powell',
            bounds=bounds,
            options={'xtol': 1e-8, 'disp': display}
        )
        
        # Returns the loglikelihood and found parameters
        return(-res.fun, res.x)
    
    def prediction(self, params, history, observation):
        """
        Returns the expected total numbers of points for a set of time points
        
        params   -- parameter tuple (p,beta) of the Hawkes process
        history  -- (n,2) numpy array containing marked time points (t_i,m_i)  
        alpha    -- power parameter of the power-law mark distribution
        mu       -- min value parameter of the power-law mark distribution
        t        -- current time (i.e end of observation window)
        """

        p,beta = params
        
        tis = history[:,0]
    
        EM = self.mu * (self.alpha - 1) / (self.alpha - 2)
        n_star = p * EM
        if n_star >= 1:
            raise Exception(f"Branching factor {n_star:.2f} greater than one")
        n = len(history)

        I = history[:,0] < observation
        tis = history[I,0]
        mis = history[I,1]
        G1 = p * np.sum(mis * np.exp(-beta * (observation - tis)))
        Ntot = n + G1 / (1. - n_star)
        return Ntot

    def predictions_from_estimator_MLE(self, history, T=None, n_tries=1, slider=True):
        """
        Compute the provided estimator for different observation windows and apply prediction according to it. Returns
        * the expected total numbers of points for a set of time points as a 1D-array
        * the computed loglikelihoods as a 1D-array
        * the estimated parameters as a 2D-array
        
        estimator -- function that implements an estimator that expect the same arguments as compute_MLE
        history   -- (n,2) numpy array containing marked time points (t_i,m_i)  
        alpha     -- power parameter of the power-law mark distribution
        mu        -- min value parameter of the power-law mark distribution
        T         -- 1D-array of times (i.e ends of observation window)
        n_tries   -- number of times the estimator is run. Best result is kept.
        """

        #ADD THIS LINE
        estimator = self.compute_MLE

        tis = history[:,0]
        if T is None:
            T = np.linspace(60, tis[-1], 50) # Compute 50 points from 1min to last time point
        
        N      = np.zeros((len(T),2)); N[:,0] = T
        LLs    = np.zeros((len(T),2)); LLs[:,0] = T
        params = np.zeros((len(T),3)); params[:,0] = T

        if slider:
            iter = tqdm(T)
        else:
            iter = T
        for i,t in enumerate(iter):
            partial_history = history[tis < t]
            best_LL, best_params, best_N_tot = -np.inf, None, np.inf
            for j in range(n_tries):
                try:
                    LL, param = estimator(partial_history, t)
                    if LL > best_LL:
                        N_tot = self.prediction(param, partial_history, t)
                        best_LL, best_params, best_N_tot = LL, param, N_tot
                except:
                    pass
            N[i,1], LLs[i,1], params[i,1:] = best_N_tot, best_LL, best_params
        return N, LLs, params