# Bulk File Renamer Sample

This is a small, safe example of the kind of local automation task that fits the $20 Python scripting gig.

It reads `file_manifest.csv`, checks a local input folder, and prints the rename operations it would perform. By default it runs in dry-run mode so the example does not modify files.

Run it:

```powershell
python rename_files.py --manifest file_manifest.csv --folder sample_files
```

Apply changes after reviewing the dry run:

```powershell
python rename_files.py --manifest file_manifest.csv --folder sample_files --apply
```

This sample does not require credentials, private files, or API keys.
