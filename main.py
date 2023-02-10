"""
An example of using the mlpath package.
"""
# pylint: skip-file
from mlpath import mlquest as mlq
l = mlq.l

# let's try this out
# let's try this out
def NaiveBayes(alpha, beta_param, c=0, depth_ratio=4, a_num=5, b_gum=7, c_hum=12):
    return alpha + beta_param + c

def SVMRegressor(x_param, y_param, z_param, a_num=5, b_gum=7, c_hum=12):
    return x_param * y_param * z_param

def DeepNeuralNet(p_num, k_num, l_num, a_num=5, b_gum=7, c_hum=12):
    return p_num**k_num + l_num


mlq.start_quest('xyz', log_defs=True)

accuracy = mlq.l(NaiveBayes)(alpha=1024, beta_param=7, c=12, )
gesult = mlq.l(SVMRegressor)(14, 510, 4)
result = mlq.l(DeepNeuralNet)(12, 2, 3)

mlq.to_log_ext('features', Type='Numerical' )

mlq.log_metrics(accuracy=accuracy)

mlq.end_quest()


