import numpy as np
import sklearn.svm
from sklearn.model_selection import train_test_split
from sklearn import (ensemble, linear_model,
                     neighbors, svm)
from imblearn.over_sampling import  ADASYN
from sklearn.metrics import confusion_matrix
import tensorflow as tf
import keras
from keras.losses import binary_crossentropy
import joblib
from sklearn.metrics import (accuracy_score, auc, f1_score, make_scorer,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve, precision_recall_curve)
from keras.layers import *
from sklearn.impute import KNNImputer
import tqdm
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from plotnine import *
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
class machinelearning():
    def __init__(self):
        self.lr = linear_model.LogisticRegressionCV()
        self.knn = neighbors.KNeighborsClassifier()
        self.svm = svm.SVC(probability=True)
        self.adaboost = ensemble.AdaBoostClassifier()
        self.bagging = ensemble.BaggingClassifier()
        self.xgboost = XGBClassifier()
        self.lr_param = {
            'fit_intercept': [True, False],  # default: True
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag',
                       'saga'],  # default: lbfgs
            'random_state': [0],
            'max_iter': [10000]
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

    def train(self, traindata,testdata):
        '''
        :param data:Array data
        :param randomnum: Number of repetitions
        :return:
        '''
        _y = traindata[:, 0]
        trainsd_x = traindata[:, 2:int(len(_y)+2)]
        trainotherx=traindata[:,int(len(_y)+2):]

        testsd_x=testdata[:,1:int(len(_y)+1)]
        testotherx=testdata[:,int(len(_y)+1):]

        index=np.arange(len(_y))
        np.random.shuffle(index)
        randomcol=index[:int(0.8*len(_y))]
        valindex=index[int(0.8*len(_y)):]
        trainsd0_x=trainsd_x[:,randomcol]
        testsd0_x=testsd_x[:,randomcol]

        newtrainx=np.concatenate((trainsd0_x,trainotherx),axis=1)
        newtestx=np.concatenate((testsd0_x,testotherx),axis=1)

        nanindert=KNNImputer()
        newtrainx=nanindert.fit_transform(newtrainx)
        newtestx=nanindert.fit_transform(newtestx)
        train_x=newtrainx[randomcol]
        train_y=_y[randomcol]
        train_y=train_y.astype(np.int)
        val_x=newtrainx[valindex]
        val_y=_y[valindex]
        val_y=val_y.astype(np.int)

        sd_trainx = train_x[:, 0:int(0.8*len(_y)+4)]
        trans_trainx = train_x[:, int(0.8*len(_y)+4):int(0.8*len(_y)+35)]
        ribo_trainx=train_x[:,int(0.8*len(_y)+35):int(0.8*len(_y)+56)]
        sd_valx=val_x[:, 0:int(0.8*len(_y)+4)]
        trans_valx=val_x[:, int(0.8*len(_y)+4):int(0.8*len(_y)+35)]
        ribo_valx=val_x[:,int(0.8*len(_y)+35):int(0.8*len(_y)+56)]
        sd_testx = newtestx[:, 0:int(0.8*len(_y)+4)]

        trans_testx = newtestx[:, int(0.8*len(_y)+4):int(0.8*len(_y)+35)]
        ribo_testx = newtestx[:,int(0.8*len(_y)+35):int(0.8*len(_y)+56)]



        inputs3 = Input(shape=(int(0.8*len(_y)+4),))
        inputs1 = Input(shape=(31,))
        inputs2 = Input(shape=(21,))

        x1 = Dense(100, activation='relu')(inputs1)
        x1 = Dropout(0.1)(x1)
        x2 = Dense(50, activation='relu')(inputs2)
        x2 = Dropout(0.1)(x2)
        x3 = Dense(50, activation='relu')(inputs3)

        x3 = Dropout(0.1)(x3)

        x = Concatenate()([x1, x2, x3])
        x = Dense(50, activation='relu')(x)


        out = Dense(1, activation='sigmoid')(x)
        model = keras.Model([inputs1, inputs2, inputs3], out)
        model.compile(optimizer='adam', loss=binary_crossentropy, metrics=['accuracy'])
        from keras.callbacks import ModelCheckpoint
        filepath = 'nn677.h5'
        checkpoint = ModelCheckpoint(filepath,
                                             monitor='val_loss',
                                             verbose=0,
                                             save_best_only=True,
                                             save_weights_only=False,
                                             mode='auto',
                                             period=1
                                             )
        callbacks_list = [checkpoint]
        model.fit([ trans_trainx, ribo_trainx,sd_trainx], train_y, batch_size=64, epochs=500, verbose=1,
                          validation_data=([ trans_valx, ribo_valx,sd_valx], val_y), callbacks=callbacks_list)
        nn = keras.models.load_model('nn677.h5')
        nntesty = nn.predict([trans_testx, ribo_testx,sd_testx])
        nntesty = nntesty.reshape(len(nntesty), )

        lr_gs = GridSearchCV(estimator=self.lr,
                                 param_grid=self.lr_param,
                                 cv=5,
                                 scoring='roc_auc',
                                 refit=True)
        knn_gs = GridSearchCV(estimator=self.knn,
                                  param_grid=self.knn_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True)
        svm_gs = GridSearchCV(estimator=self.svm,
                                  param_grid=self.svm_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True)
        ada_gs = GridSearchCV(estimator=self.adaboost,
                                  param_grid=self.adaboost_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True)
        bagging_gs = GridSearchCV(estimator=self.bagging,
                                      param_grid=self.bagging_param,
                                      cv=5,
                                      scoring='roc_auc',
                                      refit=True)
        xgb_gs = GridSearchCV(estimator=self.xgboost,
                                  param_grid=self.xgb_param,
                                  cv=5,
                                  scoring='roc_auc',
                                  refit=True)
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
        adatesty = Bada.predict_proba(newtestx)[:, 1]
        baggingtesty = Bbagging.predict_proba(newtestx)[:, 1]
        knntesty = Bknn.predict_proba(newtestx)[:, 1]
        lrtesty = Blr.predict_proba(newtestx)[:, 1]
        svmtesty = Bsvm.predict_proba(newtestx)[:, 1]
        xgbtesty = Bxgb.predict_proba(newtestx)[:, 1]
        return nntesty,adatesty,baggingtesty,knntesty,lrtesty,svmtesty,xgbtesty

