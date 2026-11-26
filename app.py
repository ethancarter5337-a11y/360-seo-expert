from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from collections import Counter
from bs4 import BeautifulSoup
import re
app=FastAPI(title="360 SEO Expert",version="0.1.0")
class AuditRequest(BaseModel):
    url:str=""
    html:str=""
    keyword:str=""
@app.get("/health")
def health(): return {"status":"ok","app":"360 SEO Expert"}
@app.get("/",response_class=HTMLResponse)
def home():
    return """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>360 SEO Expert</title><style>
    *{box-sizing:border-box}body{margin:0;background:#f4f6fb;color:#172033;font:15px Arial}.top{background:#171d35;color:white;padding:24px 5%;display:flex;justify-content:space-between;align-items:center}.top h1{margin:0;font-size:24px}.wrap{max-width:1100px;margin:32px auto;padding:0 20px}.hero{margin-bottom:24px}.hero h2{font-size:30px;margin:0 0 8px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:white;border:1px solid #e3e7f0;border-radius:14px;padding:22px;box-shadow:0 4px 18px #1720330a}.card h3{margin:0 0 14px}textarea,input{width:100%;padding:12px;border:1px solid #cbd2e1;border-radius:8px;margin:8px 0 14px;font:inherit}textarea{height:180px;resize:vertical}button{background:#5b55d9;color:white;border:0;border-radius:8px;padding:12px 18px;cursor:pointer;font-weight:bold}button:hover{background:#4540b9}.muted{color:#69748a;font-size:13px}.result{white-space:pre-wrap;line-height:1.6;background:#f7f8fc;padding:14px;border-radius:8px;margin-top:14px;min-height:50px}.pill{display:inline-block;background:#eeedff;color:#514bc4;padding:6px 10px;border-radius:20px;font-size:12px}@media(max-width:700px){.grid{grid-template-columns:1fr}.top{padding:20px}.hero h2{font-size:24px}}</style></head><body><header class=top><h1>◈ 360 SEO Expert</h1><span class=pill>SEO WORKSPACE</span></header><main class=wrap><section class=hero><h2>Website SEO Analyzer</h2><p class=muted>Analyze page titles, descriptions, headings, images and keyword usage.</p></section><div class=grid><section class=card><h3>On-page SEO Audit</h3><label>Page URL (optional)</label><input id=url placeholder=https://example.com><label>Paste page HTML / source code</label><textarea id=html placeholder='Paste your page HTML here...'></textarea><label>Target keyword (optional)</label><input id=keyword placeholder='e.g. local SEO services'><button onclick=audit()>Run SEO Audit</button><div id=out class=result>Audit results will appear here.</div></section><section class=card><h3>SEO Content Brief</h3><label>Primary keyword</label><input id=primary placeholder='Enter primary keyword'><label>Related keywords (comma separated)</label><textarea id=related placeholder='secondary keyword, related phrase, search intent'></textarea><button onclick=brief()>Generate Content Brief</button><div id=briefout class=result>Your content brief will appear here.</div></section></div><p class=muted style='margin-top:24px'>MVP version. Search Console, GA4, PageSpeed and live keyword data require API credentials and further integration.</p></main><script>
async function audit(){let o=document.getElementById('out');o.textContent='Analyzing...';try{let r=await fetch('/api/audit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:document.getElementById('url').value,html:document.getElementById('html').value,keyword:document.getElementById('keyword').value})});let d=await r.json();o.textContent=d.report||d.detail||'Audit failed'}catch(e){o.textContent='Could not reach audit service: '+e}}
function brief(){let p=document.getElementById('primary').value.trim(),k=document.getElementById('related').value.split(',').map(x=>x.trim()).filter(Boolean);if(!p){document.getElementById('briefout').textContent='Please enter a primary keyword.';return}document.getElementById('briefout').textContent='H1: '+p+'\n\nSearch intent: Identify the dominant intent before drafting.\n\nSuggested structure:\nH2: What is '+p+'?\nH2: Key benefits and considerations\nH2: How to choose the right solution\nH2: Frequently asked questions\n\nRelated terms to include naturally:\n'+(k.length?k.map(x=>'• '+x).join('\n'):'Add relevant secondary keywords.')+'\n\nEditorial guidance: Answer the reader’s question directly, use original examples, verify claims and avoid keyword stuffing.'}
</script></body></html>"""
@app.post("/api/audit")
def audit(req:AuditRequest):
    html=req.html or ""
    if not html: return {"report":"Please paste the page HTML/source code to run an audit. URL fetching is not enabled in this MVP."}
    soup=BeautifulSoup(html,"html.parser")
    title=soup.title.get_text(" ",strip=True) if soup.title else ""
    desc=soup.find("meta",attrs={"name":re.compile("^description$",re.I)})
    description=desc.get("content","").strip() if desc else ""
    h1=[x.get_text(" ",strip=True) for x in soup.find_all("h1")]
    h2=[x.get_text(" ",strip=True) for x in soup.find_all("h2")]
    imgs=soup.find_all("img")
    missing_alt=sum(1 for x in imgs if not x.get("alt","").strip())
    text=soup.get_text(" ",strip=True)
    words=re.findall(r"\b[\w'-]+\b",text)
    kw=req.keyword.lower().strip()
    occurrences=len(re.findall(re.escape(kw),text.lower())) if kw else 0
    density=(occurrences/len(words)*100) if words and kw else 0
    checks=[("Title tag",bool(title),title or "Missing"),("Meta description",bool(description),description or "Missing"),("Exactly one H1",len(h1)==1,f"Found {len(h1)}"),("H2 headings",bool(h2),f"Found {len(h2)}"),("Image alt text",missing_alt==0,f"{missing_alt} images missing alt text out of {len(imgs)}"),("Readable text",len(words)>=300,f"{len(words)} words")]
    lines=["ON-PAGE SEO AUDIT","",f"Page: {req.url or 'HTML input'}",f"Word count: {len(words)}",f"Target keyword occurrences: {occurrences}",f"Keyword density: {density:.2f}%" if kw else "Target keyword: not supplied",""]
    for label,ok,value in checks: lines.append(f"{'PASS' if ok else 'CHECK'} — {label}: {value}")
    if title and len(title)>60: lines.append("TIP — Title is over 60 characters; consider shortening it.")
    if description and len(description)>160: lines.append("TIP — Meta description is over 160 characters; consider shortening it.")
    return {"report":"\n".join(lines)}
