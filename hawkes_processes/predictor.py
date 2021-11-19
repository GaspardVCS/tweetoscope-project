import numpy as np

class Predictor:
    def __init__(self):
        self.alpha = 2.4
        self.mu = 10

    def estimate_param(history):
        pass

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