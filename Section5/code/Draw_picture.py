import os
import numpy as np
from scipy.interpolate import interp1d
import xgboost
from sklearn.model_selection import train_test_split
from sklearn import ensemble, linear_model,neighbors,  svm
from sklearn.ensemble import BaggingClassifier
import tensorflow as tf
import keras
from keras.losses import binary_crossentropy
import joblib
from sklearn.metrics import (accuracy_score, auc, f1_score, make_scorer,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve,precision_recall_curve)
from keras.layers import *
from imblearn.over_sampling import  ADASYN
import tqdm
from sklearn import preprocessing
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import  matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix
from plotnine import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
def tun_recall_precision(testy,testscore):
    threshold=np.arange(0,1,0.1)
    presicions=np.zeros(len(threshold))
    refcalls = np.zeros(len(threshold))
    a=0
    for i in threshold:
        y_predicted = testscore > i
        CM=confusion_matrix(testy, y_predicted)
        TN = CM[0][0]
        FN = CM[1][0]
        TP = CM[1][1]
        FP = CM[0][1]
        precision=TP/(TP+FP)
        recall=TP/(TP+FN)
        presicions[a]=precision
        refcalls[a]=recall
        a+=1
    return presicions,refcalls
def tune_ROC_curve(x,y):

    lr_param =  {
            'fit_intercept': [True, False],  # default: True
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag',
                       'saga'],  # default: lbfgs
            'random_state': [0],
            'max_iter':[10000]
        }
    lr = linear_model.LogisticRegressionCV()
    lr_gs = GridSearchCV(estimator=lr,
                         param_grid=lr_param,
                         cv=5,
                         scoring='roc_auc',
                         refit=True)
    aucs =np.zeros(20)
    mean_fpr = np.linspace(0, 1, 100)

    tprs = np.zeros((20, 100))
    a = 0
    for i in tqdm.tqdm(range(20)):
        _y = y
        trainsd_x = x[:, 1:69].astype(np.float)
        trainotherx = x[:, 69:].astype(np.float)
        index = np.arange(len(_y))
        np.random.shuffle(index)
        randomcol = index[:55]
        valindex = index[55:]
        trainsd0_x = trainsd_x[:, randomcol]
        newtrainx = np.concatenate((trainsd0_x, trainotherx), axis=1)
        train_x = newtrainx[randomcol]
        train_y = _y[randomcol]
        train_y = train_y.astype(np.int)
        test_x = newtrainx[valindex]
        val_y = _y[valindex]
        test_y = val_y.astype(np.int)
        lr_gs.fit(train_x, train_y)
        Blr = lr_gs.best_estimator_
        probas_ = Blr.predict_proba(test_x)
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(test_y, probas_[:, 1])
        f=(interp1d(fpr,tpr,fill_value="extrapolate"))
        tprs[i]=f(mean_fpr)
        tprs[-1][0] = 0
        testy_probs=tf.one_hot(test_y,depth=2)
        lrauc = roc_auc_score(testy_probs, Blr.predict_proba(test_x))
        aucs[i]=lrauc
        plt.plot(fpr,
                 tpr,
                 lw=1,
                 alpha=0.3,
                 label='ROC random %d (AUC = %0.2f)' % (i, lrauc))
        a += 1
    plt.plot([0, 1], [0, 1],
             linestyle='--',
             lw=2,
             color='r',
             label='Chance',
             alpha=.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1
    mean_auc = np.mean(aucs)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr,
             mean_tpr,
             color='b',
             label=r'Mean AUC (auc = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
             lw=2,
             alpha=.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr,
                     tprs_lower,
                     tprs_upper,
                     color='grey',
                     alpha=.2,
                     label=r'$\pm$ 1 std. dev.')

    plt.xlim([0, 1.05])
    plt.ylim([0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Tune Hyperparameter {} ROC'.format(
        Blr.__class__.__name__))
    plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0)
    # Hd output
    plt.tight_layout()
    # save picture
    plt.show()
    plt.clf()

def tune_PR_curve(x,y):

    lr_param =  {
            'fit_intercept': [True, False],  # default: True
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag',
                       'saga'],  # default: lbfgs
            'random_state': [0],
            'max_iter':[10000]
        }
    lr = linear_model.LogisticRegressionCV()
    lr_gs = GridSearchCV(estimator=lr,
                         param_grid=lr_param,
                         cv=5,
                         scoring='roc_auc',
                         refit=True)
    aucs =np.zeros(20)
    mean_fpr = np.linspace(0, 1, 100)

    tprs = np.zeros((20, 100))
    a = 0
    for i in tqdm.tqdm(range(20)):
        _y = y
        trainsd_x = x[:, 1:69].astype(np.float)
        trainotherx = x[:, 69:].astype(np.float)
        index = np.arange(len(_y))
        np.random.shuffle(index)
        randomcol = index[:55]
        valindex = index[55:]
        trainsd0_x = trainsd_x[:, randomcol]
        newtrainx = np.concatenate((trainsd0_x, trainotherx), axis=1)
        train_x = newtrainx[randomcol]
        train_y = _y[randomcol]
        train_y = train_y.astype(np.int)
        test_x = newtrainx[valindex]
        val_y = _y[valindex]
        test_y = val_y.astype(np.int)
        lr_gs.fit(train_x, train_y)
        Blr = lr_gs.best_estimator_
        probas_ = Blr.predict_proba(test_x)
        # Compute ROC curve and area the curve
        presicion, recall, thresholds = precision_recall_curve(test_y, probas_[:, 1])
        presicion[recall==0]=1
        # presicion, recall=tun_recall_precision(test_y,probas_[:,1])
        f=(interp1d(recall, presicion,fill_value="extrapolate"))
        tprs[i]=f(mean_fpr)
        tprs[-1][0] = 1
        lrauc = f1_score(test_y, Blr.predict(test_x))
        aucs[i]=lrauc
        plt.plot(recall,
                 presicion,
                 lw=1,
                 alpha=0.3,
                 label='F1 random %d (f1 = %0.2f)' % (i, lrauc))
        a += 1
    plt.plot([0, 1], [1, 0],
             linestyle='--',
             lw=2,
             color='r',
             label='Chance',
             alpha=.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 0
    mean_auc = np.mean(aucs)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr,
             mean_tpr,
             color='b',
             label=r'Mean F1 (F1 = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
             lw=2,
             alpha=.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr,
                     tprs_lower,
                     tprs_upper,
                     color='grey',
                     alpha=.2,
                     label=r'$\pm$ 1 std. dev.')

    plt.xlim([0, 1.05])
    plt.ylim([0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Tune Hyperparameter {} PR'.format(
        Blr.__class__.__name__))
    plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0)
    # Hd output
    plt.tight_layout()
    # save picture
    plt.show()
    plt.clf()
data=np.array(pd.read_excel('68dim\\train.xlsx'))
x = data[:, 1:]
y = data[:, 0].astype(np.int)
# tune_PR_curve(x,y)
tune_ROC_curve(x,y)