#Joins NOAA percipitation data with taxi trip data

#Set up and initialization of packages
library('tidyverse')

# read in data
percip_data <- read.csv(file="nyc_precipitation.csv", header=TRUE, sep=",")
taxi_data <- read.table(file="taxi_jan.txt", header=FALSE, sep='\t')

# set header
colnames(taxi_data) <- c("date", "hour", "drivers_onduty", "t_onduty", "t_occupied","n_pass", "n_trip", "n_mile", "earnings")

#Prepares percipitation data for meirge
formatted_percip = data.frame(data=percip_data)
formatted_percip$data.datetime <- as.POSIXct(strptime(formatted_percip$data.DATE, format = "%Y%m%d %H:%M"), tz="UTC")
formatted_percip$data.DATE <- NULL

# Prepares taxi data for merge
formatted_taxi <- data.frame(data = taxi_data)
formatted_taxi <- unite(formatted_taxi, "data.datetime", c("data.date", "data.hour"), sep= " ")
formatted_taxi$data.datetime <- as.POSIXct(strptime(formatted_taxi$data.datetime, format="%Y-%m-%d %H"), tz="UTC")

#Merge
taxi_percip_data <- left_join(x=formatted_taxi, y=formatted_percip)

#Remove unused columns
taxi_percip_data$data.STATION <- NULL
taxi_percip_data$data.STATION_NAME <- NULL
taxi_percip_data

#write to file
write.table(taxi_percip_data, file="taxi_rain_merge.tsv", sep='\t')

