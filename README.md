# okuma-resume

Scott Okuma's web and PDF resume, focused on spacecraft platform software,
embedded Linux, autonomous recovery, and engineering leadership.

- Open `index.html` to view the web resume.
- Download [Resume - Okuma.pdf](Resume%20-%20Okuma.pdf) for the printable version.

## Updating the resume

`index.html` is the source of truth for resume text. The PDF builder reads its
`data-pdf` elements, so changes to experience, dates, and skills stay synchronized.
Company/project images and web navigation are excluded from the PDF.

After editing the HTML, regenerate the PDF from the repository root:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_resume_pdf.py
```

The builder uses Python 3 and ReportLab. To preview a separate output, use
`--output /path/to/resume.pdf`. Review both PDF pages after rebuilding, particularly
when changing text length. Commit the HTML and generated PDF together.
