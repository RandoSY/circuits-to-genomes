"""Verify the v11 source and publish the integrated PDF; no previous manuscript is overwritten."""
from pathlib import Path
import hashlib, json, subprocess, sys
import fitz
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
manifest=json.loads((src/'RELEASE_MANIFEST.json').read_text())
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in manifest['sources'].items():
    assert sha(src/n)==h, 'Source checksum mismatch: '+n
baseline=src.parent/'Architectural_Economy_v9.pdf'
assert sha(baseline)==manifest['baseline_sha256']
pdf=src.parent/manifest['pdf']
assert not pdf.exists(), 'Refusing to overwrite an existing v11 PDF'
subprocess.run([sys.executable,str(src/'build.py'),'--baseline',str(baseline),'--out',str(pdf)],check=True)
with fitz.open(pdf) as doc:
    pages=len(doc)
    text='\n'.join(p.get_text() for p in doc)
    assert 29<=pages<=37,(pages,'Unexpected page count')
    for phrase in ['H100','H1-D','H3-D','K562','Figure 17.','Table 10.','References']:
        assert phrase in text, 'Missing expected text '+phrase
digest=sha(pdf)
published={'pdf':str(pdf.relative_to(root)),'sha256':digest,'bytes':pdf.stat().st_size,'pages':pages,'source_local_pdf_sha256':manifest['local_pdf_sha256'],'matches_local_pdf_bytes':digest==manifest['local_pdf_sha256'],'validation':'Source and baseline checksums, PDF render, page count and selected text checks. No scientific rerun.'}
(src/'PUBLISHED.json').write_text(json.dumps(published,indent=2)+'\n')
print(json.dumps(published,indent=2))
# Keep existing v10 expanded review links and historical baseline records.
r=root/'README.md'
t=r.read_text()
old='Architectural_Economy_v10.pdf) | v10 · 26 Nov 2026 · 28 pages'
new='Architectural_Economy_v11.pdf) | v11 · 26 Nov 2026 · '+str(pages)+' pages'
assert old in t,'Unexpected master index format'
t=t.replace(old,new,1)
t=t.replace('## Coordinated research revision — 26 November 2026','## Paper 1 — integrated v11\n\n[Integrated v11 PDF](papers/01-architectural-economy/Architectural_Economy_v11.pdf) · [Editable source, build and revision record](papers/01-architectural-economy/source-v11/) · [Publication verification](papers/01-architectural-economy/source-v11/PUBLISHED.json). The H100 architecture and the two CPU parallel-workload studies now appear in the main argument. No hardware measurement or new genomic result is claimed. v10 and all earlier versions remain preserved.\n\n## Coordinated research revision — 26 November 2026',1)
t=t.replace('| Paper | Latest expanded review edition |','| Paper | Latest review manuscript |',1)
r.write_text(t)
r=root/'papers/README.md'
t=r.read_text()
t=t.replace('## Latest review editions','## Integrated Paper 1 v11\n\n- [Architectural Economy v11 (PDF)](01-architectural-economy/Architectural_Economy_v11.pdf) · [Source, figures and revision history](01-architectural-economy/source-v11/) · [Verified publication record](01-architectural-economy/source-v11/PUBLISHED.json).\n\n## Coordinated review editions (v10 / v1.2 / v0.5)',1)
r.write_text(t)
r=root/'docs/PUBLICATION_STATUS.md'
t=r.read_text()
t=t.replace('## Coordinated review editions','## Latest integrated Paper 1 edition\n\n| Paper | Version | Pages | Status |\n|---|---|---:|---|\n| [Architectural Economy](../papers/01-architectural-economy/Architectural_Economy_v11.pdf) | 11 | '+str(pages)+' | Published, source checksums verified |\n\nThe latest three review manuscripts total '+str(pages+21+19)+' pages (v11 / v1.2 / v0.5). [v11 revision and source record](../papers/01-architectural-economy/source-v11/REVISION.md); [publication hash](../papers/01-architectural-economy/source-v11/PUBLISHED.json). No new experiments were run; independent review remains outstanding.\n\n## Coordinated review editions',1)
r.write_text(t)
r=root/'papers/SHA256SUMS.txt'
t=r.read_text().rstrip()+'\n'+digest+'  '+str(pdf.relative_to(root))+'\n'
for name in sorted(manifest['sources']):
    t+=sha(src/name)+'  '+str((src/name).relative_to(root))+'\n'
r.write_text(t)
r=root/'docs/RECIPROCAL_RESEARCH_ROADMAP.md'
t=r.read_text().rstrip()+'\n\n## Integrated manuscript checkpoint — Paper 1 v11\n\n[Read v11](../papers/01-architectural-economy/Architectural_Economy_v11.pdf) · [Source and revision history](../papers/01-architectural-economy/source-v11/REVISION.md). The modern parallel-computing work is integrated in the main narrative; the actual H100 measurement and a cost-matched biologically inspired return experiment remain prospective. Preserve prior versions, source and figures, hashes, negative results and unresolved verification gates for each revision.\n'
r.write_text(t)
