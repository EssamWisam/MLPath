"""
An example of using the mlpath package.
"""
# pylint: skip-file
from mlpath import mlquest as mlq

# let's try this out
def NaiveBayes(alpha, beta_param, c=0, depth_ratio=4, **kwargs):
    return alpha + beta_param + c

def SVMRegressor(x_param, y_param, z_param, **kwargs):
    return x_param * y_param * z_param

def DeepNeuralNet(p_num, k_num, l_num, **kwargs):
    return p_num**k_num + l_num

mlq.start('NB-SVM-DNN')

#accuracy = mlq.l(NaiveBayes)(alpha=1024, beta_param=7, c=12,  depth_ratio=538, mega_p=63, g_estim=3, h=43)
#gesult = mlq.l(SVMRegressor)(14, 510, 4, m_num=63, g_num=3, h_num=4)
result = mlq.l(DeepNeuralNet)(12, 2, 12)

mlq.log_metrics(result=result)

mlq.end()


