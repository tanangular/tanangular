import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
G="/usr/share/fonts/truetype/sand-box/google/"
FONTS={
 "serif_i":G+"Instrument Serif/InstrumentSerif-Italic.ttf",
 "serif":G+"Instrument Serif/InstrumentSerif-Regular.ttf",
 "grotesk":G+"Space Grotesk/SpaceGrotesk-VariableFont_wght.ttf",
 "mono":G+"Geist Mono/GeistMono-VariableFont_wght.ttf",
 "thai":G+"Bai Jamjuree/BaiJamjuree-Medium.ttf",
 "thai_l":G+"Bai Jamjuree/BaiJamjuree-Regular.ttf",
}
_cache={}
def _load(key,wght):
    k=(key,wght)
    if k in _cache: return _cache[k]
    p=FONTS[key]; ft=TTFont(p)
    var='fvar' in ft
    loc={'wght':wght} if (var and wght) else None
    gs=ft.getGlyphSet(location=loc) if loc else ft.getGlyphSet()
    face=hb.Face(hb.Blob.from_file_path(p)); f=hb.Font(face)
    if loc: f.set_variations(loc)
    _cache[k]=(ft,gs,face,f); return _cache[k]

def glyphs(text,key,size,x=0,y=0,wght=None,ls=0.0,anchor="start"):
    """return (list of (d, cluster_index)), width). ls = letter spacing in px"""
    ft,gs,face,f=_load(key,wght)
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(f,buf,{"kern":True,"liga":True})
    sc=size/face.upem; order=ft.getGlyphOrder()
    width=sum(p.x_advance for p in buf.glyph_positions)*sc+ls*len(text)
    if anchor=="middle": x-=width/2
    elif anchor=="end": x-=width
    out=[]; cx=x
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        name=order[info.codepoint]
        pen=SVGPathPen(gs,ntos=lambda v:("%.1f"%v).rstrip('0').rstrip('.'))
        tp=TransformPen(pen,(sc,0,0,-sc,cx+pos.x_offset*sc,y-pos.y_offset*sc))
        gs[name].draw(tp)
        d=pen.getCommands()
        if d: out.append((d,info.cluster))
        cx+=pos.x_advance*sc+ls
    return out,width

def path(text,key,size,x=0,y=0,**kw):
    g,w=glyphs(text,key,size,x,y,**kw)
    return " ".join(d for d,_ in g),w
