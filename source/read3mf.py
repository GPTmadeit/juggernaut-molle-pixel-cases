"""Minimal dependency-free 3MF reader (mesh objects + build transforms)."""
import zipfile, numpy as np, xml.etree.ElementTree as ET

def load_3mf(path):
    z = zipfile.ZipFile(path)
    name = next(n for n in z.namelist() if n.lower().endswith("3dmodel.model"))
    root = ET.fromstring(z.read(name))
    ns = {'m': root.tag.split('}')[0].strip('{')}
    objs = {}
    for obj in root.iter():
        if not obj.tag.endswith('}object'): continue
        oid = obj.get('id')
        mesh = None
        for ch in obj:
            if ch.tag.endswith('}mesh'): mesh = ch
        if mesh is None: continue
        V=[]; F=[]
        for ch in mesh:
            if ch.tag.endswith('}vertices'):
                V=[(float(v.get('x')),float(v.get('y')),float(v.get('z'))) for v in ch]
            elif ch.tag.endswith('}triangles'):
                F=[(int(t.get('v1')),int(t.get('v2')),int(t.get('v3'))) for t in ch]
        objs[oid]=(np.array(V,float), np.array(F,np.int64))
    items=[]
    for it in root.iter():
        if it.tag.endswith('}item'):
            oid=it.get('objectid'); tr=it.get('transform')
            M=np.eye(4)
            if tr:
                a=np.array([float(x) for x in tr.split()],float).reshape(4,3)
                M[:3,:3]=a[:3].T; M[:3,3]=a[3]
            items.append((oid,M))
    if not items: items=[(k,np.eye(4)) for k in objs]
    return objs, items
