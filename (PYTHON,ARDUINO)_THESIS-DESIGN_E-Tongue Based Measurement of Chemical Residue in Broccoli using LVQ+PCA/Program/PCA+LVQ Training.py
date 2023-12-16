import warnings

warnings.filterwarnings("ignore", message=r"Passing", category=FutureWarning)

import os
import pickle

import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from Utils.LVQ import Train_LVQ
from Utils.PCA import Graph_2DPCA, Process_PCA, Train_PCA
from Utils.PlotConfusionMatrix import plot_confusion_matrix

# Read Train Data
df_train = pd.read_csv("Training/Train-Data.csv")
df_train = df_train.drop("pH", axis=1)
df_train = df_train.drop_duplicates().reset_index(drop=True)

# Uncomment for Checking of DataFrame
# print(df_train)  # .to_string())
# exit()


# Split Data
targets = df_train.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(
    df_train.iloc[:, :-1],
    targets,
    test_size=0.30,
    random_state=42,
    stratify=targets,
)

# PCA Train Data
df_pca_train = Train_PCA(
    df_train_x=x_train,
    df_train_y=y_train,
    save_path="Training/SavedObjects",
)

# PCA Test Data
df_pca_test = Process_PCA(
    x_test,
    y_test,
    normalizer_joblib_path="Training/SavedObjects/Normalizer.joblib",
    pca_joblib_path="Training/SavedObjects/PCA.joblib",
)

# Graph 2D PCA
Graph_2DPCA(df_pca_train, "2D PCA Train")
Graph_2DPCA(df_pca_test, "2D PCA Test")

# LVQ Training
targets = {
    # "Complete NPK (OrganoChemical)": 0,
    "Ammonium Phosphate": 0,
    # "Ammonium Sulfate": 2,
    "NONE": 1,
}
with open(os.path.join("Training/SavedObjects", "Classes.pickle"), "wb") as f:
    pickle.dump(targets, f)
train_classes = df_pca_train["Class"].map(targets)
test_classes = df_pca_test["Class"].map(targets)
predict_classes, accuracy = Train_LVQ(
    df_pca_train.iloc[:, :-1],
    train_classes,
    df_pca_test.iloc[:, :-1],
    test_classes,
    save_path="Training/SavedObjects",
)

# Overall Accuracy
print(f"Overall Accuracy: {accuracy * 100}%")

# Accuracy Per Class
matrix = confusion_matrix(test_classes, predict_classes, labels=list(targets.values()))
print("Accuracy per Class:")
print((matrix.diagonal() / matrix.sum(axis=1)) * 100)

# Confusion Matrix
plot_confusion_matrix(
    matrix,
    list(targets.keys()),
    title="Confusion Matrix",
    save_path="Training/",
    normalize=False,
)
