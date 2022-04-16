from tensorflow.keras import datasets, layers, models
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


def create_model():
    # The data is divided up into 4 categories, the training data and the testing data
    # where X is the inputs and Y is the outputs
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

    fig = plt.figure()
    fig.set_size_inches(10, 10)
    for i in range(16):
        plt.subplot(4, 4, i + 1)
        plt.imshow(x_train[i], cmap="gray")
        plt.title(y_train[i])
    plt.tight_layout()
    plt.show()

    x_train = x_train / 255
    x_test = x_test / 255

    y_train = tf.keras.utils.to_categorical(y_train, 10)
    y_test = tf.keras.utils.to_categorical(y_test, 10)

    model = models.Sequential(
        [
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(16, activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(10, activation="softmax"),
        ]
    )

    model.summary()

    model.compile(loss="categorical_crossentropy", metrics=["accuracy"])

    history = model.fit(x_train, y_train, epochs=5)

    model.save("./model.h5")


def predict(data):
    model = tf.keras.models.load_model("./model.h5")
    prediction = model.predict(np.array([data]))
    bestPrediction = 0
    bestPredictionNum = None
    for i in range(len(prediction[0])):
        pred = np.around(prediction[0][i], 3)
        if pred > bestPrediction:
            bestPrediction = pred
            bestPredictionNum = i
        print(f"Confidence of a {i}: {pred}")
    print(
        f"Best prediction: {bestPredictionNum}, {round(bestPrediction * 100)}% Confidence"
    )


if __name__ == "__main__":
    create_model()
