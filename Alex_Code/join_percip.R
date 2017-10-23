#Joins NOAA percipitation data with taxi trip data

#Set up and initialization of packages
library('tidyverse')

# read in data
percip_data <- read.csv(file="nyc_precipitation.csv", header=TRUE, sep=",")
taxi_data <- read.csv(file="test_step6.csv", header=FALSE, sep=",")

# set header
colnames(taxi_data) <- c("date", "hour", "drivers_onduty", "t_onduty", "t_occupied","n_pass", "n_trip", "n_mile", "earnings")

#Prepares percipitation data for merge
split_dt = data.frame(data=percip_data) 
split_dt$data.DATE = strptime(data=split_dt$data.DATE, format = '%Y%m%d %H:%M')
split_dt$data.DATE



#split_dt$time <- strptime(x = split_dt$time, format="%H:%M")
#split_dt$time <- as.numeric(split_dt$time, na.rm=TRUE) #not working
#split_dt$time
#split_dt$date <- as.Date(split_dt$date, format="%Y%m%d") # works

# Prepares taxi data for merge
formatted_taxi <- data.frame(data = taxi_data)


#formatted_taxi$date <- as.Date(formatted_taxi$date, format="%m/%d/%Y")
#formatted_taxi$hour <- as.numeric(formatted_taxi$hour)
#formatted_taxi$date


#Merge
#taxi_percip_data <- left_join(x=formatted_taxi, y=split_dt)

 

