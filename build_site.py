from pathlib import Path
import json,html
R=Path(__file__).resolve().parent;P={p['key']:p for p in json.loads((R/'catalog.json').read_text())}
BASE='https://dacotahouse.github.io/tokimeki-sweets/'
COLLECTIONS=[
('haeru','映えるスイーツ','見た目に恋する、10のお菓子。','色、形、断面。思わず写真に残したくなる、お菓子の表情を集めました。','planet',['kuririn','mochi','morin','planet','petit-tart','cassata','mini-tart','fruit-tart','fukiyose','waffle']),
('cute','キュートなお菓子','かわいい、を贈る。','動物の表情や小さな形に、ふっと笑顔になるお菓子を選びました。','animal-marshmallow',['animal-marshmallow','animal-manju','caffarel','flower-pop','parfait-bar','monaka','panda-winter','yoku-christmas','royce-winter','toraya-eto']),
('gift','ギフトスイーツ','手土産やお祝いに、贈りたい10品。','ちょっとしたお礼には手渡ししやすい箱菓子を。お祝いには、開ける楽しみのある一箱を。贈る相手と場面に合わせて選べるお菓子を集めました。','frantz-tsubo',['frantz-tsubo','west-dry-cakes','kurumicco','shiseido-gana','miel-caramel','kihachi-assort-m','press-amaou','tsujiri-sato','butter-galette','fugetsudo-gaufres']),
('wagashi','和菓子・和スイーツ','日本茶と、甘いひと息。','季節の上生菓子から、どら焼きやわらび餅まで。おうちのお茶時間に楽しみたい和菓子を集めました。','shiki-junisen',['shiki-junisen','kyomizuha-warabi','ninigi-pocchiri','kanou-amo','bunmeido-mikasayama','obusedo-kanoko','josuian-tsukushi','eitaro-anmitsu','itojyu-umoregi','saiundo-wakakusa']),
('chocolate', 'チョコレート菓子', '苺の断面、紅茶の香り、ひと粒の口どけ。', '甘じょっぱいチップスから、切り分けて楽しむテリーヌまで。気分に合うチョコのおやつを探してみてください。', 'frantz-strawberry', ['frantz-strawberry', 'vanilla-showcolat', 'letao-montagne', 'antoine-orangette', 'demel-cat-milk', 'coquillage-terrine', 'shiseido-ganache', 'royal-pecan', 'royce-potato', 'lindt-tasting-16']),
('season','季節を楽しむスイーツ','秋から冬へ、お菓子も衣替え。','いまの限定パッケージと、秋冬のお茶時間に選びたい定番のお菓子を集めました。','panda-winter',['royce-winter','yoku-christmas','panda-winter','henri-collection','toraya-eto','kuri-matcha-daifuku','kuririn','kurikinton','caffarel','lindt']),
('price','価格別スイーツ','予算に合う、ときめきを。','小さなお礼から、きちんとした贈り物まで。確認時の商品価格を目安に探せます。','monaka',['monaka','royce-winter','animal-marshmallow','panda-winter','kurikinton','kuri-matcha-daifuku','yoku-christmas','caffarel','henri-collection','toraya-eto'])]
# Add an existing collection slug here when its page is ready to be featured.
PUBLISHED = ("haeru", "cute", "gift", "wagashi", "chocolate")
CATS = [c for c in COLLECTIONS if c[0] in PUBLISHED]
PRODUCT_COLLECTION = {key: c[0] for c in CATS for key in c[5]}
assert len(CATS) == len(PUBLISHED) and all(len(c[5]) == 10 for c in CATS)
assert len(PRODUCT_COLLECTION) == sum(len(c[5]) for c in CATS), "Products must be unique across published collections"
E=lambda x:html.escape(str(x),quote=True)
def img(k,cls='',lazy=True):
 p=P[k];return f'<img class="{cls}" src="{E(p["image"])}" alt="{E(p["brand"]+" "+p["name"])}" width="480" height="480" loading="{"lazy" if lazy else "eager"}">'
