import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import (ensemble, linear_model,
                     neighbors,  svm)
import sys
import os
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
class machinelearning():
    def __init__(self):
        self.lr = linear_model.LogisticRegressionCV()
        self.knn = neighbors.KNeighborsClassifier()
        self.svm = svm.SVC()
        self.adaboost = ensemble.AdaBoostClassifier()
        self.bagging = ensemble.BaggingClassifier()
        self.xgboost = XGBClassifier()
        self.lr_param = {
            'fit_intercept': [True, False],  # default: True
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag',
                       'saga'],  # default: lbfgs
            'random_state': [0],
            'max_iter': [10000000]
        }
        self.knn_param = {
            'n_neighbors': [1, 2, 3, 4, 5, 6, 7],  # default: 5
            'weights': ['uniform', 'distance'],  # default = ‘uniform’
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
        }
        self.svm_param = {
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'C': [1, 2, 3, 4, 5],  # default=1.0
            'gamma': [.1, .25, .5, .75, 1.0],  # edfault: auto
            'decision_function_shape': ['ovo', 'ovr'],  # default:ovr
            'probability': [True],
            'random_state': [0]
        }
        self.adaboost_param = {
            'n_estimators': [10, 50, 100, 300],  # default=50
            'learning_rate': [.01, .03, .05, .1, .25],  # default=
            'random_state': [0]
        }
        self.bagging_param = {
            'n_estimators': [10, 50, 100, 300],  # default=10
            'max_samples': [.1, .25, .5, .75, 1.0],  # default=1.0
            'random_state': [0]
        }

        self.xgb_param = {
            'learning_rate': [.01, .03, .05, .1, .25],  # default: .3
            'max_depth': [1, 2, 4, 6, 8, 10],  # default 2
            'n_estimators': [10, 50, 100, 300],
            'seed': [0]
        }

    def train(self, data, randomnum):
        '''
        :param data:Array data
        :param randomnum: Number of repetitions
        :return:
        '''
        auclr = np.zeros(randomnum)
        aucknn = np.zeros(randomnum)
        aucsvm = np.zeros(randomnum)
        aucada = np.zeros(randomnum)
        aucbagging = np.zeros(randomnum)
        aucxgb = np.zeros(randomnum)
        aucnn = np.zeros(randomnum)

        f1lr = np.zeros(randomnum)
        f1knn = np.zeros(randomnum)
        f1svm = np.zeros(randomnum)
        f1ada = np.zeros(randomnum)
        f1bagging = np.zeros(randomnum)
        f1xgb = np.zeros(randomnum)
        f1nn = np.zeros(randomnum)

        TPlr = np.zeros(randomnum)
        TPknn = np.zeros(randomnum)
        TPsvm = np.zeros(randomnum)
        TPada = np.zeros(randomnum)
        TPbagging = np.zeros(randomnum)
        TPxgb = np.zeros(randomnum)
        TPnn = np.zeros(randomnum)

        FPlr = np.zeros(randomnum)
        FPknn = np.zeros(randomnum)
        FPsvm = np.zeros(randomnum)
        FPada = np.zeros(randomnum)
        FPbagging = np.zeros(randomnum)
        FPxgb = np.zeros(randomnum)
        FPnn = np.zeros(randomnum)

        TNlr = np.zeros(randomnum)
        TNknn = np.zeros(randomnum)
        TNsvm = np.zeros(randomnum)
        TNada = np.zeros(randomnum)
        TNbagging = np.zeros(randomnum)
        TNxgb = np.zeros(randomnum)
        TNnn = np.zeros(randomnum)
        FNlr = np.zeros(randomnum)
        FNknn = np.zeros(randomnum)
        FNsvm = np.zeros(randomnum)
        FNada = np.zeros(randomnum)
        FNbagging = np.zeros(randomnum)
        FNxgb = np.zeros(randomnum)
        FNnn = np.zeros(randomnum)

        Truesample = np.zeros(randomnum)
        Falsesample = np.zeros(randomnum)

        for i in tqdm.tqdm(range(randomnum)):  #####重复做
            x = data[:, 1:]
            y = data[:, 0]
            _y = y
            trainsd_x = x[:, 1:int(len(y)+1)].astype(np.float)
            trainotherx = x[:, int(len(y)+1):].astype(np.float)
            index = np.arange(len(_y))
            np.random.shuffle(index)
            randomcol = index[:int(0.8*len(y))]
            valindex = index[int(0.8*len(y)):]
            trainsd0_x = trainsd_x[:, randomcol]
            newtrainx = np.concatenate((trainsd0_x, trainotherx), axis=1)
            train_x = newtrainx[randomcol]
            train_y = _y[randomcol]
            train_y = train_y.astype(np.int)
            test_x = newtrainx[valindex]
            val_y = _y[valindex]
            test_y = val_y.astype(np.int)
            scalr = preprocessing.MinMaxScaler()
            train_x = scalr.fit_transform(train_x)
            test_x = scalr.transform(test_x)

            Truesample[i] = sum(test_y == 1)
            Falsesample[i] = sum(test_y == 0)


            inputs3 = Input(shape=(int(0.8*len(y)+4),))
            x3 = Dense(100, activation='relu')(inputs3)
            x3 = Dropout(0.05)(x3)
            x = Dense(50, activation='relu')(x3)
            x = Dense(10, activation='relu')(x)
            out = Dense(1, activation='sigmoid')(x)
            model = keras.Model( inputs3,out)
            model.compile(optimizer='rmsprop', loss=binary_crossentropy, metrics=['accuracy'])
            from keras.callbacks import ModelCheckpoint
            filepath = 'nn.h5'  ####原最佳模型7dimmodelATT_TCNnew.h5
            checkpoint = ModelCheckpoint(filepath,
                                             monitor='val_loss',
                                             verbose=0,
                                             save_best_only=True,
                                             save_weights_only=False,
                                             mode='auto',
                                             period=1
                                             )
            callbacks_list = [checkpoint]
            model.fit(train_x, train_y, batch_size=64, epochs=100, verbose=1,
                          validation_data=(test_x, test_y), callbacks=callbacks_list)

            nn = keras.models.load_model('nn.h5')

            predict = np.array(nn.predict(test_x))
            predict[predict >= 0.5] = 1
            predict[predict < 0.5] = 0
            nnauc = roc_auc_score(test_y, nn.predict(test_x))
            nnf1 = f1_score(test_y, predict)
            matrix = confusion_matrix(test_y, predict)
            TPnn[i] = matrix[1, 1]
            FPnn[i] = matrix[0, 1]
            TNnn[i] = matrix[0, 0]
            FNnn[i] = matrix[1, 0]
            aucnn[i] = nnauc
            f1nn[i] = nnf1

            lr_gs = GridSearchCV(estimator=self.lr,
                                 param_grid=self.lr_param,
                                 cv=5,
                                 scoring='roc_auc',
                                 refit=True, n_jobs=-1)
            knn_gs = GridSearchCV(estimator=self.knn,
                                  param_grid=self.knn_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True, n_jobs=-1)
            svm_gs = GridSearchCV(estimator=self.svm,
                                  param_grid=self.svm_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True, n_jobs=-1)
            ada_gs = GridSearchCV(estimator=self.adaboost,
                                  param_grid=self.adaboost_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True, n_jobs=-1)
            bagging_gs = GridSearchCV(estimator=self.bagging,
                                      param_grid=self.bagging_param,
                                      cv=5,
                                      scoring='roc_auc',
                                      refit=True, n_jobs=-1)
            xgb_gs = GridSearchCV(estimator=self.xgboost,
                                  param_grid=self.xgb_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True, n_jobs=-1)


            lr_gs.fit(train_x, train_y)
            knn_gs.fit(train_x, train_y)
            svm_gs.fit(train_x, train_y)
            ada_gs.fit(train_x, train_y)
            bagging_gs.fit(train_x, train_y)
            xgb_gs.fit(train_x, train_y)
            Blr = lr_gs.best_estimator_
            Bknn = knn_gs.best_estimator_
            Bsvm = svm_gs.best_estimator_
            Bada = ada_gs.best_estimator_
            Bbagging = bagging_gs.best_estimator_
            Bxgb = xgb_gs.best_estimator_
            test_y_prob = tf.one_hot(test_y, depth=2)

            lrauc = roc_auc_score(test_y_prob, Blr.predict_proba(test_x))
            knnauc = roc_auc_score(test_y_prob, Bknn.predict_proba(test_x))
            svmauc = roc_auc_score(test_y_prob, Bsvm.predict_proba(test_x))
            adaauc = roc_auc_score(test_y_prob, Bada.predict_proba(test_x))
            baggingauc = roc_auc_score(test_y_prob, Bbagging.predict_proba(test_x))
            xgbauc = roc_auc_score(test_y_prob, Bxgb.predict_proba(test_x))
            lrf1 = f1_score(test_y, Blr.predict(test_x))
            knnf1 = f1_score(test_y, Bknn.predict(test_x))
            svmf1 = f1_score(test_y, Bsvm.predict(test_x))
            adaf1 = f1_score(test_y, Bada.predict(test_x))
            baggingf1 = f1_score(test_y, Bbagging.predict(test_x))
            xgbf1 = f1_score(test_y, Bxgb.predict(test_x))

            auclr[i] = lrauc
            f1lr[i] = lrf1
            matrix = confusion_matrix(test_y, Blr.predict(test_x))
            TPlr[i] = matrix[1, 1]
            FPlr[i] = matrix[0, 1]
            TNlr[i] = matrix[0, 0]
            FNlr[i] = matrix[1, 0]

            if lrauc > auclr[i - 1] and i >= 1:
                joblib.dump(Blr, 'model\\lr.pkl')
            elif i == 0:
                joblib.dump(Blr, 'model\\lr.pkl')
            aucknn[i] = knnauc
            f1knn[i] = knnf1
            matrix = confusion_matrix(test_y, Bknn.predict(test_x))
            TPknn[i] = matrix[1, 1]
            FPknn[i] = matrix[0, 1]
            TNknn[i] = matrix[0, 0]
            FNknn[i] = matrix[1, 0]

            if knnauc > aucknn[i - 1] and i >= 1:
                joblib.dump(Bknn, 'model\\knn.pkl')
            elif i == 0:
                joblib.dump(Bknn, 'model\\knn.pkl')
            aucsvm[i] = svmauc
            f1svm[i] = svmf1
            matrix = confusion_matrix(test_y, Bsvm.predict(test_x))
            TPsvm[i] = matrix[1, 1]
            FPsvm[i] = matrix[0, 1]
            TNsvm[i] = matrix[0, 0]
            FNsvm[i] = matrix[1, 0]

            if svmauc > aucsvm[i - 1] and i >= 1:
                joblib.dump(Bsvm, 'model\\svm.pkl')
            elif i == 0:
                joblib.dump(Bsvm, 'model\\svm.pkl')
            aucada[i] = adaauc
            f1ada[i] = adaf1
            matrix = confusion_matrix(test_y, Bada.predict(test_x))
            TPada[i] = matrix[1, 1]
            FPada[i] = matrix[0, 1]
            TNada[i] = matrix[0, 0]
            FNada[i] = matrix[1, 0]

            if adaauc > aucada[i - 1] and i >= 1:
                joblib.dump(Bada, 'model\\ada.pkl')
            elif i == 0:
                joblib.dump(Bada, 'model\\ada.pkl')
            aucbagging[i] = baggingauc
            f1bagging[i] = baggingf1
            matrix = confusion_matrix(test_y, Bbagging.predict(test_x))
            TPbagging[i] = matrix[1, 1]
            FPbagging[i] = matrix[0, 1]
            TNbagging[i] = matrix[0, 0]
            FNbagging[i] = matrix[1, 0]
            if baggingauc > aucbagging[i - 1] and i >= 1:
                joblib.dump(Bbagging, 'model\\bagging.pkl')
            elif i == 0:
                joblib.dump(Bbagging, 'model\\bagging.pkl')
            aucxgb[i] = xgbauc
            f1xgb[i] = xgbf1
            matrix = confusion_matrix(test_y, Bxgb.predict(test_x))
            TPxgb[i] = matrix[1, 1]
            FPxgb[i] = matrix[0, 1]
            TNxgb[i] = matrix[0, 0]
            FNxgb[i] = matrix[1, 0]
            if xgbauc > aucxgb[i - 1] and i >= 1:
                joblib.dump(Bxgb, 'model\\xgb.pkl')
            elif i == 0:
                joblib.dump(Bxgb, 'model\\xgb.pkl')
        return auclr, aucknn, aucsvm, aucada, aucbagging, aucxgb, aucnn, f1lr, f1knn, f1svm, f1ada, f1bagging, f1xgb, f1nn, TPlr, TPknn, TPsvm, TPada, TPbagging, TPxgb, TPnn, FPlr, FPknn, FPsvm, FPada, FPbagging, FPxgb, FPnn, TNlr, TNknn, TNsvm, TNada, TNbagging, TNxgb, TNnn, FNlr, FNknn, FNsvm, FNada, FNbagging, FNxgb, FNnn, Truesample, Falsesample
