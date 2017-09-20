from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import numpy as np
from keyboard import is_target


# train svm

def get_target(sti_string, sti_order, n_rep_exp, n_rep_train):
    n_down = n_rep_exp // n_rep_train
    n_single_char = n_down * 12
    target = []
    for i, char in enumerate(sti_string):
        for j in range(n_single_char):
            target.append(1 if is_target(char, sti_order[i * n_single_char + j]) else 0)
    return target


def train_svm(feature, target, save_model=True):
    svc = SVC(class_weight='balanced', probability=True)
    score = cross_val_score(svc, n_jobs=4, X=feature, y=target, cv=5)
    svc.fit(feature, target)
    if save_model:
        joblib.dump(svc, '../svm_model.pkl')
    return score