def nav(active=''):
 links=''.join(f'<a {"aria-current=page" if active==c[0] else ""} href="{c[0]}.html">{c[1]}</a>' for c in CATS)
 return '<a class="skip" href="#main">本文へ移動</a><header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><span aria-hidden="true">♡</span> ときめきスイーツ図鑑<small>SWEETS & LITTLE HAPPINESS</small></a><a class="header-link" href="index.html#categories">お菓子を探す <span>↗</span></a></div><nav class="category-nav" aria-label="カテゴリー">'+links+'</nav></header>'
def foot():
 return '<footer class="site-footer"><div class="footer-inner"><a class="brand" href="index.html">♡ ときめきスイーツ図鑑</a><p>見てときめいて、選んでうれしい。<br>お取り寄せのお菓子を、好きな切り口から。</p><div class="footer-links"><a href="about.html">このサイトについて・掲載方針</a><a href="privacy.html">広告・プライバシーについて</a><a href="index.html#categories">カテゴリー一覧</a></div><p class="fine">当サイトはアフィリエイト広告を掲載しています。広告リンクを経由した購入により、運営者が報酬を受け取る場合があります。<br>商品仕様・価格・在庫・送料・配送地域は販売ページの最新情報をご確認ください。</p><p class="fine">© ときめきスイーツ図鑑</p></div></footer>'
def shell(title,desc,body,file,active='',schema=None,og_image='haeru-main.webp'):
 structured='' if schema is None else '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>'+E(title)+'｜ときめきスイーツ図鑑</title><meta name="description" content="'+E(desc)+'"><link rel="canonical" href="'+BASE+file+'"><meta property="og:type" content="website"><meta property="og:title" content="'+E(title)+'｜ときめきスイーツ図鑑"><meta property="og:description" content="'+E(desc)+'"><meta property="og:url" content="'+BASE+file+'"><meta property="og:image" content="'+BASE+og_image+'"><link rel="stylesheet" href="style.css"><script src="site.js" defer></script>'+structured+'</head><body>'+nav(active)+'<main id="main">'+body+'</main>'+foot()+'</body></html>'
def adnote():
    return '<p class="ad-note"><strong>広告を含みます</strong> 商品画像・購入リンクには、アフィリエイト広告を使用しています。</p>'

def purchase(product):
    name = E(product["name"])
    ads = ""
    if rakuten_code := product.get("code"):
        ads = '<p class="ad-label">広告・楽天市場</p>' + rakuten_code
    if yahoo_code := product.get("yahoo_code"):
        ads += '<div class="additional-purchase"><p class="ad-label">広告・Yahoo!ショッピング</p>' + yahoo_code + '</div>'
    return f'<div class="purchase" aria-label="{name}の購入先（広告）">{ads}</div>'

def card(k,n=0,context='',compact=False):
 p=P[k];data=f' data-price="{p["price"] or 0}"';badge=('期間・季節の販売商品' if p['seasonal'] else '秋冬に選びたい定番') if context=='season' else p['tag']
 price=f'<p class="price-guide">確認時の商品価格 <strong>{p["price"]:,}円</strong><small>税込・送料別途の場合あり／2026年11月16日確認</small></p>' if context=='price' else ''
 return f'<article class="product" id="product-{k}"{data}><div class="product-heading"><div class="product-kicker"><span>{n:02d}</span><span>{E(badge)}</span></div><p class="product-brand">{E(p["brand"])}</p><h2>{E(p["name"])}</h2><p class="product-catch">{E(p["catch"])}</p></div>{purchase(p)}<div class="product-editorial">{price}<p>{E(p["description"])}</p><p class="product-note">{E(p["note"])}</p></div><a class="back-index" href="{chr(35)+("page-index" if context else "categories")}">一覧に戻る ↑</a></article>'
# Optional artwork for category cards.
CATEGORY_BANNERS = {
    "haeru": ("category-haeru.webp", 1448, 1086),
    "cute": ("category-cute.webp", 1448, 1086),
    "gift": ("category-gift.webp", 1448, 1086),
    "wagashi": ("category-wagashi.webp", 1536, 1024),
    "chocolate": ("category-chocolate.webp", 1672, 941),
}


