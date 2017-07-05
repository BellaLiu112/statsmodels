import summary_stats as ss
import pandas as pd
import numpy as np
from numpy.testing import (assert_almost_equal, assert_equal, assert_array_less,
                           assert_raises, assert_allclose)

strata = np.r_[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
cluster = np.r_[0, 0, 2, 2, 3, 3, 4, 4, 4, 6, 6, 6]
weights = np.r_[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2].astype(np.float64)
data = np.asarray([[1, 3, 2, 5, 4, 1, 2, 3, 4, 6, 9, 5],
                   [5, 3, 2, 1, 4, 7, 8, 9, 5, 4, 3, 5]], dtype=np.float64).T
design = ss.SurveyDesign(strata, cluster, weights)

def test_design():
    assert_equal(design.ncs, np.array([2, 3]))
    assert_equal(design.sfclust, np.array([0, 0, 1, 1, 1]))
    assert(len(np.unique(design.sclust)) == len(np.unique(cluster)))

def test_mean_jack():
    avg = ss.SurveyMean(design, data, 'jack')
    assert_allclose(avg.est, np.r_[3.777778, 4.722222])
    assert_allclose(avg.vc, np.r_[0.9029327, 1.061515],  rtol=1e-5, atol=0)

# def test_mean_boot():
#     avg = ss.SurveyMean(design, data, 'boot')
#     assert_allclose(avg.est, np.r_[0, 0])
#     assert_allclose(avg.vc, np.r_[0, 0], rtol=1e-5, atol=0)

def test_total_jack():
    tot = ss.SurveyTotal(design, data, 'jack')
    assert_allclose(tot.est, np.r_[68, 85])
    assert_allclose(tot.vc, np.r_[19.79899, 15.71623],  rtol=1e-5, atol=0)

# def test_total_boot():
#     tot = ss.SurveyTotal(design, data, 'boot')
#     assert_allclose(tot.est, np.r_[68, 85])
#     assert_allclose(tot.vc, np.r_[19.79899, 15.71623],  rtol=1e-5, atol=0)

def test_quantile_jack():
    quant = ss.SurveyQuantile(design, data, [.1, .25, .33, .5, .75, .99], 'jack')
    assert_allclose(quant.est[0], np.r_[1, 2, 2, 3.5, 5, 9])
    ## change 7 to 6 to accommodate w/ stata
    assert_allclose(quant.est[1], np.r_[2, 3, 3, 4.5, 7, 9])

    # ensure that median yields same result
    med = ss.SurveyMedian(design, data, 'jack')
    assert_equal(quant.est[0][-3], med.est[0][0])
    assert_equal(quant.est[1][-3], med.est[1][0])

# def test_quantile_boot():
#     quant = ss.SurveyQuantile(design, data, [.1, .25, .33, .5, .75, .99], 'boot')
#     assert_allclose(quant.est[0], np.r_[1, 2, 2, 3.5, 5, 9])
#     ## change 7 to 6 to accommodate w/ stata
#     assert_allclose(quant.est[1], np.r_[2, 3, 3, 4.5, 7, 9])

#     # ensure that median yields same result
#     med = ss.SurveyMedian(design, data, 'boot')
#     assert_equal(quant.est[0][-3], med.est[0][0])
#     assert_equal(quant.est[1][-3], med.est[1][0])
