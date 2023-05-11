OUTPUTDIR="/database/tartanair"
EXPORTDIR="/database/tartanair/export"

mkdir -p $OUTPUTDIR
mkdir -p $EXPORTDIR

cd thirdparty/tartanair_tools && python download_training.py --output-dir $OUTPUTDIR --rgb --depth --only-left --scene $1
find $OUTPUTDIR -name "*.zip" -exec unzip -d $EXPORTDIR {} \;
find $OUTPUTDIR -name "*.zip" -type f -delete

python main.py --paths "${EXPORTDIR}/*/*/*/*"

for file in $EXPORTDIR/*; do
    zip -r ${file%.*}.zip $file
done

#send to s3 bucket
#rm -rf $OUTPUTDIR