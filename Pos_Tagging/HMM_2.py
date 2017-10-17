import numpy as np
from math import log


class HiddenMarkovModel:
    state, time_period, obs = 0, 0, 0

    def __init__(self, _state, _timeperiod, _obs):
        self.state, self.time_period, self.obs = _state, _timeperiod, _obs
        self.log = np.vectorize(log)

    def log_probabilty(self, C):
        return -np.sum(self.log(C))

    def forward(self, I, A, B, O):
        alpha = np.zeros(shape=(self.time_period, self.state))
        C = np.zeros(shape=self.time_period)
        for i in xrange(self.state):
            alpha[0][i] = I[i]*B[i][O[0]]
            C[0]+=alpha[0][i]
        C[0] = 1/alpha[0].sum()
        for i in xrange(self.state):
            alpha[0][i] = alpha[0][i] * C[0]
        for t in xrange(1, self.time_period):
            for i in xrange(self.state):
                for j in xrange(self.state):
                    alpha[t][i] += alpha[t-1][j]*A[j][i]
                    C[t]+=alpha[t][i]
            C[t] = 1/C[t]
            for i in xrange(self.state):
                alpha[t][i] = alpha[t][i] / C[t]
        return alpha, C

    def backward(self, I, A, B, O, C=[]):
        if C.shape[0] == 0:
            C = np.ones(self.time_period)
        beta = np.zeros(shape=(self.time_period, self.state))
        beta[self.time_period-1][:] = np.ones(self.state)*C[self.time_period - 1]
        for t in xrange(self.time_period - 2, -1, -1):
            for i in xrange(self.state):
                for j in xrange(self.state):
                    beta[t][i] += A[i][j]*B[j][O[t+1]]*beta[t+1][j]
                beta[t][i]*=C[t]
        return beta

    def forward_backward(self, I, A, B, O, maxiters=10):
        oldLog = -float("inf")
        for iter in xrange(maxiters):
            alpha, C = self.forward(I, A, B, O)
            print alpha[1][:], C[:6]
            beta = self.backward(I, A, B, O, C)
            gamma = np.zeros(shape=(self.time_period, self.state, self.state))
            Gamma = np.zeros(shape=(self.time_period, self.state))
            for t in xrange(self.time_period - 1):
                #gamma[t][:][:] = np.multiply(A, np.matrix(alpha[t]).transpose() * np.matrix(np.multiply(beta[t + 1][:], B[:][O[t + 1]])))
                den = 0
                for i in xrange(self.state):
                    for j in xrange(self.state):
                        gamma[t][i][j] = alpha[t][i]*A[i][j]*B[j][O[t+1]]*beta[t+1][j]
                        den += gamma[t][i][j];
                for i in xrange(self.state):
                    for j in xrange(self.state):
                        gamma[t][i][j]/=den
                for i in xrange(self.state):
                    for j in xrange(self.state):
                        Gamma[t][i] += gamma[t][i][j]
            print gamma[1][:][:].sum() , Gamma[2].sum()
            #gamma[:][:][:] = gamma[:][:][:] / gamma[:][:][:].sum()
            # did not sum alpha as they are normalized in each time instant
            print "sum of last alpha", alpha[self.time_period-1].sum()
            Gamma[self.time_period - 1][:] = alpha[self.time_period - 1][:]

            # resetimate
            I, A, B = 0 * I, 0 * A, 0 * B.transpose()
            I = Gamma[0]
            print I
            for i in xrange(self.state):
                for j in xrange(self.state):
                    d = 0;
                    for t in xrange(self.time_period-1):
                        A[i][j] += gamma[t][i][j]
                        d+=Gamma[t][i]
                A[i][j] /= d
            ##differs
            for i in xrange(self.state):
                d = 0
                for t in xrange(self.time_period):
                    B[i][O[t]] += Gamma[t][i]
                    d += Gamma[t][i]
                for j in xrange(self.obs):
                    B[i][j] = B[i][j] / d
            ##ends
            logP = self.log_probabilty(C)
            print "log_probability",logP
            print A
            if logP <= oldLog:
                break;
            oldLog = logP
        return I,A,B
