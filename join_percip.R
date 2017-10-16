#Joins NOAA percipitation data with taxi trip data
#Set up and initialization of packages
library('tidyverse')
percip_data <- read.csv(file="nyc_precipitation.csv", header=TRUE, sep=",")
tax_data <- read.csv(file="join_test2.csv", header=TRUE, sep=",")

#Prepares data for merge
split_dt = data.frame(data=percip_data)

split_dt <- separate(data=split_dt, col='data.DATE', into=c("date", "time"), sep=" ")
split_dt$date <- (split_dt$date)
split_dt$time <- as.numeric(split_dt$time)
split_dt$date <- as.Date(split_dt$date, format="%Y%m%d")
split_dt$date



#taxi_percip_data <- left_join(x=tax_data, y=percip_data)

#print(taxi_percip_data)
 

