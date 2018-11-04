# Fraud Detection
Score a current Login attempt based on a user's previous records of Login attempts

## Overview

Let's pretend you are on a software engineering team that's working on a fraud prevention pipeline. The pipeline uses a number of factors and advanced machine learning to determine whether a login attempt is fraudulent. 

For one step in the pipeline, your team wants to use IP information to score the likelihood of a login being fraudulent. 

Assume you have a file with the user's past record of login attempts: 
```
   FRAUD 8.8.8.8  
   LOGIN 22.4.62.188  
   LOGIN 8.8.8.8
   ... 
```
This file is a list of IP addresses from which a login was attempted.  The list may contain hundreds or thousands of entries with some IP addresses appearing many times if the user frequently logs in from the same place.  FRAUD means that this IP was used for a known fraudulent login attempt, and LOGIN means this login attempt was not known to be fraudulent.   

Given this file, score a new login attempt using the following criteria: 
* Let the "distance" between two IP addresses be the physical distance between the IP’s latitude/longitude coordinates. You can use IPinfo.io for latitude/longitude location information, and you may use the latitude/longitude distance formula of your choice. 
* The score will be the mile distance between the new login IP and the closest IP found in the input list. 
* If the closest previous IP was marked as FRAUD, we double the score before returning your final answer.

## Approach

I use the Vincenty distance formula to calculate the distance between 2 IP addresses. Vincenty's formulae are two related iterative methods used in geodesy to calculate the distance between two points on the surface of a spheroid. They are based on the assumption that the figure of the Earth is an oblate spheroid, and hence are more accurate than methods such as great-circle distance which assume a spherical Earth.

Rest of the code is pretty straightforward has I go through the previous records file to find the closest IP by distance and return a score based on whether it was fraudulent or not.

*Note: I'm comparing the first occurence of the closest IP in the records file. Uncomment line 74 for using the last occurence. Also, I didn't bother removing the access token here for ease of running the script*

## Try It Out

* Clone the Repo-  
`$ git clone https://github.com/kev5/fraud-detection.git`

* Install Dependencies-  
`$ pip install -r requirements.txt`

* For running this application-  
`$ python fraud_score.py 68.181.88.8 login_records.txt`

## Follow Up Questions

* What circumstances may lead to false positives or false negatives when using solely this score?  

   - One of the questions I had was whether the previous login records list will be arranged in an orderly manner. In the case where a single IP address has multiple login entries which may contain both, `FRAUD` as well as `LOGIN` statuses, which record should we give more weight to? The oldest one or the newest one? Or do we add more metrics for calculating a score?

* What challenges are there with computing distances based on latitude/longitude?  

   - Computing distances based on latitude/longitude might not be the most accurate metric when it comes to a case when the IP addresses are very close to each other.

## Further Considerations

* I'd like to add more metrics in calculating the score of the new login attempt. For example, defining the type of `FRAUD` in more detail. Was it just a login attempt with a wrong password by accident?
* Also, a timestamp for the login records might help as well. For example, if the user logged in from Las Vegas on Sunday morning and we see a login attempt from China in the afternoon same day, there might be something of our interest there.
