"""Create and verify the independent INSTANT training submission package."""
from __future__ import annotations
import hashlib, json, shutil, subprocess, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEST=Path('/Users/fariskishtah/INSTANT_AI_Training_Submissions/SPRINT_4_GAN_AND_AGENTS/05_ProcurePilot_AI')
COMMIT=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
FILES=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
DEST.mkdir(parents=True,exist_ok=True)
for child in DEST.iterdir():
    if child.name in {'ProcurePilot_AI_Submission.zip','ProcurePilot_AI_Submission.zip.sha256'}: child.unlink()
    elif child.is_dir(): shutil.rmtree(child)
    else: child.unlink()
project=DEST/'02_PROJECT_FILES'
for relative in FILES:
    source=ROOT/relative
    target=project/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
(DEST/'03_DOCUMENTATION').mkdir()
for name in ['README.md','PROJECT_STATUS.md']:
    shutil.copy2(ROOT/name,DEST/'03_DOCUMENTATION'/name)
for source in (ROOT/'docs').glob('*.md'): shutil.copy2(source,DEST/'03_DOCUMENTATION'/source.name)
shutil.copytree(ROOT/'artifacts'/'screenshots',DEST/'04_SCREENSHOTS')
(DEST/'05_RESULTS').mkdir()
shutil.copy2(ROOT/'examples'/'verified_empty_evidence_trace.json',DEST/'05_RESULTS'/'Verified_CrewAI_Execution_Trace.json')
(DEST/'06_PROCUREMENT_REPORTS').mkdir()
shutil.copy2(ROOT/'examples'/'ProcurePilot_Procurement_Report.html',DEST/'06_PROCUREMENT_REPORTS'/'ProcurePilot_Procurement_Report.html')
(DEST/'07_RESEARCH_REPORT').mkdir()
shutil.copy2(ROOT/'ProcurePilot_AI_Research_Report.pdf',DEST/'07_RESEARCH_REPORT'/'ProcurePilot_AI_Research_Report.pdf')
(DEST/'01_GITHUB_PROJECT.md').write_text(f'# GitHub project\n\nPublic repository: https://github.com/fariskishtah/procurepilot-ai\n\nBranch: main\n\nVerified commit: {COMMIT}\n\nStatus: partial academic assignment; no supplier recommendation.\n')
(DEST/'README_FIRST.md').write_text('# ProcurePilot AI submission\n\nThis package is PARTIAL. A real six-task CrewAI sequential run completed. Tavily was blocked by missing credentials; no approved supplier data or verified prices were collected. The HTML report therefore makes no purchase recommendation. Start with 03_DOCUMENTATION/PROJECT_STATUS.md.\n')
(DEST/'HOW_TO_RUN.md').write_text('# How to run\n\nSee 02_PROJECT_FILES/README.md. On macOS with Python 3.12 and Ollama, install pyproject.toml dependencies in a virtual environment, pull qwen2.5:1.5b-instruct, run pytest, then launch Streamlit. No Tavily key is needed to reproduce the empty-evidence CrewAI workflow.\n')
(DEST/'SUBMISSION_CHECKLIST.md').write_text('# Checklist\n\n- [x] Source, tests, license, docs\n- [x] Genuine CrewAI trace\n- [x] Browser screenshots and HTML report\n- [x] Research PDF\n- [x] ZIP and SHA-256 (verified by packaging script)\n- [ ] Live Tavily search\n- [ ] Permitted supplier extraction\n- [ ] CrewAI agent tool invocation\n- [ ] Source-backed recommendation\n- [ ] Free hosting\n')
manifest=[]
for file in sorted(DEST.rglob('*')):
    if file.is_file() and not file.name.startswith('ProcurePilot_AI_Submission.zip'):
        manifest.append({'path':str(file.relative_to(DEST)),'size':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(DEST/'ARTIFACT_MANIFEST.md').write_text('# Artifact manifest\n\n'+f'{len(manifest)} files before this manifest; Git commit {COMMIT}.\n\n'+'\n'.join(f"- `{x['path']}` — {x['size']} bytes — SHA-256 `{x['sha256']}`" for x in manifest)+'\n')
zip_path=DEST/'ProcurePilot_AI_Submission.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(DEST.rglob('*')):
        if file.is_file() and file!=zip_path and file.name!='ProcurePilot_AI_Submission.zip.sha256': archive.write(file,file.relative_to(DEST))
with zipfile.ZipFile(zip_path) as archive:
    assert archive.testzip() is None
    names=archive.namelist()
    assert '06_PROCUREMENT_REPORTS/ProcurePilot_Procurement_Report.html' in names
    assert '07_RESEARCH_REPORT/ProcurePilot_AI_Research_Report.pdf' in names
    assert not any(name.endswith('.zip') for name in names)
    with tempfile.TemporaryDirectory() as folder:
        archive.extractall(folder)
        for name in names:
            assert (Path(folder)/name).read_bytes()==(DEST/name).read_bytes()
checksum=hashlib.sha256(zip_path.read_bytes()).hexdigest()
(DEST/'ProcurePilot_AI_Submission.zip.sha256').write_text(f'{checksum}  {zip_path.name}\n')
print(json.dumps({'folder':str(DEST),'zip':str(zip_path),'files':len(names),'size':zip_path.stat().st_size,'sha256':checksum,'commit':COMMIT},indent=2))