# path = os.getcwd()
# DataSet = pd.read_excel(sys.argv,index_col='gene')
data=np.array(pd.read_excel('transsd.xlsx'))
allfeaturetrain=machinelearning()
auclr,aucknn,aucsvm,aucada,aucbagging,aucxgb,aucnn,f1lr,f1knn,f1svm,f1ada,f1bagging,f1xgb,f1nn,TPlr,TPknn,TPsvm,TPada,TPbagging,TPxgb,TPnn,FPlr,FPknn,FPsvm,FPada,FPbagging,FPxgb,FPnn,TNlr,TNknn,TNsvm,TNada,TNbagging,TNxgb,TNnn,FNlr,FNknn,FNsvm,FNada,FNbagging,FNxgb,FNnn,Truesample,Falsesample=allfeaturetrain.train(data,20)
aucdict = {'LR_AUC': auclr,
           'KNN_AUC': aucknn,
           'SVM_AUC': aucsvm,
           'AdaBoost_AUC': aucada,
           'Bagging_AUC': aucbagging,
           'XgBoost_AUC': aucxgb,
           'NeuralNet_AUC': aucnn,
           'LR_F1': f1lr,
           'KNN_F1': f1knn,
           'SVM_F1': f1svm,
           'AdaBoost_F1': f1ada,
           'Bagging_F1': f1bagging,
           'XgBoost_F1': f1xgb,
           'NeuralNet_F1': f1nn,
           'LR_TP': TPlr,
           'KNN_TP': TPknn,
           'SVM_TP': TPsvm,
           'AdaBoost_TP': TPada,
           'Bagging_TP': TPbagging,
           'XgBoost_TP': TPxgb,
           'NeuralNet_TP': TPnn,
           'LR_FP': FPlr,
           'KNN_FP': FPknn,
           'SVM_FP': FPsvm,
           'AdaBoost_FP': FPada,
           'Bagging_FP': FPbagging,
           'XgBoost_FP': FPxgb,
           'NeuralNet_FP': FPnn,

           'LR_FN': FNlr,
           'KNN_FN': FNknn,
           'SVM_FN': FNsvm,
           'AdaBoost_FN': FNada,
           'Bagging_FN': FNbagging,
           'XgBoost_FN': FNxgb,
           'NeuralNet_FN': FNnn,
           'LR_TN': TNlr,
           'KNN_TN': TNknn,
           'SVM_TN': TNsvm,
           'AdaBoost_TN': TNada,
           'Bagging_TN': TNbagging,
           'XgBoost_TN': TNxgb,
           'NeuralNet_TN': TNnn,
           'Truesamples': Truesample,
           'Falsesamples': Falsesample

           }
allfeaturedict = pd.DataFrame(aucdict).to_excel('transsdauc_f1.xlsx')
