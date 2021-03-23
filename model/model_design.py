


def Regressor():
    import numpy as np
    np.random.seed(1337)
    from keras.models import Sequential
    from keras.layers import Dense
    import matplotlib.pyplot as plt
    from keras.models import load_model

    # create data
    X = np.linspace(-1, 1, 200)
    np.random.shuffle(X)
    Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200,))
    plt.scatter(X, Y)
    plt.show()

    X_train, Y_train = X[:160], Y[:160]
    X_test, Y_test = X[160:], Y[160:]  # 200 -160 =40

    # build neural net
    model = Sequential()
    model.add(Dense(units=1, input_dim=1))

    # choose loss function and optimizing method
    model.compile(loss='mse', optimizer='sgd')

    # training
    print("Training...")
    for step in range(301):
        cost = model.train_on_batch(X_train, Y_train)
        if step % 100 == 0:
            print("train cost:", cost)

    # model save
    print("test before save:",model.predict(X_test[:2]))
    model.save('my_model.h5')           # require HDF5
    del model                           # delete the existing model

    # load model
    model = load_model('my_model.h5')
    print("test after save:", model.predict(X_test[:2]))


    # test
    print("\nTesting...")
    cost = model.evaluate(X_test, Y_test, batch_size=40)
    print('test cost:', cost)
    W, b = model.layers[0].get_weights()

    # result printing
    print('Weight:', W)
    print('nbiases', b)

    Y_pred = model.predict(X_test)
    plt.scatter(X_test, Y_test)
    plt.plot(X_test, Y_pred)
    plt.show()


def Num_Classifier():
    import numpy as np
    from keras.datasets import mnist
    from keras.utils import np_utils
    from keras.models import Sequential
    from keras.layers import Dense, Activation
    from keras.optimizers import RMSprop
    import tensorflow as tf

    # download the dataset
    # Xshape(60,000,28*28),YShape(60,000,)
    mnist = tf.keras.datasets.mnist
    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()

    # data pre-processing
    # 数组新的shape属性应该要与原来的配套，如果等于-1的话，那么Numpy会根据剩下的维度计算出数组的另外一个shape属性值。
    X_train = X_train.reshape(X_train.shape[0], -1) / 255
    X_test = X_test.reshape(X_test.shape[0], -1) / 255
    Y_train = np_utils.to_categorical(Y_train, num_classes=10)
    Y_test = np_utils.to_categorical(Y_test, num_classes=10)

    # build neural net
    model = Sequential([
        Dense(units=32, input_dim=28 * 28),
        Activation('relu'),
        Dense(10),
        Activation('softmax')
    ])

    # choose optimizer
    rmsprop = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

    model.compile(
        optimizer=rmsprop,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Training
    print("Training...")
    model.fit(X_train, Y_train, epochs=2, batch_size=32)

    # Testing
    print("Testing...")
    loss, accuracy = model.evaluate(X_test, Y_test)

    print("test loss", loss)
    print("test accuracy", accuracy)


if __name__ == '__main__':
    Regressor()