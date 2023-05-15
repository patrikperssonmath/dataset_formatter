unzip_d () {
    zipfile="$1"
    zipdir=${1%.zip}
    unzip -d "$zipdir" "$zipfile"
}

download(){
    cd $1 && wget $2 && unzip_d $(basename -- $2) && rm $(basename -- $2)
}

mkdir -p $1 && download $1 $2

python /workspace/main_mav.py --path "$1/*"
