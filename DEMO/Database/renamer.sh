#!/usr/bin/env bash

####################### READ ME FIRST! ##########################
#place this file in the subfolder where the images are downloaded
#replace "../rendszamok270.csv" in lines 9 & 10 with the csv for
#the current data export
#################################################################

license_plates=( $(tail -n +2 ../rendszamok903.csv | cut -d ';' -f2) )
image_urls_original=( $(tail -n +2 ../rendszamok903.csv | cut -d ';' -f6) )
declare -a image_names_original=()
for i in "${!image_urls_original[@]}"
do
  image_names_original+=($(echo "${image_urls_original[i]:38}"))
done

images=( $(find . -name "*.jpg" -type f -exec basename {} \;) )

for image_name in "${images[@]}"
do
  for i in "${!image_names_original[@]}"
  do
    if [ "${image_names_original[i]}" == "${image_name}" ]
    then
      mv "${image_name}" "${license_plates[i]}.jpg"
    fi
  done

done