traindata=np.array(pd.read_excel('train.xlsx'))
testdata=np.array((pd.read_excel('test.xlsx')))
model=machinelearning()
nntesty0=np.zeros((int(testdata.shape[0]),))
adatesty0=np.zeros((int(testdata.shape[0]),))
baggingtesty0=np.zeros((int(testdata.shape[0]),))
knntesty0=np.zeros((int(testdata.shape[0]),))
lrtesty0=np.zeros((int(testdata.shape[0]),))
svmtesty0=np.zeros((int(testdata.shape[0]),))
xgbtesty0=np.zeros((int(testdata.shape[0]),))
for i in tqdm.tqdm(range(20)):
   nntesty,adatesty,baggingtesty,knntesty,lrtesty,svmtesty,xgbtesty=model.train(traindata,testdata)
   nntesty0+=nntesty
   adatesty0+=adatesty
   baggingtesty0+=baggingtesty
   knntesty0+=knntesty
   lrtesty0+=lrtesty
   svmtesty0+=svmtesty
   xgbtesty0+=xgbtesty
dict={'nnpredresult':nntesty0/20,
      'adapredresult':adatesty0/20,
      'baggingpredresult':baggingtesty0/20,
      'knnpredresult':knntesty0/20,
      'lrpredresult':lrtesty0/20,
      'svmpredresult':svmtesty0/20,
      'xgbpredresult':xgbtesty0/20,
      'Gene':testdata[:,0]}
result=pd.DataFrame(dict).to_excel('predresult.xlsx')

###export importance of features
data=pd.DataFrame(pd.read_excel('train.xlsx')) ##input train data
featurename=list(data.columns)[2:]
x=np.array(data)[:,2:].astype(np.float)
y=np.array(data)[:,0].astype(np.int)
train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.8)
lr_param = {
            'fit_intercept': [True, False],  # default: True
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag',
                       'saga'],  # default: lbfgs
            'random_state': [0],
            'max_iter': [10000]}
lr=linear_model.LogisticRegressionCV()
lr_gs = GridSearchCV(estimator=lr,
                                 param_grid=lr_param,
                                 cv=5,
                                 scoring='roc_auc',
                                 refit=True)
lr_gs.fit(train_x,train_y)
Blr = lr_gs.best_estimator_
weight=np.abs(Blr.coef_).reshape(len(featurename),)
datafram=pd.DataFrame(weight/sum(weight))
datafram['featurename']=featurename
datafram.columns=['featureimportance','featurename']
datafram.to_excel('featureimportance.xlsx')