def category_card(collection):
    slug, name, headline, _, cover, _ = collection
    banner = CATEGORY_BANNERS.get(slug)
    if banner:
        path, width, height = banner
        photo = (
            f'<div class="category-photo category-banner"><img src="{E(path)}" alt="" '
            f'width="{width}" height="{height}" loading="lazy"></div>'
        )
    else:
        photo = f'<div class="category-photo">{img(cover)}</div>'
    return (
        f'<a class="category-card category-{slug}" href="{slug}.html">'
        f'{photo}<div class="category-copy"><h3>{name} <span>↗</span></h3>'
        f'<p>{headline}</p><span class="count">10のお菓子</span></div></a>'
    )


def categories(active=None):
    cards = [category_card(c) for c in CATS if c[0] != active]
    return '<div class="category-grid">' + ''.join(cards) + '</div>'

for slug,name,headline,intro,_,keys in CATS:
 body=f'<div class="breadcrumb"><a href="index.html">ホーム</a><span>／</span>{name}</div><section class="collection-hero collection-hero-text"><div><p class="eyebrow">SWEETS COLLECTION</p><h1>{name}</h1><p class="collection-heading">{headline}</p><p>{intro}</p><a class="text-link" href="#page-index">10の商品を見る ↓</a></div></section>'+adnote()
 if slug == 'chocolate':
  hero = '<figure class="chocolate-hero"><img src="category-chocolate.webp" width="1672" height="941" alt="白い苺チョコの断面とチョコサンド、オレンジピールのチョコがけ" fetchpriority="high"><figcaption class="image-note">チョコレート菓子のイメージです。</figcaption></figure>'
  body = body.replace('</section>', '</section>' + hero, 1)
 if slug=='season':body+='<aside class="editorial-note"><strong>2026年 秋冬のセレクション</strong><p>前半6品は、販売ページに季節限定・期間限定・クリスマス仕様・干支パッケージの案内がある商品です。後半4品は、秋冬のお茶時間に選びたい定番品。限定品は販売終了・売り切れになる場合があります。</p></aside>'
 if slug=='price':body+='<aside class="editorial-note"><strong>価格は、比較のための目安です。</strong><p>2026年11月16日に、もしもアフィリエイトの商品検索で表示された税込商品価格です。送料を含む総額や、選択するセットによって金額が変わる場合があります。購入前に販売ページでご確認ください。</p></aside><div class="budget-filters" aria-label="予算で絞り込む"><button type="button" data-budget="all" aria-pressed="true">すべて</button><button type="button" data-budget="1000">1,000円以下</button><button type="button" data-budget="2000">2,000円以下</button><button type="button" data-budget="3000">3,000円以下</button><button type="button" data-budget="over">3,001円以上</button></div><p id="budget-status" class="result-status" aria-live="polite"></p>'
 body+='<nav id="page-index" class="page-index" aria-label="このページの商品"><h2>気になるお菓子から</h2><ol>'+''.join(f'<li><a href="#product-{k}"><span>{i+1:02d}</span>{E(P[k]["name"])}</a></li>' for i,k in enumerate(keys))+'</ol></nav><div class="product-grid">'+''.join(card(k,i+1,slug) for i,k in enumerate(keys))+'</div><section class="more-section"><h2>ほかのカテゴリー</h2>'+categories(slug)+'</section>'
 schema={'@context':'https://schema.org','@type':'CollectionPage','name':name,'url':BASE+slug+'.html','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':P[k]['brand']+' '+P[k]['name'],'url':BASE+slug+'.html#product-'+k} for i,k in enumerate(keys)]}}
 (R/(slug+'.html')).write_text(shell(name+'10選',intro,body,slug+'.html',slug,schema,og_image='category-chocolate.webp' if slug == 'chocolate' else 'haeru-main.webp'))
# Home
def search_result(key, slug):
    product = P[key]
    search = E(" ".join(product[field] for field in ("brand", "name", "tag", "description")))
    photo = img(key) if product.get("image") else ""
    return (
        f'<a class="search-result" data-search="{search}" href="{slug}.html#product-{key}">'
        f'{photo}<span><small>{E(product["brand"])}</small><strong>{E(product["name"])}</strong></span>'
        '<span aria-hidden="true">↗</span></a>'
    )


