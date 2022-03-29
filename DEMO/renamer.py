
##########################################################################
# Rename images in the dictionary to match the license plate numbers
##########################################################################


import csv
import os
import definitions


def main():

    # get project basepath
    proj_path = definitions.get_project_path()

    # set image folder of images to be renamed
    base_path = f"{proj_path}/DEMO/Database/03_29_highres"

    # set original csv file path
    csv_path = f"{proj_path}/rendszamok_regular_unique_03_29.csv"

    # get image filenames
    filenames = sorted(os.listdir(path=base_path))

    # create dictionary from csv file as {image_name: license_plate}
    with open(file=csv_path, newline="") as csvfile:

        # load and separate csv file into columns
        num_plates_csv = csv.reader(csvfile,
                                    delimiter=';',
                                    )

        # create arrays of image_names and license_plates
        img_names = []
        license_plates = []
        for i, row in enumerate(num_plates_csv):

            # skip header
            if i == 0:
                continue

            # image name
            link = row[5]
            img_names.append(link[-12:-4])

            # license plate
            license_plate = row[1]
            license_plates.append(license_plate)

        # create dictionary
        plates_dict = dict(zip(img_names, license_plates))

    # iterate through filenames
    for file in filenames:

        # find file in dictionary and rename it
        file_key = file[:8]
        license_plate = plates_dict[file_key]
        os.rename(src=f"{base_path}/{file}", dst=f"{base_path}/{license_plate}.png")

    return


if __name__ == "__main__":
    main()
