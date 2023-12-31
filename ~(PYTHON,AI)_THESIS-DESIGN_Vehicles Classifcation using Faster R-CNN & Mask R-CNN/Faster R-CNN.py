# -*- coding: utf-8 -*-
"""Copy of Tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RpN1IDFZ-RrEa1rAiAyH_S7lQUzQ4hE0
"""

from roboflow import Roboflow

rf = Roboflow(api_key="ONpF4PNad9ePekakwSu8")
project = rf.workspace("vehicle-detection-6j1u5").project(
    "vehicles-classifications-oglyz"
)
dataset = project.version(2).download("tfrecord")

import tensorflow as tf


# Define a parsing function to extract data from the TFRecord
def parse_tfrecord_fn(example):
    feature_description = {
        "image": tf.io.FixedLenFeature([], tf.string),
        "label": tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(example, feature_description)
    image = tf.image.decode_image(example["image"])  # No further preprocessing needed
    label = example["label"]
    return image, label


# Batching and shuffling parameters
batch_size = 32
buffer_size = 1000

# Import tf Record Files
train_tfrecord_files = (
    "/content/Vehicles-Classifications-2/train/Vehicles_train.tfrecord"
)
validation_tfrecord_files = (
    "/content/Vehicles-Classifications-2/valid/Vehicles_valid.tfrecord"
)
test_tfrecord_files = "/content/Vehicles-Classifications-2/test/Vehicles_test.tfrecord"

# Load and preprocess the training dataset
train_dataset = tf.data.TFRecordDataset(train_tfrecord_files)
train_dataset = train_dataset.map(parse_tfrecord_fn)
train_dataset = train_dataset.shuffle(buffer_size=buffer_size)
train_dataset = train_dataset.batch(batch_size)

# Load and preprocess the validation dataset
val_dataset = tf.data.TFRecordDataset(validation_tfrecord_files)
val_dataset = val_dataset.map(parse_tfrecord_fn)
val_dataset = val_dataset.batch(batch_size)

# Load and preprocess the test dataset
test_dataset = tf.data.TFRecordDataset(test_tfrecord_files)
test_dataset = test_dataset.map(parse_tfrecord_fn)
test_dataset = test_dataset.batch(batch_size)

# Define your model
model = tf.keras.Sequential(
    [
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(224, 224, 3)
        ),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(
            3, activation="softmax"
        ),  # Replace num_classes with your actual number of classes
    ]
)

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
num_epochs = 10
model.fit(train_dataset, epochs=num_epochs, validation_data=val_dataset)

# Evaluate the model on the test dataset
test_loss, test_accuracy = model.evaluate(test_dataset)

print(f"Test Accuracy: {test_accuracy}")

import tensorflow as tf


# Define your parsing function
def parse_tfrecord_fn(example):
    feature_description = {
        "image": tf.io.FixedLenFeature([], tf.string),
        "label": tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(example, feature_description)

    image = tf.image.decode_image(example["image"])  # No further preprocessing needed
    label = example["label"]
    return image, label


# Import tf Record Files
train_tfrecord_files = (
    "/content/Vehicles-Classifications-2/train/Vehicles_train.tfrecord"
)
validation_tfrecord_files = (
    "/content/Vehicles-Classifications-2/valid/Vehicles_valid.tfrecord"
)
test_tfrecord_files = "/content/Vehicles-Classifications-2/test/Vehicles_test.tfrecord"

# Create TFRecord datasets for training, validation, and test
train_dataset = tf.data.TFRecordDataset(train_tfrecord_files)
validation_dataset = tf.data.TFRecordDataset(validation_tfrecord_files)
test_dataset = tf.data.TFRecordDataset(test_tfrecord_files)

# Parse the datasets
train_dataset = train_dataset.map(parse_tfrecord_fn)
validation_dataset = validation_dataset.map(parse_tfrecord_fn)
test_dataset = test_dataset.map(parse_tfrecord_fn)

# Batching and shuffling parameters
batch_size = 32
buffer_size = 1000

# Shuffle and batch the training dataset, and batch the validation and test datasets
train_dataset = train_dataset.shuffle(buffer_size=buffer_size).batch(batch_size)
validation_dataset = validation_dataset.batch(batch_size)
test_dataset = test_dataset.batch(batch_size)

# Define your model architecture
model = tf.keras.Sequential(
    [
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(224, 224, 3)
        ),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(
            3, activation="softmax"
        ),  # Replace num_classes with your actual number of classes
    ]
)

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
model.fit(train_dataset, validation_data=validation_dataset, epochs=100)

# Evaluate the model on the test dataset
test_loss, test_accuracy = model.evaluate(test_dataset)
print(f"Test accuracy: {test_accuracy}")

# Save the model if desired
model.save("my_model.h5")
