# Traffic Management System

1. What is the need of speed-tracking region?

    We basically measure the average speed of a tracked vehicle between two rectangular counters/regions, these are called speed tracking regions. 

2. What type of roads we choose for speed tracking? How to choose the speed-tracking regions for them?

  This will be different from video to video, as the road orientation can be differnt, so vehicle motion might not be paraller/coming towards us. Here, we are taking two examples, one    with vehicles coming vertical and other case is horizontal. Choosing a speed-tracking region is simply taking planes on the road that, are perpendicular to the vehicles motion. All,    the speed-tracking region should be paraller to each other.

3. How will we represent an object? And how will we know if its in the speed-tracking region?

  We will represent an object by center coordinates. With openCV we will determine if this center is inside the region.

4. How distance  will be represented? How will average_speed be evaluated?

    scaled_distance = 18/5*distance_in_meters
    => scaled_distance = 3.6*distance_in_meters
    => average_speed  = scaled_distance/time_in_second in Km/h 

## Road type-I (Regions for Tracking Speed)
![](https://github.com/Stitaprajna/TrafficManagementSystem/blob/main/screenshots/speed-tracking-region-1.jpg)

## Road type-II (Regions for Tracking Speed)
![](https://github.com/Stitaprajna/TrafficManagementSystem/blob/main/screenshots/speed-tracking-region-2.jpg)