body = '''<section class="home-hero simple-hero" aria-labelledby="home-title">
  <img class="home-hero-image" src="haeru-main.webp" alt="桜の花と、タルトや華やかなお菓子を並べたイメージ" width="1752" height="897" fetchpriority="high">
  <div class="home-hero-copy">
    <h1 id="home-title">ときめきスイーツ図鑑</h1>
    <p>自分へのご褒美にも、大切な人への贈り物にも。<br>写真を眺めながら、お取り寄せスイーツを選べます。</p>
    <a class="primary-link" href="#categories">お菓子を選ぶ <span aria-hidden="true">↓</span></a>
  </div>
</section>
<p class="image-note">メイン画像はイメージです。</p>
<section class="tea-feature" aria-labelledby="tea-feature-title">
  <figure class="tea-feature-visual">
    <img src="feature-anko.webp" alt="どら焼きと花の形の練り切りを、温かいお茶と並べたイメージ" width="1280" height="853" loading="lazy">
    <figcaption>写真はイメージです。</figcaption>
  </figure>
  <div class="tea-feature-copy">
    <p class="tea-feature-label">今日のおやつ、どんな気分？</p>
    <h2 id="tea-feature-title">温かいお茶と、<br>あんこのおやつ</h2>
    <p>肌寒い日は、ほうじ茶を淹れて、あんこのおやつをひとつ。香ばしいお茶には、ふんわりしたどら焼きを。緑茶を淹れるなら、花の形をした練り切りを小皿にのせて。お茶からおやつを選んでみるのも、楽しいものです。</p>
    <a href="wagashi.html">和菓子・和スイーツを眺める <span aria-hidden="true">→</span></a>
  </div>
</section>
<section id="categories" class="home-section simple-collections">
  <div class="section-head"><h2>カテゴリーから選ぶ</h2></div>''' + categories() + '''
  <p class="image-note">カテゴリー画像はイメージです。</p>
</section>
<figure class="tea-message">
  <img src="tea-message.jpg" width="1204" height="370" loading="lazy"
       alt="スイーツには、毎日をちょっと幸せにしてくれる魔法があります。この図鑑が、あなたのお気に入りのスイーツを見つけるきっかけになれば嬉しいです。今日も、素敵なスイーツとの出会いがありますように。">
</figure>
<details class="home-section simple-search">
  <summary>商品名や素材で探す</summary>
  <label class="search-label" for="sweet-search">商品名・ブランド名・素材</label>
  <div class="search-input-wrap"><input id="sweet-search" type="search" placeholder="例：栗、パンダ" autocomplete="off"></div>
  <p id="search-status" class="result-status" aria-live="polite"></p>
  <div class="search-results" hidden>''' + ''.join(search_result(key, slug) for key, slug in PRODUCT_COLLECTION.items()) + '''</div>
</details>''' + adnote()
(R/'index.html').write_text(shell('見てときめく、お取り寄せスイーツ','映えるスイーツ、キュートなお菓子、ギフトスイーツ、和菓子・和スイーツ、チョコレート菓子を各10品、計50品紹介。お取り寄せスイーツを写真で見比べて選べます。',body,'index.html'))
about='''<article class="text-page"><p class="eyebrow">ABOUT THIS GUIDE</p><h1>このサイトについて</h1><p class="text-lead">「すき」から始まる、お菓子選び。</p><p>ときめきスイーツ図鑑は、見た目の魅力や選ぶ楽しさを大切に、お取り寄せのお菓子を紹介するサイトです。自分へのご褒美にも、大切な人への贈り物にも。用途に合う一品を見つけるきっかけを目指しています。</p><h2>商品の選び方</h2><ul><li>形・色・断面・パッケージなどに、それぞれの魅力があること。</li><li>楽天市場・Amazon・Yahoo!ショッピングのいずれかで通常購入の商品として取り扱いがあること。</li><li>もしもアフィリエイトで広告リンクの取得を確認できること。現在掲載している50品には、確認できた楽天市場・Yahoo!ショッピングの広告リンクを掲載しています。</li><li>ふるさと納税の返礼品や、お菓子ではない雑貨・ミニチュアを混ぜないこと。</li></ul><h2>紹介文と写真について</h2><p>紹介文は、販売ページなどの公開情報をもとに、AIによる制作支援を利用して作成しています。すべての商品を実食した体験談ではありません。食べたと誤解させる表現や、根拠のない評価・ランキングは使いません。</p><p>商品写真は、アフィリエイト広告から提供される画像がある場合に表示しています。商品画像の内容や色の加工は行っていません。トップページのメイン画像とカテゴリー画像には、イメージ画像を使っています。</p><h2>カテゴリーと掲載数</h2><p>映えるスイーツ、キュートなお菓子、ギフトスイーツ、和菓子・和スイーツ、チョコレート菓子を各10品、計50品紹介しています。掲載する商品はカテゴリーごとに異なります。</p><h2>販売情報の更新</h2><p>掲載情報の確認日：映えるスイーツ・キュートなお菓子は2026年11月16日、ギフトスイーツ・和菓子と和スイーツ・チョコレート菓子は2026年11月17日。価格・在庫・送料・内容量・パッケージ・配送条件は変更になる場合があります。とくに期間限定品は、注文前に販売ページで最新情報をご確認ください。</p><h2>購入・配送に関するお問い合わせ</h2><p>当サイトは商品を販売する店舗ではありません。ご注文・配送・返品・商品仕様については、リンク先の販売店へお問い合わせください。</p><a class="primary-link" href="index.html#categories">お菓子を探す ↗</a></article>'''
(R/'about.html').write_text(shell('このサイトについて・掲載方針','ときめきスイーツ図鑑の商品選定、写真・紹介文、広告と掲載情報について。',about,'about.html'))
privacy='''<article class="text-page"><p class="eyebrow">ADS & PRIVACY</p><h1>広告・プライバシーについて</h1><h2>アフィリエイト広告</h2><p>当サイトは、もしもアフィリエイトを利用した楽天市場とYahoo!ショッピングの広告リンクを掲載しています。リンクを経由した購入により、サイト運営者が報酬を受け取る場合があります。広告は商品画像や購入ボタンの近くで明示しています。</p><h2>外部サイトへの移動</h2><p>各販売先への広告リンクを押すと、外部の販売ページへ移動します。商品代金・送料・購入条件は、外部サイトの注文画面でご確認ください。</p><h2>外部画像・広告スクリプト</h2><p>商品画像や広告カードの表示には、広告配信元などの外部サービスへの通信が発生します。その際、IPアドレスやブラウザ情報などが外部サービスへ送信される場合があります。広告配信・成果計測にはCookie等が使用される場合があります。</p><h2>サイト内検索</h2><p>当サイトの商品検索は、ブラウザ内で動作します。検索欄に入力した内容を、当サイト独自のサーバーへ送信・保存する機能は設けていません。</p><h2>アクセス解析・入力フォーム</h2><p>この版には、当サイト独自のアクセス解析タグ、会員登録、問い合わせ入力フォームは設置していません。サイトのホスティングや広告配信サービスによる情報の取り扱いについては、各サービスの方針をご確認ください。</p><p>最終更新：2026年11月17日</p><a class="text-link" href="about.html">掲載方針を見る ↗</a></article>'''
(R/'privacy.html').write_text(shell('広告・プライバシーについて','アフィリエイト広告、外部サイト、商品画像の表示、サイト内検索での情報の取り扱い。',privacy,'privacy.html'))
urls=['index.html']+[c[0]+'.html' for c in CATS]+['about.html','privacy.html']
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE+f}</loc><lastmod>2026-11-17</lastmod></url>' for f in urls)+'</urlset>')
(R/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
# Keep bookmarks to retired collections usable without advertising the old pages.
for slug, *_ in COLLECTIONS:
    if slug not in PUBLISHED:
        (R / f"{slug}.html").write_text(
            '<!doctype html><html lang="ja"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>カテゴリー一覧｜ときめきスイーツ図鑑</title>'
            '<meta name="robots" content="noindex,follow">'
            f'<link rel="canonical" href="{BASE}">'
            '<meta http-equiv="refresh" content="0; url=index.html#categories">'
            '</head><body><p><a href="index.html#categories">カテゴリー一覧に戻る</a></p></body></html>'
        )

print(f"Built home, {len(CATS)} category pages, two policy pages and sitemap")
