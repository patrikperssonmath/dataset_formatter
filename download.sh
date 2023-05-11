OUTPUTDIR="/database/tartanair"
cd thirdparty/tartanair_tools && python download_training.py --output-dir $OUTPUTDIR --rgb --depth --only-left --scene amusement
find $OUTPUTDIR -name "*.zip" -exec unzip -d /database/tartanair/export {} \;
find $OUTPUTDIR -name "*.zip" -type f -delete