# [★★★] Suspect tracking

## Identification

<details open>
<summary>
Description
</summary>

We received a tip about a dangerous individual who uses various false identities. Several agencies are working to obtain
any new information that could help track down this person. A photograph has been obtained, allegedly taken by the
suspect. Can we learn anything more from it?

[`photo.jpg`](Identification/identification.jpg)

</details>
<details>
<summary>
Solution
</summary>

It seems the `photo.jpg` is
from https://www.tripadvisor.com/Hotel_Review-g608946-d27536201-Reviews-Best_Western_Premier_Malta-St_Paul_s_Bay_Island_of_Malta.html

Identified the hotel in the image and found it on
Google - https://www.google.com/travel/search?q=best%20western%20premier%20malta&g2lb=4965990[…]CCQklcUD-ue1Ax0IJCSVxQP657UDHSAA&ap=MAC6AQdyZXZpZXdz&ictx=111
One of the reviews on that page ^ was made by `cybergameosintplayer` - linked from tripadvisor that says:

> I recently stayed at this hotel and had a pleasant overall experience. The check-in process was smooth and the staff
> were friendly and helpful throughout my stay. …

On Tripadvisor - you can search in the reviews for the first line. Bringing you this review that seems to
match https://www.tripadvisor.com/ShowUserReviews-g608946-d27536201-r1000507523-Best_Western_Premier_Malta-St_Paul_s_Bay_Island_of_Malta.html

Click on the user Jolaus
profile - https://www.tripadvisor.com/Profile/cybergameosintplayer?fid=cf222a74-0656-4ceb-a826-aea95aa2289d and see in
his intro the first flag

```SK-CERT{h0t31_r3vi3w_f14g}```

</details>

## Localization

<details open>
<summary>
Description
</summary>

We have managed to identify the hotel and also a review that was allegedly posted by the wanted individual. The suspect
then left the hotel and has been moving through unspecified locations. The only clue we currently have is a photograph
posted on their profile on the TripAdvisor website.

Can we determine where the photo was taken? Specifically, we are interested in the exact coordinates of the location
from which the photograph was captured.

The flag should be in the format: "Latitude,Longitude", with a precision of five decimal places.

Correct format example (without quotes):

- “27.98800,86.92505”

Incorrect format examples:

- “27.9880,86.92505” – missing decimal digit in latitude
- “27.98800, 86.92505” – space
- “27,98800,86.92505” – comma instead of a dot
- “27.988000, 86.92505” – more than five decimal places

</details>
<details>
<summary>
Solution
</summary>

Identify the image - https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2f/7c/29/1e/caption.jpg - within 5 digits
of latitude/longitude

The Hotel is at "Triq It-Tamar, St. Paul's Bay, Island of Malta SPB 1281 Malta"

It is quickly clear this is "Fungus Rock, Malta" that we are seeing. Problem is finding the exact location with
precision of 5 decimal digits of lat/lng.

I spent some time finding all possible images of Fungus rock that had GPS coordinates to them. I created a project in
Google Earth and marked them all there with pins. Then comparing all of them (their angle, distance, etc.) to the
challenge image, I was able to narrow down an area I believed was where the image was taken.

After a couple of tries, I came up with these coordinates:

```
36.04863,14.19105
```

</details>

## Golden hour

<details open>
<summary>
Description
</summary>

!!WARNING: The number of flag submission attempts is limited to 10 !!

Good work! We have managed to identify the location with an accuracy down to a few centimeters. We know where the
photograph in question was taken and likely also the time it was captured.

Can we determine the exact date when the photograph was taken based on the image?

The flag should be in the format "MMDD", e.g., if it was taken on February 14th, the flag would be "0214".

!!WARNING: The number of flag submission attempts is limited to 10 !!

</details>
<details>
<summary>
Solution
</summary>

So, we know the location of the image now, we see how high the sun is above the horizon. I figured the best would be to
use one of many libraries that can calculate sunset time and sun azimuth at a specific time.

I used [SunCalc](https://www.suncalc.org/) to determine the approximate azimuth of the sun in the image—just by moving
the sun around until the azimuth line roughly matched with the peninsula—compared to the image. By doing that I figured
the azimuth of the sun at the time in the image must be around 246° approximately.

Then I wrote [`golden_hour.py`](Golden%20Hour/Solution/golden_hour.py) to calculate the sunset times + azimuth of the
sun at 17:14—the time on the picture. I then split it up by what I thought was close enough to my estimate:

```
there are probably too early, sunset the pic is at least 4-5 minutes away
date 2025-01-17 - sunset at 17:14, azimuth at 17:14 is 244.798
date 2025-01-18 - sunset at 17:15, azimuth at 17:14 is 244.912
date 2025-01-19 - sunset at 17:16, azimuth at 17:14 is 245.032
date 2025-01-20 - sunset at 17:17, azimuth at 17:14 is 245.159

somewhere here?
date 2025-01-21 - sunset at 17:18, azimuth at 17:14 is 245.293
date 2025-01-22 - sunset at 17:19, azimuth at 17:14 is 245.433
date 2025-01-23 - sunset at 17:20, azimuth at 17:14 is 245.580
date 2025-01-24 - sunset at 17:21, azimuth at 17:14 is 245.733
date 2025-01-25 - sunset at 17:22, azimuth at 17:14 is 245.892
date 2025-01-26 - sunset at 17:23, azimuth at 17:14 is 246.058
date 2025-01-27 - sunset at 17:24, azimuth at 17:14 is 246.230
date 2025-01-28 - sunset at 17:25, azimuth at 17:14 is 246.408
date 2025-01-29 - sunset at 17:26, azimuth at 17:14 is 246.592
date 2025-01-30 - sunset at 17:27, azimuth at 17:14 is 246.783
date 2025-01-31 - sunset at 17:28, azimuth at 17:14 is 246.980
date 2025-02-01 - sunset at 17:29, azimuth at 17:14 is 247.182

these are probably too late (past sunset) or azimuth too high
date 2025-02-02 - sunset at 17:31, azimuth at 17:14 is 247.391
date 2025-02-03 - sunset at 17:32, azimuth at 17:14 is 247.605
date 2025-02-04 - sunset at 17:33, azimuth at 17:14 is 247.825
date 2025-02-05 - sunset at 17:34, azimuth at 17:14 is 248.050
date 2025-02-06 - sunset at 17:35, azimuth at 17:14 is 248.282
date 2025-02-07 - sunset at 17:36, azimuth at 17:14 is 248.519
date 2025-02-08 - sunset at 17:37, azimuth at 17:14 is 248.761
date 2025-02-09 - sunset at 17:38, azimuth at 17:14 is 249.008
date 2025-02-10 - sunset at 17:39, azimuth at 17:14 is 249.261
```

After a few tries I came up with the answer - `0130`. That actually fairly precisely matched by azimuth estimate of
246° - it was 246.783°.

</details>
