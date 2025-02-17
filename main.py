import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import tm_sim

      
        
def empirical(max, tm, accept, start):
    df = pd.DataFrame(columns=["n", "t"])
    one = "1"
    for i in range(1,max):
        n = "_"+i*one
        tape = tm_sim.tokenize(n)
        t_n = tm_sim.sim(tm,tape, start, accept, showConfig=False)
        df = pd.concat([df, pd.DataFrame({"n": [i], "t": [t_n]})], ignore_index=True)
    return df

def analysis(max, tm, accept, start):
    time_analysis = analysis(13,tm,accept,start)
    X = time_analysis["n"].values
    Y = time_analysis['t'].values
    def exp_function(x, a):
        return a**x
    params, _ = curve_fit(exp_function, X, Y)
    a_best = params[0]
    y_pred = exp_function(X, a_best)

    r2_exp = r2_score(Y, y_pred)
    print(f"Exponential Regression (a^x) Best a: {a_best:.4f}, R² Score: {r2_exp:.4f}")

    plt.scatter(x=time_analysis['n'],y=time_analysis['t'])
    plt.plot(X, y_pred, color="green", label=f"Exp Fit (a={a_best:.2f}^x)")
    plt.legend()
    plt.show()
    
def print_seq(tape):
    rslt = ""
    for ch in tape:
        rslt+=ch
    unary = rslt.split("#")
    fib = []
    for un in unary:
        if not ("%" in un):
            fib.append(len(un))
            
    print(fib)
def test(tm, accept, start, input, ret):
    tape = tm_sim.tokenize(input)
    accept,start,TM = tm_sim.gen_tm('./transitions.txt')
    showconfig = True
    ret = ""
    rslt = tm_sim.sim(tm,tape,start,accept,showconfig,ret)
    return rslt


accept,start,TM = tm_sim.gen_tm('./transitions.txt')
