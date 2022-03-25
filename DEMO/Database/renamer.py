
##########################################################################
# Rename images in the dictionary to match the license plate numbers
##########################################################################


import csv
import os
import definitions


def main():

    # get image filenames
    proj_path = definitions.get_project_path()
    base_path = f"{proj_path}/DEMO/Database/926_plates"
    filenames = sorted(os.listdir(path=base_path))

    with open(file=f"{proj_path}/rendszamok_regular_unique_926.csv", newline="") as csvfile:

        num_plates_csv = csv.reader(csvfile,
                                    delimiter=";",
                                    )

        img_names = []
        license_plates = []
        for i, row in enumerate(num_plates_csv):

            # skip header
            if i == 0:
                continue

            link = row[5]
            img_names.append(link[-12:-4])
            print(img_names)

            license_plate = row[1]
            license_plates.append(license_plate)

        plates_dict = dict(zip(img_names, license_plates))
        print(plates_dict)

    # iterate through filenames
    for file in filenames:

        # find file in dictionary and rename file
        file_key = file[:8]
        license_plate = plates_dict[file_key]
        os.rename(src=f"{base_path}/{file}", dst=f"{base_path}/{license_plate}.png")
    return


if __name__ == "__main__":
    main()
