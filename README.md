`daniels-running-formula-to-intervals` takes a runnings workout in the form of "6 E + 5 x (3 min I w/2 min jg recoveries) + 6 x (1 min R w/2 min jg) + 2 E" and sends it to Intervals.icu as a workout.

## Usage

There are no dependencies, so usage is as simple as:

```
python3 cli.py
```

The CLI will prompt you for your Intervals Athlete ID and Intervals API Key, you can add these as environment variables (`INTERVALS_ALTHETE_ID` and `INTERVALS_API_KEY`) to load them from their instead.


## Notes

The parsing of the DRF string is _hacky_, but it covers the full Q2 plan from the book with the exception of strings like "steady E run of 90-120 min" which needs to be converted to "120 min E".

Also not working: "6 E + 5 x (3 min I w/2 min E) + 4 E". This is because of the "I" and "E" inside the brackets. Will fix on cleanup. Can be converted to "6 E + 5 x (3 min I w/2 min jog recoveries) + 4 E"
