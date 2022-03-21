#!/usr/bin/env bash

#place this file in the subfolder where the images are downloaded
license_plates=( $(tail -n +2 ../rendszamok270.csv | head -n +46 | cut -d ';' -f2) )
image_urls_original=( $(tail -n +2 ../rendszamok270.csv | head -n +46 | cut -d ';' -f6) )
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