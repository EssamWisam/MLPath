"""
An example of using the mlpath package.
"""
# pylint: skip-file
from mlpath import mlquest as mlq
l = mlq.l

# let's try this out
def DatasetFilter(x_param, y_param, z_param, **kwargs):
    return x_param * y_param * z_param

def FeatureExtractor(p_num, k_num, l_num, **kwargs):
    return p_num**k_num + l_num

def NaiveBayes(alpha, beta_param, c=0, depth_ratio=4, **kwargs):
    return alpha + beta_param + c

def MultinomialNB( alpha=1.0, force_alpha='warn', fit_prior=True, class_prior=None):
    return 8

mlq.start('NaiveBayes')

dataset = l(DatasetFilter)(14, 510, 4, m_num=True, g_num=True, h_num=True)
features = l(FeatureExtractor)(12, 2, 12)
accuracy = l(NaiveBayes)(alpha=1024, beta_param=7, c=12,  depth_ratio=538, mega_p=63, g_estim=3, h=43)

mlq.to_log_ext('features', Type='Numerical' )

mlq.log_metrics(accuracy=accuracy)

mlq.end()


