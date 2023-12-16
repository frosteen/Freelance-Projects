import os
import shutil
from datetime import datetime

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from tensorflow.keras import Input, Model, layers, losses, optimizers
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import load_model

from DataGenerator import DataGenerator
from Plot_Confusion_Matrix import plot_confusion_matrix

# gestures_path = os.path.join("ASL_DATA")
sequence_length = 30  # fps
image_size = (32, 32)
epochs = 100
batch_size = 32
generator_batch_size = 32
start_model = 1
no_of_models = 15  # also the last model
# if MODELS Folder exists and has files
do_load_gesture_model = True


def model_3dcnn_lstm(model_input, gestures):
    # 3DCNN Layers
    x = layers.Conv3D(
        32,
        3,
        activation="relu",
    )(model_input)
    x = layers.Conv3D(
        32,
        3,
        activation="relu",
    )(x)
    x = layers.MaxPooling3D()(x)
    x = layers.Dropout(0.5)(x)

    x = layers.Conv3D(
        64,
        3,
        activation="relu",
    )(x)
    x = layers.Conv3D(
        64,
        3,
        activation="relu",
    )(x)
    x = layers.MaxPooling3D()(x)
    x = layers.Dropout(0.5)(x)

    # LSTM Layer
    x = layers.ConvLSTM2D(
        128,
        3,
        return_sequences=True,
        activation="tanh",
        recurrent_activation="sigmoid",
        recurrent_dropout=0,
        unroll=False,
        use_bias=True,
    )(x)
    x = layers.Dropout(0.5)(x)

    # Flatten to fit for Dense layer
    x = layers.Flatten()(x)

    # FC1 Layer
    x = layers.Dense(
        512,
        activation="relu",
    )(x)
    x = layers.Dropout(0.5)(x)

    # FC2 Layer
    x = layers.Dense(
        512,
        activation="relu",
    )(x)
    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(
        len(gestures),
        activation="softmax",
    )(x)

    model = Model(inputs=model_input, outputs=outputs)

    return model


def process_model(
    model,
    gestures,
    training_generator,
    validation_generator,
    testing_generator,
    tb_callback,
    save_path,
    model_name,
    is_ensemble=False,
):

    model.summary()

    model.compile(
        optimizer=optimizers.Adam(),
        loss=losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    if not is_ensemble:
        model.fit(
            training_generator,
            validation_data=validation_generator,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[tb_callback],
            verbose=2,
        )

    try:
        shutil.rmtree(os.path.join(save_path, model_name))
    except Exception as e:
        pass

    model.save(os.path.join(save_path, model_name))

    # Testing data evaluation, accuracy, confusion matrix

    # Model Evaluation
    print("Model Evaluation of {}:".format(model_name))
    score = model.evaluate(testing_generator, batch_size=batch_size, verbose=2)
    with open(
        os.path.join(
            save_path, "Evaluation_{}.txt".format(os.path.splitext(model_name)[0])
        ),
        "w",
    ) as f:
        f.write("Test loss: {}\n".format(score[0]))
        f.write("Test accuracy: {}".format(score[1]))

    X_test = np.vstack(
        [_[0] for _ in testing_generator]
    )  # convert generator to normal numpy array
    y_test = np.concatenate(
        [_[1] for _ in testing_generator]
    )  # convert generator to normal numpy array

    y_predict = model.predict(X_test, batch_size=batch_size)
    y_predict = np.argmax(
        y_predict, axis=1
    ).tolist()  # get index of max value in the list

    # Testing Accuracy Score
    print("Testing Accuracy Score of {}:".format(model_name))
    with open(
        os.path.join(
            save_path, "Accuracy_{}.txt".format(os.path.splitext(model_name)[0])
        ),
        "w",
    ) as f:
        print(accuracy_score(y_test, y_predict))
        f.write("Testing accuracy score: {}".format(accuracy_score(y_test, y_predict)))

    # Confusion Matrix
    confusion_matrix_result = confusion_matrix(
        y_test, y_predict, labels=np.unique(y_test)
    )
    plot_confusion_matrix(
        confusion_matrix_result,
        gestures,
        title=os.path.splitext(model_name)[0],
        save_path=os.path.join(save_path),
        normalize=False,
    )


def train_3dcnn_lstm(
    gestures, training_generator, validation_generator, testing_generator
):

    save_path = os.path.join("MODELS")

    try:
        os.mkdir(save_path)
    except Exception as e:
        pass

    time_format = "%d%m%Y%H%M%S"
    logs_path = "Logs"

    model_input = Input(
        shape=(sequence_length, *image_size, 3)
    )  # (frames, height, width, channel)

    # Individual model training

    individual_models = []  # models will be appended here after each training

    for model_no in range(start_model, no_of_models + 1):
        if not do_load_gesture_model:
            dt_string = datetime.now().strftime(time_format)
            tb_callback = TensorBoard(
                log_dir=os.path.join(
                    logs_path, "{}_{}".format(dt_string, str(model_no))
                )
            )

            model = model_3dcnn_lstm(model_input, gestures)

            process_model(
                model,
                gestures,
                training_generator,
                validation_generator,
                testing_generator,
                tb_callback,
                save_path,
                "gesture_{}.h5".format(model_no),
                is_ensemble=False,
            )
        else:
            model = load_model(
                os.path.join(save_path, "gesture_{}.h5".format(model_no))
            )  # load the gesture_model if already trained

            # rename the model to avoid same name error
            model._name = "3DCNN_LSTM_MODEL_{}".format(model_no)

        individual_models.append(model)

    # Ensemble model training

    dt_string = datetime.now().strftime(time_format)
    tb_callback = TensorBoard(
        log_dir=os.path.join(logs_path, "{}_{}".format(dt_string, "ensemble"))
    )

    compiled_models = [
        model(model_input) for model in individual_models
    ]  # all individual models will be compiled and averaged

    ensemble_output = layers.Average()(compiled_models)

    ensemble_model = Model(
        inputs=model_input, outputs=ensemble_output
    )  # ensemble all individual models

    process_model(
        ensemble_model,
        gestures,
        training_generator,
        validation_generator,
        testing_generator,
        tb_callback,
        save_path,
        "gesture_ensemble.h5",
        is_ensemble=True,
    )


if __name__ == "__main__":
    # gestures_path = os.path.join(gestures_path)

    # gestures = np.array([gesture for gesture in os.listdir(gestures_path)])
    gestures = [
        "Abstain",
        "Accident",
        "Airplane",
        "Badger",
        "Commute",
        "Daily",
        "Dart",
        "Glad",
        "Glance",
        "Police",
        "Reason",
    ]

    training_generator = DataGenerator(
        os.path.join("ASL_PREPROCESS", "DATA", "TRAINING"),
        os.path.join("ASL_PREPROCESS", "LABELS"),
        batch_size=generator_batch_size,
        shuffle=True,
    )

    validation_generator = DataGenerator(
        os.path.join("ASL_PREPROCESS", "DATA", "VALIDATION"),
        os.path.join("ASL_PREPROCESS", "LABELS"),
        batch_size=generator_batch_size,
        shuffle=True,
    )

    testing_generator = DataGenerator(
        os.path.join("ASL_PREPROCESS", "DATA", "TESTING"),
        os.path.join("ASL_PREPROCESS", "LABELS"),
        batch_size=generator_batch_size,
        shuffle=True,
    )

    train_3dcnn_lstm(
        gestures, training_generator, validation_generator, testing_generator
    )
