# here I can define any services I want to be used as an IoC provider following the standard below
#{
#        "name": feed name,
#        "url": feed file download url,
#        "update_interval_minutes": to avoid being blacklisted, always follow policies of the feed provider,
#        "filename": name assigned to downloaded feed file,
#        "check_what": "domain/ip/both/...other things?..."
#}
FEEDS = [
    {
        "name": "phishing.army",
        "url": "https://phishing.army/download/phishing_army_blocklist_extended.txt",
        "update_interval_minutes": 1440, # always be respectful of the provider
        "filename": "phishing_army_blocklist_extended.txt",
        "check_what": "domain" # I will use this feed to check domains
    }
]