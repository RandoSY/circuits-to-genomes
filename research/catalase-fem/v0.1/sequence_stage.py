"""Download exact 2021 protein accession sequences, then compare global alignments.
Requires Python 3, Biopython, network to NCBI. Does not establish structural similarity or functional equivalence.
"""
import csv, json, hashlib, time, urllib.request, urllib.parse, io
from pathlib import Path
from Bio import SeqIO, Align
from Bio.Align import substitution_matrices
from itertools import combinations
p=Path(__file__).parent
rows=list(csv.DictReader((p/'streptomyces_2021.csv').open(newline='')))
out=p/'sequences';out.mkdir(exist_ok=True)
seqs={}; provenance=[]
for r in rows:
    acc=r['accession'];dest=out/(acc+'.fasta')
    url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urllib.parse.urlencode({'db':'protein','id':acc,'rettype':'fasta','retmode':'text','tool':'c2g_catalase'})
    if not dest.exists():
        with urllib.request.urlopen(url,timeout=45) as response: raw=response.read()
    else: raw=dest.read_bytes()
    rec=SeqIO.read(io.StringIO(raw.decode()),'fasta')
    if acc not in rec.id.split('|') and rec.id!=acc: raise ValueError(f'Accession mismatch {rec.id} != {acc}')
    if set(str(rec.seq))-set('ACDEFGHIKLMNPQRSTVWY'): raise ValueError(f'Noncanonical residues in {acc}')
    dest.write_bytes(raw);seqs[acc]=str(rec.seq)
    provenance.append({'accession':acc,'length':len(rec.seq),'sha256':hashlib.sha256(raw).hexdigest(),'url':url});time.sleep(.4)
aligner=Align.PairwiseAligner();aligner.mode='global';aligner.substitution_matrix=substitution_matrices.load('BLOSUM62');aligner.open_gap_score=-10;aligner.extend_gap_score=-.5
pairs=[]
for a,b in combinations(seqs,2):
    al=aligner.align(seqs[a],seqs[b])[0]
    x,y=str(al[0]),str(al[1]);paired=[(i,j) for i,j in zip(x,y) if i!='-' and j!='-'];ident=sum(i==j for i,j in paired)
    pairs.append({'a':a,'b':b,'aligned_columns':len(x),'nongap_pairs':len(paired),'identity_over_columns':ident/len(x),'identity_over_nongap_pairs':ident/len(paired),'coverage_a':len(paired)/len(seqs[a]),'coverage_b':len(paired)/len(seqs[b])})
    (out/f'{a}_{b}.txt').write_text(str(al))
(out/'manifest.json').write_text(json.dumps({'sequences':provenance,'alignment':'global BLOSUM62, gaps -10/-0.5, first optimal alignment','pairs':pairs,'warning':'Descriptive paralog comparison; ten pairwise comparisons are dependent.'},indent=2))
print('Completed; send sequences/manifest.json and FASTA files for audit.')
