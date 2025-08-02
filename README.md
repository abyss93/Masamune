<img src="https://github.com/abyss93/masamune/blob/master/logo/Masamune_logo.jpg?raw=true" style="width:200px;heigth:200px;">
<img src="https://github.com/abyss93/masamune/blob/master/logo/Masamune_name.jpg?raw=true" style="width:300px;heigth:40px;">
<h3>What is?</h3>
This is a tool to help analysts to analyze emails.
Given an email, the tool creates an HTML report with insights and security info based on feeds that can be configured adding elements to the feeds.py file.

<h3>Usage</h3>

```
usage: masamune.py [-h] [-H] [-p] [-a] [-d] [-c] email_path

 -- Masamune -- Email Forensic and Analysis Tool --

positional arguments:
  email_path            Path of the email to analyze (EML format)

optional arguments:
  -h, --help            show this help message and exit
  -H, --headers         Print email headers in a friendly way (default: True)
  -p, --print-payload   Print email payloads as they are (default: False)
  -a, --payload-analysis
                        Payload analysis: hashes, URLs... (default: False)
  -d, --debug           Debug info to stdout (default: False)
  -c, --color           Some output sections are printed using terminal colors (default: False)
```

Be sure to create a config.yml based on the included config_sample.yml
Some directories are needed to store the feed files and the reports generated as a results of the executino of the tool.
Be also sure to fill the feeds.py file with the sources of the IoC/feeds

<h3>Security</h3>

Opening mail with this tool should be safe enough as EML files are read and interpreted as text files, so nothing will be executed and nothing malicious should be triggered unless Python itself contains vulnerable code in the file read method (very unlikely, but nothing is impossible).

<h3>Feeds</h3>

More feed can be added, one very good feed is for example https://phishing.army/, that is provided as an example, along with urlhaus.abuse.ch.
I want to thank the maintainers of those feeds.

<h3>Credits</h3>

This project makes use of the following components:
- "Analytics Template" by https://www.w3schools.com/w3css/w3css_templates.asp<br>
As of today, the page states:
<i>"We have created some responsive W3.CSS website templates for you to use.
You are free to modify, save, share, and use them in all your projects."</i><br>
Should this ever change for whatever reason I'll adapt the projects accordingly to reflect the authors will.
I also want to give credits to the authors of the CSS used in the template:<br>
<i>W3.CSS 5.02 March 31 2025 by Jan Egil and Borge Refsnes [...]<br>
[...] Extract from normalize.css by Nicolas Gallagher and Jonathan Neal git.io/normalize [...]</i>
- The "treeview" component is based on https://www.w3schools.com/howto/howto_js_treeview.asp with some changes/improvements to adapt to my needs for the project

I want to thank all the authors of these resources.

These freely available feeds have been used as an example, but their files are <b>not</b> provided with this project.
- https://phishing.army/download/phishing_army_blocklist_extended.txt
- https://urlhaus.abuse.ch/downloads/text/

I want to thank the authors of these resources.

<h3>Next...</h3>

<ul>
<li>Better payload analysis (magic bytes, internal URLs, internal JS, etc)</li>
<li>Code quality (remove duplication, use patterns, etc) and test coverage</li>
<li>Better debug output</li>
<li>HTML output improvements</li>
<li>X-Headers analysis</li>
<li>dig txt record to better investigate sender DNS</li>
<li>some analysis on spf, dkim, dmarc</li>
</ul>
