# Sales Data Cleaner

## Project Title & Goal
Cleans messy sales CSV data by removing duplicates and converting USD prices to INR, then saves it as JSON.

## Setup Instructions
```bash
python main.py
```

That's it! No external packages needed - just Python 3.6+

## The Logic (How I Thought)

### Why I chose this approach

I broke down the problem into smaller steps - read the CSV, clean the messy fields (remove $ signs and quotes), find duplicates, convert currency, and save as JSON. 

The main reason I used the standard csv module instead of pandas was because the problem said no external dependencies. Also, for a small dataset like this, csv module works fine and keeps things simple.

For duplicate detection, I used a set with tuples of (product_name, price). So when I see the same product with the same price again, I just skip it. I kept the first occurrence because that seemed like the right thing to do.

I also added print statements at each step - mainly because when I was testing, I wanted to see if duplicates were actually getting removed or not.

### Hardest bug I faced and how I fixed it

Honestly, the duplicate detection gave me the most trouble. 

Initially, I was checking for duplicates right after reading the CSV using the raw string values. But then I noticed row 1 had `"$10.50"` and row 3 had `10.50` (no dollar sign). After cleaning, they looked the same, but when I printed them out, one was still a string `"10.50"` and I hadn't converted it to float yet in that version of my code.

So duplicates weren't being caught properly. I had to restructure it:
1. Clean ALL fields first (remove $, quotes, whitespace)
2. Convert price to float right after cleaning
3. THEN check for duplicates using the float value

This way both `$10.50` and `10.50` become `10.5` (as float) and get detected as duplicates correctly.

Lesson learned: convert data types early so you're comparing the right things.

## Output Screenshots

Here's what the `clean_sales.json` file looks like when opened in a text editor:

![Screenshot of clean_sales.json](screenshot_clean_sales.png)

As you can see, the output contains 2 records instead of the original 3 - the duplicate Widget A entry (row 103) was successfully removed. The prices are now in INR (871.5 and 415.0) instead of USD, converted at the rate of 1 USD = 83 INR.

## Future Improvements

If I had 2 more days, here's what I'd probably add:

**Configuration stuff**
- The conversion rate (83) is hardcoded right now. Would be better to put it in a config file or take it as a command line argument
- Same thing for the input/output file names

**Better error handling**
- What if someone gives a completely messed up CSV? It might crash
- Could add validation for country codes, product ID formats, etc.

**Handle different CSV formats**
- Right now I'm assuming there's no header row. Some CSVs have headers though
- Different delimiters (sometimes semicolons instead of commas, or tabs)
- Auto-detect these would be nice

**Add some tests**
- Should write unit tests for each function
- Test edge cases like empty files, files with all duplicates, weird characters in names

**Track performance**
- Add a timer to see how long it takes
- Might be useful if running on really large files

**Generate a report**
- Show total records, duplicates found, maybe average price or something
- Would help catch issues if the numbers look weird