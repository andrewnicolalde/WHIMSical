# WHIMSical - Where the HELL Is My Stuff?

## Inspiration

Ever walked into a meeting room and found all the whiteboard pens missing? Pesky co-workers stealing your food? And where the hell is your keyboard? Well no more! Presenting WHIMSical, the world's cheapest bit of desk defense kit.

## What it does

WHIMSical is a unique piece of software which automatically captures, identifies and logs items left on your desk. When a relevant action observed, such as when an item is added or removed, the action is logged for review by you, the indignant victim of theft.

![Headphones nicked again... >:(](https://i.imgur.com/aUNHAJz.jpg)

You can also ask Alexa to tell you what, if anything, is missing from your desk!

## How we built it

WHIMSical is designed in two components. A Raspberry Pi + Camera attachment monitors your desk at all times for signs of movement. Once movement is detected, an image is captured and uploaded to a highly advanced™ serverless object recognition service built on AWS Rekognition. Objects are identified, classified and compared to previous images in order to find out which new objects have been taken or added to the desk.

This information is, of course, logged in a database and presented via a friendly web UI to the poor guy who won't, in fact, be enjoying his breakfast croissant today.

## Challenges we ran into

Originally we designed the application around the services offered by Google Cloud Platform, many of which are similar in nature to those offered by Amazon Web Services. Unfortunately, these services, namely the Rekogiition competitor GCP Vision AI, lacked the maturity and accuracy we required in order to build a useful product.

We also had hardware issues initially using the Raspberry Pi 4, however after downgrading to a Model 2B these issues were resolved. In the end, we had to ensure our code was more efficient for the less powerful processor.

## Accomplishments that we're proud of

For many of us, this was our first ever serverless application and there were many nuances and particularities we needed to become familiar with in order to ensure that this was a success.

There were many components from physical hardware to cloud-based lambdas which needed to fit together seamlessly, and we're proud to report they do!

## What we learned

Serverless application design is fundamentally different from typical client-server architectures in that it it's primary strength lies in the programmer making use of all of the other services offered by the cloud provider.

Amazon Web Services have developed a truly remarkable offering of inter-connectable services, each with significant capabilities. Having a chance to use these services ourselves, it's no longer any mystery why the guys in Seattle are eating everyone's lunch.

## What's next for WHIMSical?

I need this in my house, my office and most importantly the FRIDGE!
Next feature to be added in the coming days is automated notification emails courtesy of Amazon SES.