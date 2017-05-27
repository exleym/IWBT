# IWBT: I Went Boating Today
### Rob Hurst and Exley McCormick
Summer 2015
>I Went Boating Today (IWBT) is a mobile solution to the information problems 
>arising in the whitewater community. 

In the first round of design and development, we will implement these features:
  - Easily accessable realtime flow data
  - Google Maps integration for improved navigation to put ins and take outs.
  - Paddling Logs

I went boating today is designed as a mobile app front-end with web and 
back-end support provided for various features. Most of the real work will be 
done back-end and the app itself should just be a gui/wrapper for the back-end 
support (I think.)  

**Part 1: Easily Access realtime flow data**
Flow data is available from the [USGS Website](http://waterservices.usgs.gov/).
Their API returns river gauge information in JSON format. We have written a 
simple JSON parser to pull relevant data from the return string.

Example (pseudocode) python object for parsing XLM from USGS

```python
class DataReader(object):  
    def get_flow(self, gauge=None):
        # Take optional input of gauge
	    # return flows for all defined gauges.
	    self._read_json(gauge)
        self._parse_flow_xml()
        return self.gauges[gauge]  # return flow for individual gauge
```

This parser runs on the back-end to keep the database continuously updated, 
and the front end simply references the up-to-date tables.  

### Part 2: Google Maps Layovers
Gonna need some professional help on this part. GIS layovers, Google Maps API, 
getting Lat/Long data for access and rapids, mapping it to RiverId and 
RapidId, etc.

### Part 3: Paddling Log
So far, we have the basic idea mapped out as a database, but we need to get 
some help here for how to make it easy to customize your own fields in this 
table. Basically, we need to be able to add custom user paddling logs for 
people like 'u/rob' who like to have lots of creative control.

The basic idea goes something like this:
  - Start with a pretty basic template
    - Where did you go?
    - What Date / Time did you go?
    - Who did you go with?
    - Where did you put on?
    - Where did you take out?
    - Who did you go with?
  - Give some pre-made "optional" questions that you can add to your defaults
    - Did You Swim?
      - Which rapids? Check all that apply.
      - Did you self rescue?
      - Who got your boat?
      - What kind of bootie beer did you drink?
    - What did you paddle?
      - User can pick from list of "owned" boats or enter text.
    - What was the weather like? (If we cant/don't integrate with NOAA for 
    weather)
      - Frozen wasteland
      - Cold, wet, and miserable
      - Cold (but I was dry)
      - Chilly
      - etc? Or just a temperature band (<35, 35-50, etc)

On the idea of allowing users to select boats as part of the paddling log, 
perhaps we create a Boat class that can be used in this situation and for any 
other references to a specific boat -- gear swaps, boat use analytics:

```python
class Boat(object):
	# Attributes
	self.name = None
	self.type = None
	self.brand = None
	self.model = None
	self.color = None
	self.size = None
	self.picture_url = None
	
	# Methods?
```
As well as a boat / trip mapping that basically keeps track of your "favorite" 
boats along with your favorite rivers. This would, eventually, allow boats to 
take on character the way users do. If you get drunk and smash up the front of 
your boat paddling the 12 mile at flood stage, that damage gets tagged to that 
boat and that run. Then if you go to your user page, you can see your boats, 
click on them, and see their story. This need not introduce any particular 
extra work from the user, but rather just a different way to explore or filter 
one's paddling log from a different perspective ("when was the last time 
I paddled the Remix?")
