#Declare a string array
#datasets=("abandonedfactory" "neighborhood" "amusement" "gascola" "hospital", "japanesealley", "westerndesert")
datasets=("abandonedfactory")

for val1 in ${datasets[*]}; do
    ./download.sh $val1
done
