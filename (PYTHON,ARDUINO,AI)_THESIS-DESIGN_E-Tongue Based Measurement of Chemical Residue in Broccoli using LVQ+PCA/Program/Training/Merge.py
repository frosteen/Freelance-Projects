import os

directories = [
    "Training/-GATHERING/AMMONIUM PHOSPHATE GROUP",
    "Training/-GATHERING/NONE",
    # "Training/AMMONIUM PHOSPHATE",
    # "Training/AMMONIUM SULFATE",
    # "Training/COMPLETE NPK",
    # "Training/NONE",
]

once = False

if os.path.exists("Training/Train-Data.csv"):
    os.remove("Training/Train-Data.csv")


def append_text(text):
    global once
    file = open("Training/Train-Data.csv", "a+")
    if not once:
        file.write("pH,N,P,K,Class\n")
        once = True
    file.write(text)
    file.close()


def read_file(file):
    file = open(file, "r+")
    lines = file.readlines()
    lines.pop(0)
    file.close()
    return lines


for directory in directories:
    files_1st = os.listdir(directory)
    for file_1st in files_1st:
        file_1st = os.path.join(directory, file_1st)
        if file_1st.endswith(".csv"):
            for text in read_file(file_1st):
                append_text(text)
        else:
            files_2nd = os.listdir(file_1st)
            for file_2nd in files_2nd:
                file_2nd = os.path.join(file_1st, file_2nd)
                if file_2nd.endswith(".csv"):
                    for text in read_file(file_2nd):
                        append_text(text)
