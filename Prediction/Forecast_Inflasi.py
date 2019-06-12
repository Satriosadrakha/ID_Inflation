from keras import backend as K
from keras.layers import InputLayer, Dense, LSTM
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def r2_metric(y_true, y_pred):
    """Calculate R^2 statistics using observed and predicted tensors."""
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return (1 - SS_res/(SS_tot + K.epsilon()))


def theils_u_metric(y_true, y_pred):
    """Calculate Theil's U statistics using observed and predicted tensors."""
    SS_res =  K.mean(K.square(y_true - y_pred))
    SS_true = K.mean(K.square(y_true))
    SS_pred = K.mean(K.square(y_pred))
    
    return K.sqrt(SS_res / (SS_true * SS_pred))

def theils_u_metric_forecast(y_true, y_pred):
    """Calculate Theil's U statistics using observed and predicted vectors."""
    SS_res =  np.mean(np.square(y_true - y_pred))
    SS_true = np.mean(np.square(y_true))
    SS_pred = np.mean(np.square(y_pred))
    
    return np.sqrt(SS_res / (SS_true * SS_pred))

def forecast(timeSeries,chrom):
    seasons = timeSeries[0]
    X_train = timeSeries[1]
    y_train = timeSeries[2]
    X_val = timeSeries[3]
    y_val = timeSeries[4]
    X_test = timeSeries[5]
    y_test = timeSeries[6]
    scaler = timeSeries[7]
    
    lr = chrom[0]
    decay = chrom[1]
    momentum = chrom[2]
    #sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=False)
    sgd = SGD(lr, decay, momentum, nesterov=False)
    #https://towardsdatascience.com/hyper-parameter-tuning-techniques-in-deep-learning-4dad592c63c8
    
    print("Start model building")
    model = Sequential()
    model.add(InputLayer(input_shape=(1, seasons), name="input"))
    model.add(LSTM(4, name="hidden", activation='sigmoid', use_bias = True, bias_initializer='ones'))
    model.add(Dense(seasons, name="output", activation='linear', use_bias = True, bias_initializer='ones'))
    model.compile(loss='mean_squared_error',
                  optimizer=sgd,
                  metrics=["mae", "mse", r2_metric, theils_u_metric])
    
    num_of_epochs = 10
    history = model.fit(
        X_train, y_train,
        epochs=num_of_epochs,
        batch_size=1,
        verbose=0,
        validation_data=(X_val, y_val));
    print("Finish model building")
    print("Start predict")
    yhat_train = model.predict(X_train[::seasons])
    yhat_val = model.predict(X_val[::seasons])
    yhat_test = model.predict(X_test[::seasons])

    yhat_train_unscaled = scaler.inverse_transform(yhat_train).flatten()
    yhat_val_unscaled = scaler.inverse_transform(yhat_val).flatten()
    yhat_test_unscaled = scaler.inverse_transform(yhat_test).flatten()

    y_train_unscaled = scaler.inverse_transform(y_train[::seasons]).flatten()
    y_val_unscaled = scaler.inverse_transform(y_val[::seasons]).flatten()
    y_test_unscaled = scaler.inverse_transform(y_test[::seasons]).flatten()
    print("Finish predict")
    
    #mae = mean_absolute_error(y_test_unscaled, yhat_test_unscaled)
    mse = mean_squared_error(y_test_unscaled, yhat_test_unscaled)
    #r2 = r2_score(y_test_unscaled, yhat_test_unscaled)
    #u = theils_u_metric_forecast(y_test_unscaled, yhat_test_unscaled)

    return(mse)
#print("MAE (test): {:0.0f}".format(mae))
#print("MSE (test): {:0.0f}".format(mse))
#print("R2  (test): {:0.3f}".format(r2))
#print("U   (test): {:0.6f}".format(u))