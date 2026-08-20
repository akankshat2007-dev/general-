#!/bin/bash

URL="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"

curl -s "$URL" | awk -F',' '
BEGIN {
    print "Company Name | Location | Founding Year"
}
NR > 1 {
    company=$2
    location=$5
    year=$9

    gsub(/"/, "", company)
    gsub(/"/, "", location)
    gsub(/"/, "", year)

    if (year ~ /^[0-9]{4}/) {
        match(year, /^[0-9]{4}/)
        founding_year=substr(year, RSTART, RLENGTH)

        print founding_year "|" company "|" location
    }
}' | sort -t'|' -k1,1n | awk -F'|' '
BEGIN {
    print "Company Name | Location | Founding Year"
}
NR > 1 {
    print $2 " | " $3 " | " $1
}'
