# IWBT: I Went Boating Today
<h3>Rob Hurst and Exley McCormick<br>
Summer 2015</h3>
<h4>NOTE: THIS IS TURNING INTO A DESIGN DOC NOW. NEED TO MAKE A DESIGN DOC SEPARATE FROM README.md; CREATE A DesignDocs DIRECTORY AND DO THIS STUFF THERE.</h4>

I Went Boating Today (IWBT) is a mobile solution to the information problems arising in the whitewater community. In the first round of design and development, the features we hope to implement are:
<ol>
	<li>Easily accessable realtime flow data
	<li>Google Maps integration to allow for improved navigation to put ins and take outs.
	<li>Paddling Logs
</ol>
I went boating today is designed as a mobile app front-end with web and back-end support provided for various features. Most of the real work will be done back-end and the app itself should just be a gui/wrapper for the back-end support (I think.)
<br><br>
<b>Part 1: Easily Access realtime flow data</b><br>
Flow data is available from the <a href='http://waterservices.usgs.gov/'>USGS Website</a>. Their API returns river gauge information in XML format. We have written a simple XML parser to pull relevant data from the return string.

Example (pseudocode) python object for parsing XLM from USGS

```python
class DataReader(object):
	def get_flow(gauge=None)
		# Take optional input of gauge
		# return flows for all defined gauges.
		self._get_flow_xml()
		self._parse_flow_xml()
		
		# return flow for individual gauge
		return self.gauges[gauge]
		# or if gauge was left blank
		retur self.gauges
		
```

This parser runs on the back-end to keep the database continuously updated, and the front end simply references the up-to-date tables.
<br><br>
<b>Part 2: Google Maps Layovers</b><br>
Gonna need some professional help on this part. GIS layovers, Google Maps API, getting Lat/Long data for access and rapids, mapping it to RiverId and RapidId, etc.
<br><br>
<b>Part 3: Paddling Log</b><br>
So far, we have the basic idea mapped out as a database, but we need to get some help here for how to make it easy to customize your own fields in this table. Basically, we need to be able to add custom user paddling logs for people like 'u/rob' who like to have lots of creative control.
<br><br>
The basic idea goes something like this:
<ul>
	<li>Start with a pretty basic template
		<ol>
			<li>Where did you go?
			<li>What Date / Time did you go?
			<li>Who did you go with?
			<li>Where did you put on?
			<li>Where did you take out?
			<li>Who did you go with?
		</ol>
	<li>Give some pre-made "optional" questions that you can add to your defaults
		<ol>
			<li>Did You Swim?
				<ul>
					<li>Which rapids? Check all that apply.
					<li>Did you self rescue?
					<li>Who got your boat?
					<li>What kind of bootie beer did you drink?
				</ul>
			<li>What did you paddle?
				<ul>
					<li>User can pick from list of "owned" boats or enter text.
				</ul>
			<li>What was the weather like? (If we cant/don't integrate with NOAA for weather)
				<ul>
					<li>Frozen wasteland
					<li>Cold, wet, and miserable
					<li>Cold (but I was dry)
					<li>Chilly
					<li>etc? Or just a temperature band (<35, 35-50, etc)
				</ul>
		</ol>
</ul>
On the idea of allowing users to select boats as part of the paddling log, perhaps we create a Boat class that can be used in this situation and for any other references to a specific boat -- gear swaps, boat use analytics:

```python
class Boat(object):
	# Attributes
	self.name
	self.type
	self.brand
	self.model
	self.color?
	self.size?
	self.picture_url
	
	# Methods?
```
As well as a boat / trip mapping that basically keeps track of your "favorite" boats along with your favorite rivers. This would, eventually, allow boats to take on character the way users do. If you get drunk and smash up the front of your boat paddling the 12 mile at flood stage, that damage gets tagged to that boat and that run. Then if you go to your user page, you can see your boats, click on them, and see their story. This need not introduce any particular extra work from the user, but rather just a different way to explore or filter one's paddling log from a different perspective ("when was the last time I paddled the Remix?")
