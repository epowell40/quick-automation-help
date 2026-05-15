# CSV Cleanup Sample

This is a safe public example of the kind of small automation included in the $20 quick fix offer.

Run:

```powershell
py clean_csv.py messy_contacts.csv cleaned_contacts.csv
```

Output:

- trims messy headers and cells
- lowercases email addresses
- normalizes common 10-digit US phone numbers
- removes duplicate contacts by email
