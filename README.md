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

## Google Quantum AI resume

A separate version tailored to **Technical Program Manager, System Integration,
Quantum AI** in Goleta ([job 135168602138387142](https://www.google.com/about/careers/applications/jobs/results/135168602138387142-technical-program-manager-system-integration-quantum-ai)).

- Source/web resume: [google-quantum-tpm.html](google-quantum-tpm.html)
- Printable resume: [Scott-Okuma-Google-Quantum-AI-TPM.pdf](Scott-Okuma-Google-Quantum-AI-TPM.pdf)

This version emphasizes technical project leadership, cross-functional hardware/software
integration, RF engineering, process development, and system verification. Employment
titles and dates are retained. It does not claim direct quantum-computing experience
or unverified budget, supply-chain, inventory, or vendor-management responsibilities.

Rebuild this version independently:

```sh
python3 scripts/build_resume_pdf.py --source google-quantum-tpm.html --output Scott-Okuma-Google-Quantum-AI-TPM.pdf
```

Review both pages after rebuilding. Commit the HTML and PDF together.
