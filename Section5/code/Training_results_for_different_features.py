import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import (ensemble, linear_model,
                     neighbors,  svm)
import tensorflow as tf
import keras
from keras.losses import binary_crossentropy
import joblib
from sklearn.metrics import (accuracy_score, auc, f1_score, make_scorer,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve,precision_recall_curve)
import os
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
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class machinelearning():
    def __init__(self):
        self.lr = linear_model.LogisticRegressionCV()
        self.svm = svm.SVC()
        self.bagging = ensemble.BaggingClassifier()
        self.xgboost = XGBClassifier()
        self.lr_param = {
            'fit_intercept': [True, False],  # default: True
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag',
                       'saga'],  # default: lbfgs
            'random_state': [0],
            'max_iter': [10000]
        }
        self.svm_param = {
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'C': [1, 2, 3, 4, 5],  # default=1.0
            'gamma': [.1, .25, .5, .75, 1.0],  # edfault: auto
            'decision_function_shape': ['ovo', 'ovr'],  # default:ovr
            'probability': [True],
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

    def train(self, data, randomnum, name):
        '''
         :param data:Array data
        :param randomnum: Number of repetitions
        :return:
        '''

        # y=one_hot(y,depth=2)
        auclr = np.zeros(randomnum)
        aucsvm = np.zeros(randomnum)
        aucbagging = np.zeros(randomnum)
        aucxgb = np.zeros(randomnum)
        aucnn = np.zeros(randomnum)

        f1lr = np.zeros(randomnum)
        f1svm = np.zeros(randomnum)
        f1bagging = np.zeros(randomnum)
        f1xgb = np.zeros(randomnum)
        f1nn = np.zeros(randomnum)

        TPlr = np.zeros(randomnum)
        TPsvm = np.zeros(randomnum)
        TPbagging = np.zeros(randomnum)
        TPxgb = np.zeros(randomnum)
        TPnn = np.zeros(randomnum)

        FPlr = np.zeros(randomnum)
        FPsvm = np.zeros(randomnum)
        FPbagging = np.zeros(randomnum)
        FPxgb = np.zeros(randomnum)
        FPnn = np.zeros(randomnum)

        TNlr = np.zeros(randomnum)
        TNsvm = np.zeros(randomnum)
        TNbagging = np.zeros(randomnum)
        TNxgb = np.zeros(randomnum)
        TNnn = np.zeros(randomnum)

        FNlr = np.zeros(randomnum)
        FNsvm = np.zeros(randomnum)
        FNbagging = np.zeros(randomnum)
        FNxgb = np.zeros(randomnum)
        FNnn = np.zeros(randomnum)

        Truesample = np.zeros(randomnum)

        Falsesample = np.zeros(randomnum)

        for i in tqdm.tqdm(range(randomnum)):
            x = data[:, 1:]
            imputer = KNNImputer()
            x1 = imputer.fit_transform(x[:,1:])
            y = data[:, 0]
            if name == 'allfeature':
                _y = y
                trainsd_x = x[:, 1:int(1+len(y))].astype(np.float)
                trainotherx = x[:, int(1+len(y)):].astype(np.float)
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


            elif name == 'trans':
                _x = x[:, int(len(y))+5:int(len(y))+36].astype(np.float)
                _y = y.astype(np.int)
                train_x, test_x, train_y, test_y = train_test_split(_x, _y, train_size=0.8)

            elif name == 'ribo':
                _x = x[:, int(len(y))+36:int(len(y))+57].astype(np.float)
                _y = y.astype(np.int)
                train_x, test_x, train_y, test_y = train_test_split(_x, _y, train_size=0.8)
                test_y = test_y.astype(np.int)

            else:
                _x = x[:, 1:int(1+len(y))].astype(np.float)
                _y = y.astype(np.int)
                index = np.arange(len(_y))
                np.random.shuffle(index)
                randomcol = index[:int(0.8 * len(y))]
                valindex = index[int(0.8 * len(y)):]
                trainsd0_x = _x[:, randomcol]

                trainotherx = x[:, int(1+len(y)):int(1+len(y))+4].astype(np.float)
                newtrainx = np.concatenate((trainsd0_x, trainotherx), axis=1)
                train_x = newtrainx[randomcol]
                train_y = _y[randomcol]
                train_y = train_y.astype(np.int)
                test_x = newtrainx[valindex]
                test_y = _y[valindex]
                test_y = test_y.astype(np.int)


            Truesample[i] = sum(test_y == 1)
            Falsesample[i] = sum(test_y == 0)
            imputer = KNNImputer()
            train_x = imputer.fit_transform(train_x)
            test_x=imputer.fit_transform(test_x)

            if name == 'allfeature':
                trans_x = train_x[:, int(0.8 * len(y)+4):int(0.8 * len(y)+35)]
                ribo_x = train_x[:, int(0.8 * len(y)+35):int(0.8 * len(y)+56)]
                graph_x = train_x[:, 0:int(0.8 * len(y)+4)]
                test_trans_x = test_x[:, int(0.8 * len(y)+4):int(0.8 * len(y)+35)]
                test_ribo_x = test_x[:, int(0.8 * len(y)+35):int(0.8 * len(y)+56)]
                test_graph_x = test_x[:, 0:int(0.8 * len(y)+4)]
                inputs1 = Input(shape=(31,))
                inputs2 = Input(shape=(21,))
                inputs3 = Input(shape=(int(0.8 * len(y)+4),))
                x1 = Dense(50, activation='relu')(inputs1)

                x1 = Dropout(0.05)(x1)

                x2 = Dense(50, activation='relu')(inputs2)

                x2 = Dropout(0.05)(x2)

                x3 = Dense(100, activation='relu')(inputs3)

                x2 = Dropout(0.05)(x2)

                x = Concatenate()([x1, x2, x3])
                x = Dense(50, activation='relu')(x)

                x = Dense(10, activation='relu')(x)
                x = BatchNormalization()(x)

                out = Dense(1, activation='sigmoid')(x)
                model = keras.Model([inputs1, inputs2, inputs3], out)
                model.compile(optimizer='rmsprop', loss=binary_crossentropy, metrics=['accuracy'])
                from keras.callbacks import ModelCheckpoint
                filepath = 'nn.h5'
                isExists = os.path.exists('model')
                if not isExists:
                    os.mkdir('model')
                    print('model'+'创建成功')
                checkpoint = ModelCheckpoint(filepath,
                                             monitor='val_loss',
                                             verbose=0,
                                             save_best_only=True,
                                             save_weights_only=False,
                                             mode='auto',
                                             period=1
                                             )
                callbacks_list = [checkpoint]
                model.fit([trans_x, ribo_x, graph_x], train_y, batch_size=64, epochs=100, verbose=1,
                          validation_data=([test_trans_x, test_ribo_x, test_graph_x], test_y), callbacks=callbacks_list)

                nn = keras.models.load_model('nn.h5')

                predict = np.array(nn.predict([test_trans_x, test_ribo_x, test_graph_x]))
                predict[predict >= 0.5] = 1
                predict[predict < 0.5] = 0
                nnauc = roc_auc_score(test_y, nn.predict([test_trans_x, test_ribo_x, test_graph_x]))
                nnf1 = f1_score(test_y, predict)
                matrix = confusion_matrix(test_y, predict)
                TPnn[i] = matrix[1, 1]
                FPnn[i] = matrix[0, 1]
                TNnn[i] = matrix[0, 0]
                FNnn[i] = matrix[1, 0]
                aucnn[i] = nnauc
                f1nn[i] = nnf1

            elif name == 'trans':

                inputs1 = Input(shape=(31))
                x1 = Dense(100, activation='relu')(inputs1)
                x1 = BatchNormalization()(x1)

                x1 = Dense(50, activation='relu')(x1)
                x1 = BatchNormalization()(x1)

                x = Dense(50, activation='relu')(x1)
                x = BatchNormalization()(x)

                out = Dense(1, activation='sigmoid')(x)
                model = keras.Model(inputs1, out)
                model.compile(optimizer='rmsprop', loss=binary_crossentropy, metrics=['accuracy'])
                from keras.callbacks import ModelCheckpoint
                filepath = 'nn.h5'
                isExists = os.path.exists('model')
                if not isExists:
                    os.mkdir('model')
                checkpoint = ModelCheckpoint(filepath,
                                             monitor='val_loss',
                                             verbose=0,
                                             save_best_only=True,
                                             save_weights_only=False,
                                             mode='auto',
                                             period=1
                                             )
                callbacks_list = [checkpoint]
                model.fit(train_x, train_y, batch_size=64, epochs=70, verbose=1,
                          validation_data=(test_x, test_y), callbacks=callbacks_list)
                nn = keras.models.load_model('nn.h5')
                predict = np.array(nn.predict(test_x))
                predict[predict >= 0.5] = 1
                predict[predict < 0.5] = 0
                nnauc = roc_auc_score(test_y, nn.predict(test_x))
                nnf1 = f1_score(test_y, predict)
                aucnn[i] = nnauc
                f1nn[i] = nnf1

                matrix = confusion_matrix(test_y, predict)
                TPnn[i] = matrix[1, 1]
                FPnn[i] = matrix[0, 1]
                TNnn[i] = matrix[0, 0]
                FNnn[i] = matrix[1, 0]
            elif name == 'ribo':
                inputs2 = Input(shape=(21))
                x2 = Dense(100, activation='sigmoid')(inputs2)
                x2 = BatchNormalization()(x2)
                x2 = Dropout(0.1)(x2)
                x2 = Dense(50, activation='sigmoid')(x2)
                x2 = BatchNormalization()(x2)
                x2 = Dropout(0.1)(x2)
                x = Dense(50, activation='sigmoid')(x2)
                x = BatchNormalization()(x)
                x = Dropout(0.1)(x)
                out = Dense(1, activation='sigmoid')(x)
                model = keras.Model(inputs2, out)
                model.compile(optimizer='rmsprop', loss=binary_crossentropy, metrics=['accuracy'])
                model.summary()
                from keras.callbacks import ModelCheckpoint
                filepath = 'nn.h5'
                isExists = os.path.exists('model')
                if not isExists:
                    os.mkdir('model')
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
                aucnn[i] = nnauc
                f1nn[i] = nnf1

                matrix = confusion_matrix(test_y, predict)
                TPnn[i] = matrix[1, 1]
                FPnn[i] = matrix[0, 1]
                TNnn[i] = matrix[0, 0]
                FNnn[i] = matrix[1, 0]
            else:

                inputs3 = Input(shape=(int(0.8 * len(y)+4)))
                x3 = Dense(100, activation='relu')(inputs3)
                x3 = BatchNormalization()(x3)
                x3 = Dropout(0.1)(x3)
                x3 = Dense(50, activation='relu')(x3)
                x3 = BatchNormalization()(x3)
                x3 = Dropout(0.1)(x3)
                x = Dense(50, activation='relu')(x3)
                x = BatchNormalization()(x)
                x = Dropout(0.1)(x)
                out = Dense(1, activation='sigmoid')(x)
                model = keras.Model(inputs3, out)
                model.compile(optimizer='rmsprop', loss=binary_crossentropy, metrics=['accuracy'])

                from keras.callbacks import ModelCheckpoint
                filepath = 'model\\nn.h5'
                isExists = os.path.exists('model')
                if not isExists:
                    os.mkdir('model')
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
                aucnn[i] = nnauc
                f1nn[i] = nnf1

                matrix = confusion_matrix(test_y, predict)
                TPnn[i] = matrix[1, 1]
                FPnn[i] = matrix[0, 1]
                TNnn[i] = matrix[0, 0]
                FNnn[i] = matrix[1, 0]
            lr_gs = GridSearchCV(estimator=self.lr,
                                 param_grid=self.lr_param,
                                 cv=5,
                                 scoring='roc_auc',
                                 refit=True, n_jobs=-1)

            svm_gs = GridSearchCV(estimator=self.svm,
                                  param_grid=self.svm_param,
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
            svm_gs.fit(train_x, train_y)
            bagging_gs.fit(train_x, train_y)
            xgb_gs.fit(train_x, train_y)
            Blr = lr_gs.best_estimator_
            Bsvm = svm_gs.best_estimator_
            Bbagging = bagging_gs.best_estimator_
            Bxgb = xgb_gs.best_estimator_
            test_y_prob = tf.one_hot(test_y, depth=2)

            lrauc = roc_auc_score(test_y_prob, Blr.predict_proba(test_x))
            svmauc = roc_auc_score(test_y_prob, Bsvm.predict_proba(test_x))
            baggingauc = roc_auc_score(test_y_prob, Bbagging.predict_proba(test_x))
            xgbauc = roc_auc_score(test_y_prob, Bxgb.predict_proba(test_x))
            lrf1 = f1_score(test_y, Blr.predict(test_x))
            svmf1 = f1_score(test_y, Bsvm.predict(test_x))
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
        return auclr, aucsvm,  aucbagging, aucxgb, aucnn, f1lr,  f1svm,  f1bagging, f1xgb, f1nn, TPlr,  TPsvm, TPbagging, TPxgb, TPnn, FPlr,  FPsvm,  FPbagging, FPxgb, FPnn, TNlr,  TNsvm,  TNbagging, TNxgb, TNnn, FNlr,  FNsvm,  FNbagging, FNxgb, FNnn, Truesample, Falsesample


data = np.array(pd.read_excel('input.xlsx'))
allfeaturetrain = machinelearning()
traintype=['allfeature','trans','ribo','ppi']
for type in traintype:
    auclr, aucsvm,  aucbagging, aucxgb, aucnn, f1lr,  f1svm,  f1bagging, f1xgb, f1nn, TPlr,  TPsvm, TPbagging, TPxgb, TPnn, FPlr,  FPsvm,  FPbagging, FPxgb, FPnn, TNlr,  TNsvm,  TNbagging, TNxgb, TNnn, FNlr,  FNsvm,  FNbagging, FNxgb, FNnn, Truesample, Falsesample= allfeaturetrain.train(
    data, 20, type)
    aucdict = {'LR_AUC': auclr,
           'SVM_AUC': aucsvm,
           'Bagging_AUC': aucbagging,
           'XgBoost_AUC': aucxgb,
           'NeuralNet_AUC': aucnn,
           'LR_F1': f1lr,
           'SVM_F1': f1svm,
           'Bagging_F1': f1bagging,
           'XgBoost_F1': f1xgb,
           'NeuralNet_F1': f1nn,
           'LR_TP': TPlr,
           'SVM_TP': TPsvm,
           'Bagging_TP': TPbagging,
           'XgBoost_TP': TPxgb,
           'NeuralNet_TP': TPnn,
           'LR_FP': FPlr,
           'SVM_FP': FPsvm,
           'Bagging_FP': FPbagging,
           'XgBoost_FP': FPxgb,
           'NeuralNet_FP': FPnn,

           'LR_FN': FNlr,
           'SVM_FN': FNsvm,
           'Bagging_FN': FNbagging,
           'XgBoost_FN': FNxgb,
           'NeuralNet_FN': FNnn,
           'LR_TN': TNlr,
           'SVM_TN': TNsvm,
           'Bagging_TN': TNbagging,
           'XgBoost_TN': TNxgb,
           'NeuralNet_TN': TNnn,
           'Truesamples': Truesample,
           'Falsesamples': Falsesample

           }
    transdict = pd.DataFrame(aucdict).to_excel(str(type)+'auc_f1.xlsx')
