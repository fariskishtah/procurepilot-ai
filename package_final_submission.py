"""Build a separate verified final package; preserve the original submission."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEST=Path('/Users/fariskishtah/INSTANT_AI_Training_Submissions/SPRINT_4_GAN_AND_AGENTS/05_ProcurePilot_AI')

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def copy(source: Path, target: Path):
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--run-id',required=True)
    p.add_argument('--release-name',default='ProcurePilot_AI_Final_Submission')
    args=p.parse_args()
    if not args.release_name.replace('_','').isalnum(): raise SystemExit('Invalid release name')
    STAGE=DEST/(args.release_name+'_files')
    ZIP=DEST/(args.release_name+'.zip')
    if ZIP.exists() or STAGE.exists(): raise SystemExit('Final package already exists; preserving it. Remove it explicitly to rebuild.')
    trace=ROOT/'artifacts'/'traces'/f'{args.run_id}.json'
    report=ROOT/'artifacts'/'reports'/f'{args.run_id}.html'
    if not trace.is_file() or not report.is_file(): raise SystemExit('Final run artifacts missing')
    result=json.loads(trace.read_text())
    if not result.get('crew_completed') or len(result.get('products',[]))<2 or len({p['source_url'].split('/')[2] for p in result['products']})<2: raise SystemExit('Expected a completed, independent multi-source run')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip(): raise SystemExit('Commit all project changes before packaging')
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    DEST.mkdir(parents=True,exist_ok=True)
    STAGE.mkdir()
    for rel in tracked:
        copy(ROOT/rel,STAGE/'02_PROJECT_FILES'/rel)
    copy(trace,STAGE/'05_RESULTS'/'Final_CrewAI_Execution_Trace.json')
    copy(report,STAGE/'06_PROCUREMENT_REPORTS'/'ProcurePilot_Final_Procurement_Report.html')
    copy(ROOT/'ProcurePilot_AI_Research_Report.pdf',STAGE/'07_RESEARCH_REPORT'/'ProcurePilot_AI_Research_Report.pdf')
    screenshot_dir=ROOT/'artifacts'/'screenshots'/'academic_completion'
    if not screenshot_dir.exists(): screenshot_dir=ROOT/'artifacts'/'screenshots'/'final'
    for shot in screenshot_dir.glob('*.png'):
        copy(shot,STAGE/'04_SCREENSHOTS'/shot.name)
    (STAGE/'README_FIRST.md').write_text(f'# ProcurePilot AI academic completion release\n\nAcademic status: PARTIAL. Run `{args.run_id}` completed six CrewAI tasks and observed {len(result["products"])} direct supplier offers from independent websites. See the trace for agent-selected calls and labeled orchestrator recovery. No purchase recommendation is made because landed cost and ten-unit stock remain unconfirmed. The original laptop scenario remains unverified. Start with `02_PROJECT_FILES/docs/ACADEMIC_COMPLETION_RUN.md`.\n',encoding='utf-8')
    (STAGE/'01_GITHUB_PROJECT.md').write_text(f'# GitHub project\n\nhttps://github.com/fariskishtah/procurepilot-ai\n\nBranch: main\n\nCommit: `{commit}`\n',encoding='utf-8')
    (STAGE/'SUBMISSION_CHECKLIST.md').write_text('# Checklist\n\n- [x] Source, docs, tests and license\n- [x] Genuine six-task CrewAI trace\n- [x] Independent direct supplier price observations\n- [x] Browser screenshots, HTML report and research PDF\n- [x] Agent tool calls and orchestrator recovery distinguished\n- [ ] Original laptop sourcing\n- [ ] Confirmed ten-unit stock, shipping, tax and warranty\n- [ ] Full agent-selected assessment\n- [ ] Tavily live call and free cloud hosting\n',encoding='utf-8')
    paths=[p for p in sorted(STAGE.rglob('*')) if p.is_file()]
    manifest={'commit':commit,'run_id':args.run_id,'files':{str(p.relative_to(STAGE)):{'size':p.stat().st_size,'sha256':digest(p)} for p in paths}}
    (STAGE/'ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(STAGE.rglob('*')):
            if path.is_file(): archive.write(path,path.relative_to(STAGE))
    with zipfile.ZipFile(ZIP) as archive:
        if archive.testzip() is not None: raise RuntimeError('ZIP CRC failure')
        names=archive.namelist()
        if any(name.endswith('.zip') for name in names): raise RuntimeError('Nested ZIP')
        with tempfile.TemporaryDirectory() as folder:
            archive.extractall(folder)
            for name in names:
                extracted=Path(folder)/name
                staged=STAGE/name
                if digest(extracted)!=digest(staged): raise RuntimeError(f'Extraction mismatch: {name}')
    checksum=digest(ZIP)
    (DEST/(ZIP.name+'.sha256')).write_text(f'{checksum}  {ZIP.name}\n',encoding='utf-8')
    print(json.dumps({'zip':str(ZIP),'size':ZIP.stat().st_size,'sha256':checksum,'files':len(names),'screenshots':len(list((STAGE/'04_SCREENSHOTS').glob('*.png'))),'commit':commit,'run_id':args.run_id},indent=2))

if __name__=='__main__': main()
