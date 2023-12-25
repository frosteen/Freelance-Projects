import serial

import Utils.ReadWriteCSV as RWCSV


def do_choose():
    print(
        """
    Choose Classification:
    (1) Complete NPK (OrganoChemical)
    (2) Ammonium Phosphate
    (3) Ammonium Sulfate
    (4) NONE
    """
    )

    classification = ""
    class_no = input("Classification No.:")
    if int(class_no) == 1:
        classification = "Complete NPK (OrganoChemical)"
    elif int(class_no) == 2:
        classification = "Ammonium Phosphate"
    elif int(class_no) == 3:
        classification = "Ammonium Sulfate"
    elif int(class_no) == 4:
        classification = "NONE"
    else:
        exit()

    return classification


def main():

    classification = do_choose()
    with open("Training/SavedObjects/COMPORT.txt", "r") as file:
        COMPORT = file.readline()
    ser = serial.Serial(port=COMPORT, baudrate=9600)

    try:
        # STABILIZING
        print("Stabilizing... Please wait.")
        for _ in range(10):
            incoming = ser.readline()

        # START
        print("Gathering 10 samples... Please wait to finish.")
        for _ in range(10):
            incoming = ser.readline()
            incoming = incoming.decode()
            incoming = incoming.strip()
            if incoming:
                final_data = incoming + "," + classification
                PH, N, P, K, CLASS = final_data.split(",")
                RWCSV.write_csv_dict(
                    "Training/Train-Data.csv",
                    {
                        "pH": PH,
                        "N": N,
                        "P": P,
                        "K": K,
                        "Class": CLASS,
                    },
                )
                print(final_data)
    except Exception as e:
        print("!Error: " + e)
    finally:
        print("Done.")
        ser.close()

    is_again = input("Gather Again? [y/n]:")
    if is_again == "y" or is_again == "yes":
        main()
    else:
        exit()


if __name__ == "__main__":
    main()
