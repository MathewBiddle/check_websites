# check_websites

Credit to @sdiggs for the script.

This repository checks a collection of urls and tests accessibility of web and FTP sites automatically every hour using GitHub Actions and presents the results as an HTML table using GitHub Pages. You can see the resultant table at https://mathewbiddle.github.io/check_websites/table.html. More details about the main tools can be found below.

## check_websites.py

This code collects, combines, and tests the accessibility of web and FTP sites, then logs the results with timestamps. It begins by loading a local JSON file (`websites.json`) containing URLs, then downloads a second dataset maintained by NOAA’s Changing, Ecosystems, and Fisheries Initiative ([CEFI](https://www.fisheries.noaa.gov/resource/document/noaa-climate-ecosystems-and-fisheries-initiative-fact-sheet)) (source file: https://github.com/NOAA-CEFI-Portal/CEFI-info-hub-list). After merging both lists and removing duplicate URLs, it determines the current local date and time for use in labeling output data.

The script defines two main functions:

* **`check_ftp_status()`** — attempts an anonymous login to an FTP server, listing its contents to confirm accessibility.
* **`check_url()`** — checks whether a given URL is reachable, using `requests.head()` for web addresses and delegating to `check_ftp_status()` for FTP sites.

For each URL, the script prints and records the connection result (HTTP status code or error message) in a new column labeled with the current timestamp. Finally, it saves the combined dataset—with each URL and its latest status—to a CSV file called `website_status.csv`.

## build_webpages.py
This Python script turns a CSV of website status results into a clean, styled HTML dashboard showing which sites are working and which are not.

1. **Template loading and setup**

   * The `load_template()` function locates a `templates` directory, initializes a Jinja2 environment, and loads an HTML template named `table.html`.
   * The `write_html_index()` function creates a `docs` directory (if it doesn’t already exist) and writes the rendered HTML output to `docs/table.html`.

2. **Data processing**

   * In the `main()` function, the script reads a CSV file (`website_status.csv`) containing URLs and their connection statuses (e.g., HTTP status codes).
   * It identifies the most recent “status” column using a regular expression.
   * It then adds a new column, **`functioning`**, that visually represents website health:

     * ✅ (checkmark) for sites returning HTTP 200 (OK)
     * ❌ (x mark) for sites returning 403 or anything else

3. **HTML rendering**

   * The script converts the DataFrame into an HTML table using `pandas.DataFrame.to_html()`, preserving clickable links and applying a CSS class for styling.
   * The HTML table is inserted into the Jinja2 template and written to a static HTML file in `docs/table.html`.

4. **Execution**

   * When run directly (`__main__`), it sets up a title configuration and calls `main(configs)` to produce a formatted HTML page titled “Table of website status.”


