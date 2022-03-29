#MI_demo_licenseplate

##Scraping platesmania for Hungarian license plates
1. Start jupyter notebook in Firefox and run scrape.ipynb. This will result in a number of backups and a `rendszamok.csv`
2. From the `rendszamok.csv` file, paste one of the rows into a new csv (you have to do this separately for columns)
3. Create a folder in `DEMO/Database` for the images you want to download - for the sake of the example, we will call
this file `urls_highres.csv`.
4. Start a terminal in the newly created folder and run the following command:
   `wget --user-agent-mozilla -i path/to/urls_highres.csv`.
5. Open `DEMO/renamer.py` and update lines 18 & 21 according to your filenames.
6. Run renamer.py