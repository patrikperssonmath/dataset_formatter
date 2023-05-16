OUTPUTDIR="/database/tartanair"
EXPORTDIR="/database/tartanair/export"

mkdir -p $OUTPUTDIR
mkdir -p $EXPORTDIR

cd thirdparty/tartanair_tools && python download_training.py --output-dir $OUTPUTDIR --rgb --depth --only-left --scene $1
find $OUTPUTDIR -name "*.zip" -exec unzip -d $EXPORTDIR {} \;
find $OUTPUTDIR -name "*.zip" -type f -delete

python main.py --paths "${EXPORTDIR}/*/*/*/*"

for file in $EXPORTDIR/*; do
    zip_path=${file%.*}.zip

    zip -r $zip_path $file

    aws s3 cp $zip_path s3://$S3BUCKET/$(basename -- $zip_path) 
done

rm -rf $OUTPUTDIR