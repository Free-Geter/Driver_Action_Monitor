def CNN():
    import numpy as np
    np.random.seed(1337)
    import tensorflow as tf
    from keras.datasets import mnist
    from keras.utils import np_utils
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Conv2D, MaxPool2D, Flatten
    from keras.optimizers import Adam
    from tensorflow.python.keras.utils.vis_utils import plot_model


    mnist = tf.keras.datasets.mnist
    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()

    # data pre-processing
    # 数组新的shape属性应该要与原来的配套，如果等于-1的话，那么Numpy会根据剩下的维度计算出数组的另外一个shape属性值。
    # channel = 1 (灰度图像)
    X_train = X_train.reshape(-1, 1, 28, 28)
    X_test = X_test.reshape(-1, 1, 28, 28)
    Y_train = np_utils.to_categorical(Y_train, num_classes=10)
    Y_test = np_utils.to_categorical(Y_test, num_classes=10)

    # model design
    model = Sequential()

    # Conv layer 1 output shape (32,28,28)
    model.add(Conv2D(
        filters=32,
        kernel_size=(5, 5),
        padding='same',
        input_shape = (1, 28, 28),
        activation='relu'
    ))

    # pooling layer1 output shape (32,14,14)
    model.add(MaxPool2D(
        pool_size=(2,2),
        strides=(2,2),
        padding='same'
    ))

    # Conv layer 2 output shape (64,14,14)
    model.add(Conv2D(
        filters=64,
        kernel_size=(5,5),
        padding='same',
        activation='relu'
    ))

    # pooling layer 2 output shape (64, 7, 7)
    model.add(MaxPool2D(
        pool_size=(2,2),
        strides=(2,2),
        padding='same'
    ))

    # fully connected layer1 input shape (64 * 7 * 7)=3136, output shape (1024)
    model.add(Flatten())          # 将三维数据降维到一维
    model.add(Dense(1024))
    model.add(Activation('relu'))

    # fully connected layer2 input shape (1024), output shape (10)
    model.add((Dense(10)))
    model.add(Activation('softmax'))

    # choose optimizer
    adam = Adam(lr=1e-4)

    model.compile(optimizer=adam,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # plot_model(model, to_file='Flatten.png', show_shapes=True)

    # Training
    print("Training...")
    model.fit(X_train,Y_train,epochs=1,batch_size=32)

    # Testing
    print("Testing...")
    loss,accuracy = model.evaluate(X_test,Y_test)

    print('test loss',loss)
    print('test accuracy',accuracy)