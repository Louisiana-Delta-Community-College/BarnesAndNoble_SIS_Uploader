# used by main.py
_SCHOOL_NAME         = ""
_ZIP_FILE_NAME       = _SCHOOL_NAME+".bncroster.zip"
_WRITE_CSV_TO_DISK   = False
_WRITE_ZIP_TO_DISK   = False
_UPLOAD_FILES_TO_AWS = True
_IS_VALIDATION       = False

if _IS_VALIDATION:
  _DESTINATION         = "inbox/validation/"
else:
  _DESTINATION         = "inbox/"


# used by Queries.py
_EMAIL_DOMAIN                   = "someschool"
_EMAIL_DOMAIN_WITH_EXT          = "someschool.edu"
_EMAIL_DOMAIN_ADJUNCT_WITH_EXT  = "[subdomain.]someschool.edu"
_YEARS_OF_HISTORICAL_DATA       = 1

_TIME_FRAMES = {
  "CURRENT": "stvterm.stvterm_end_date >= current_date",
  "HISTORICAL": """stvterm.stvterm_end_date <= current_date
  and stvterm.stvterm_start_date >= to_date((extract(month from current_date)||'-'||extract(day from current_date)||'-'||(extract(year from current_date)-{_YEARS_OF_HISTORICAL_DATA})), 'MM-DD-YYYY')""".format(**locals()),
}

# Choices are "CURRENT" or "HISTORICAL"
# "HISTORICAL" also requires the number of previous years to include
_TIME_FRAME  = _TIME_FRAMES["CURRENT"]