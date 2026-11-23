"""Read-only Hatena Blog AtomPub check. Never prints secrets."""
import os,sys,base64,urllib.request,urllib.error,xml.etree.ElementTree as ET
def main():
  user=os.getenv("HATENA_ID","").strip()
  key=os.getenv("HATENA_API_KEY","").strip()
  blog=os.getenv("HATENA_BLOG_ID","dacotahouse.hatenablog.com").strip()
  if not user or not key:
    print("ERROR: HATENA_ID and HATENA_API_KEY GitHub secrets are required.")
    return 2
  url=f"https://blog.hatena.ne.jp/{user}/{blog}/atom/entry"
  auth=base64.b64encode(f"{user}:{key}".encode()).decode()
  request=urllib.request.Request(url,headers={"Authorization":"Basic "+auth,"Accept":"application/atom+xml","User-Agent":"tokimeki-oyatsu-connectivity-check/1.0"},method="GET")
  try:
    with urllib.request.urlopen(request,timeout=25) as r: body=r.read(2000000); status=r.status
  except urllib.error.HTTPError as e:
    print(f"ERROR: Hatena HTTP {e.code}; check credentials and blog ID.")
    return 1
  except Exception as e:
    print(f"ERROR: Connection failed ({type(e).__name__}).")
    return 1
  try:
    entries=ET.fromstring(body).findall("{http://www.w3.org/2005/Atom}entry")
  except ET.ParseError:
    print("ERROR: Hatena returned non-Atom XML.")
    return 1
  print(f"OK: authenticated read-only GET; HTTP {status}; {len(entries)} entries on first page")
  print("No content was created or changed.")
  return 0
if __name__=="__main__": sys.exit(main())
