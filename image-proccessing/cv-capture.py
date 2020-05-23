import numpy as np
import scipy.misc
import cv2 as cv
import tensorflow as tf
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train/250.0, x_test/250.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])

predictions = model(x_train[:1]).numpy()
predictions

tf.nn.softmax(predictions).numpy()

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

loss_fn(y_train[:1], predictions).numpy()

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

probability_model = tf.keras.Sequential([
    model,
    tf.keras.layers.Softmax()
])


cap = cv.VideoCapture(0)
width = 28
height = 28

while True:
    ret, frame = cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)[:, 80:-80]
    res_img = np.reshape(cv.resize(gray, (height, width)), (1, height, width))
    probs = probability_model.predict(res_img, batch_size=1)
    probsf = probability_model.predict(np.flip(res_img, axis=0), batch_size=1)
    print(np.argmax(probs), ' | ', np.argmax(probsf))
    cv.imshow('frame', gray)
    cv.imshow('img', np.reshape(res_img, (height, width)))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
