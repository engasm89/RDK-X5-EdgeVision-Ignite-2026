# GitHub publication — prepared, NOT published

The connected GitHub account is **engasm89** (verified 2026-11-06). GitHub connector tools can push text content to EXISTING repositories, but do not provide a CREATE-REPOSITORY action in the present session. An unrelated repository must not be repurposed as this competition project.

## Step 1 (owner action, about 30 seconds)
Open https://github.com/new while logged in as `engasm89` and create a **Public** repository named exactly `RDK-X5-EdgeVision-Ignite-2026`.
Leave `Add README`, `.gitignore` and `License` **unchecked**, because those files already exist here.

## Step 2 (push)
On a machine with Git and authenticated GitHub push access, unzip the package, open its project directory and run:

```bash
git init -b main
git add .
git commit -m "Prepare RDK X5 EdgeVision Ignite Stage 1"
git remote add origin https://github.com/engasm89/RDK-X5-EdgeVision-Ignite-2026.git
git push -u origin main
```

Or provide the newly created repository URL to ChatGPT with the connected GitHub account, so the repository contents can be uploaded without local Git commands.

## Critical checks

- `/vendor` and `/evidence` binaries/actual photos are gitignored; genuine Stage 1 evidence is uploaded **only after manual security review**.
- Secret files, `.env`, private keys and device serials should never be committed.
- The illustrative `assets/CONCEPT_ONLY_NOT_EVIDENCE.png` is NOT valid competition proof.
- Fill actual metadata and proof links before updating the completion post and official showcase PR.
