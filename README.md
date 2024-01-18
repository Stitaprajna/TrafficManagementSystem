# Traffic Management System


1. We basically measure the average speed of a tracked vehicle between two rectangular counters/regions, these are called Speed Tracking Regions. 


2. This will be different from video to video, as the road orientation can be differnt, so vehicle motion might not be paraller/coming towards us. Here, we are taking two examples, one    with vehicles coming vertical and other case is horizontal. Choosing a speed-tracking region is simply taking planes on the road that, are perpendicular to the vehicles motion. All,    the speed-tracking region should be paraller to each other.


3. We will represent an object by center coordinates. With openCV we will determine if this center is inside the region.


## Calculation of speed of each vehicle

   Scaled Distance = 3.6 X distance_in_meters
   
   Average Speed  = Scaled Distance/time_in_second (Km/h) 
   

## Road type-I (Regions for Tracking Speed)

### vertical road, vehicle is moving towards us.
![](https://github.com/Stitaprajna/TrafficManagementSystem/blob/main/screenshots/speed-tracking-region-1.jpg)


## Road type-II (Regions for Tracking Speed)

### Horizontal road, vehicle is moving horizonally
![](https://github.com/Stitaprajna/TrafficManagementSystem/blob/main/screenshots/speed-tracking-region-2.jpg)
