import urllib.request, urllib.parse, urllib.error, ssl, json, time, sqlite3, random, time, requests, re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

#loop variable
x = 0
y = 0
z = 0

#url parameter
category_number = None
page = 1
rows = 100
start = 0
o_b_number = 23

#count item parameter
num = 0
count = 0
item_id = list()
item_recorded = set(item_id)

#ignore ssl certificate, just in case
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE

#sqlite
con = sqlite3.connect('Tokopedia.sqlite')
cur = con.cursor()

#user-agent
ua = UserAgent()
ua_list = [ua.ie, ua.msie, ua.opera, ua.chrome, ua.google, ua.firefox]

def resetloopvar():
    global x, y, z, start
    x = 0
    y = 0
    z = 0
    start = 0
    status = False

def url_to_json(url):
    opener = urllib.request.build_opener()
    if '/provi/' not in url:
        opener.addheaders = [('User-agent', ua.random)]
    if '/provi' in url:
        opener.addheaders = [
                            ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                            ('Accept-encoding', 'gzip, deflate, br'),
                            ('Accept-language', 'en-US,en;q=0.8'),
                            ('Cache-control', 'max-age=0'),
                            ('Upgrade-insecure-requests', '1'),
                            ('User-agent', random.choice(ua_list)),
                            ('Host', 'www.tokopedia.com'),
                            ('Cookie', '_ampUITN=98135ca86dbot27e2cdb743e7-30045-1510086117902; spUID=15100861188117d089ec93e.aa98a08c; discovery_onboarding={"new_filter":true}; _BID_TOKOPEDIA_=bf7925fbe7b694832c89b1fc6e25438d; ta_lpid=[200230020,216533950,95415322]; __utmx=169845028.BIViotTZQlii1ZIQnXimig$19726872-131:; __utmxx=169845028.BIViotTZQlii1ZIQnXimig$19726872-131:1510370102:15552000; _ampNV=1; _ga=GA1.2.1601698372.1510086116; _gid=GA1.2.1748590012.1510289817; appier_uid_1=a9597da1-82be-4a34-be03-55ee2a834390; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1510086117%7D; appier_uid_2=l3RVSNQI0egZoXodGQAFGC; _atrk_siteuid=bL9Fz3S8vGG6NFhA; insdrSV=97; scs=%7B%22t%22%3A1%7D; current-currency=IDR; _SID_Tokopedia_=Ksv5HrVHvQxL0fb2EnISu45ikaIeHt1l1mBta0SN36tYOQspGaVTgz3p125n9CuphpU7-B56c6KP3bdeblgXY5Wh7bhU5CIl-vczjrb2P3khmEqyqGiUX_EwNTHQSDoU; _ID_autocomplete_=89b29d4ed4784dc0ae940ff188100a0d; __asc=9164688915fab9dc78490a6067c; __auc=904b5ff715f98257ee505a0bbcc'),]
    urlhandle = opener.open(url)
    material = urlhandle.read().decode()
    try:
        data = json.loads(material)
    except:
        pos1 = material.find('(')
        pos2 = material.rfind(')')
        data = json.loads(material[pos1+1:pos2])
    return data

def getdepartmentname(product_url):
    urlhandle = urllib.request.urlopen(product_url)
    material = urlhandle.read().decode()
    soup = BeautifulSoup(material, 'html.parser')
    data = soup.findAll('script')
    try:
        target = re.findall('\W{"name":"([^"]+)","id":"[0-9]+"}],', str(data))
        department_name = target[0]
    except:
        try:
            target = re.findall('\W{"id":"[0-9]+","name":"([^"]+)"}],', str(data))
            department_name = target[0]
        except:
            print('Unable to retrieve Department Name')
            target = None
    return department_name

cur.execute('''
CREATE TABLE IF NOT EXISTS Search
(search_id INTEGER PRIMARY KEY, keyword TEXT, from_dept_id INTEGER, orderby_id INTEGER, time_stamp TEXT, retrieved INTEGER)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Product
(id INTEGER PRIMARY KEY, to_dept_id INTEGER, name TEXT, condition INTEGER, price INTEGER, disc_percentage REAL,
view_count INTEGER, review_count INTEGER, sold_count INTEGER, success_count INTEGER, reject_count INTEGER, rating INTEGER,
label_id INTEGER, badge_id INTEGER, wholesale TEXT, url TEXT, store_id INTEGER, search_id INTEGER)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Department
(dept_id INTEGER PRIMARY KEY, dept_name TEXT UNIQUE)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS ProductLabel
(label_id INTEGER PRIMARY KEY, label_name TEXT UNIQUE)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS ProductBadge
(badge_id INTEGER PRIMARY KEY, badge_name TEXT UNIQUE)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Store
(store_id INTEGER PRIMARY KEY, store_name TEXT UNIQUE, location_id INTEGER, gold_is_true TEXT, store_url TEXT)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Location
(location_id INTEGER PRIMARY KEY, location_name TEXT UNIQUE)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Link
( from_dept_id INTEGER, to_dept_id INTEGER, UNIQUE(from_dept_id, to_dept_id) ON CONFLICT REPLACE)''')

while z < 1:
    search = input('Search, or quit: ')
    if search.lower() == 'quit':
        quit()
    search_url = ("https://ace.tokopedia.com/universe/"+
                    "v4?callback=callback&q={}&unique_id=ed524b33735546dc9c25494bd28b325f"+
                    "&universe_id=6c817883d50c12fb914f898265134dc2&source=search&device=desktop"+
                    "&user_id=0&_=1510076543580").format(search.replace(' ','+'))
    recommend_data = url_to_json(search_url)
    category = dict({'Semua Kategori': 0})
    for tag in recommend_data['data'][2]['items']:
        sc = tag['sc']
        recom = tag['recom']
        category[recom] = sc
    print(' ')
    for (k, v) in category.items():
        print(("{}: {}".format(k, v)))
    print(' ')
    z = z + 1

    while y < 1:
        category_input = input('Insert category number (e.g. 0 for "Semua Kategori"): ')
        try:
            category_number = int(category_input)
            if category_number in category.values():
                y = y + 1
            if category_number not in category.values():
                print('Please select a valid category number')
                print(' ')
                for (k, v) in category.items():
                    print(("{}: {}".format(k, v)))
                    y = 0
                continue
        except:
            print('Please enter a numeric number')
            print(' ')
            continue
    order_by = dict()
    o_b_url = ("https://ace.tokopedia.com/v2/dynamic_attributes?"+
                "st=product&q={}&source=search&device=desktop").format(search.replace(' ','+'))
    o_b_data = url_to_json(o_b_url)
    for tag in o_b_data['data']['sort']:
        name = tag['name']
        value = tag['value']
        order_by[name] = int(value)
    print(' ')
    for (k, v) in order_by.items():
        print(("{}: {}".format(k, v)))
    print(' ')

    while x < 1:
        o_b_input = input('Insert order by number (e.g. 23 for "Paling Sesuai"): ')
        try:
            o_b_number = int(o_b_input)
            if o_b_number in order_by.values():
                status = True
                x = x + 1
            if o_b_number not in order_by.values():
                print('Please select a valid order by number')
                print(' ')
                for (k, v) in order_by.items():
                    print(("{}: {}".format(k, v)))
                x = 0
                continue
        except:
            print('Please enter a numeric number')
            print(' ')
            continue

    cur.execute('''INSERT INTO Search (keyword, from_dept_id, orderby_id, time_stamp) VALUES (?,?,?, CURRENT_TIMESTAMP)''', (search, category_number, o_b_number))
    con.commit()
    cur.execute('''SELECT search_id, from_dept_id FROM Search WHERE retrieved is NULL ORDER BY search_id ASC LIMIT 1''')
    try:
        row_search = cur.fetchone()
        search_id = row_search[0]
        from_dept_id = row_search[1]
        cur.execute('''UPDATE Search SET retrieved = 1 WHERE search_id = ?''',(search_id,))
        con.commit()
    except:
        print('Unable to retrieve id')

    while status:
        if category_number == 0:
            url = ("https://ace.tokopedia.com/search/product/"+
            "v3?utm_expid=19726872-131.BIViotTZQlii1ZIQnXimig.0&st=product&q={}&source=search&device=desktop"+
            "&scheme=https&page={}&rows={}&catalog_rows=10&unique_id=ec524b33735546dc9c25494bd28b325f&start={}&ob={}"+
            "&full_domain=www.tokopedia.com").format(search.replace(' ','+'), page, rows, start, o_b_number)
        if category_number > 0 :
            url = ("https://ace.tokopedia.com/search/product/"+
            "v3?q={}&sc={}&default_sc={}&source=search&st=product&utm_expid=19726872-131.BIViotTZQlii1ZIQnXimig.0"+
            "&device=desktop&scheme=https&page={}&rows={}&catalog_rows=10&unique_id=89b29d4ed4784dc0ae940ff188100a0d&start={}&ob={}"+
            "&full_domain=www.tokopedia.com").format(search.replace(' ','+'),category_number,category_number, page, rows, start, o_b_number)

        data = url_to_json(url)
        #print(json.dumps(data, indent=4))
        if data['header']['total_data'] < 1:
            print('Done 134')
            resetloopvar()
            break
        if len(data['data']['products']) < 1:
            print('Done 139')
            resetloopvar()
            break
        if len(item_id) == data['header']['total_data']:
            print('Done 199')
            resetloopvar()
            break
        target = data['data']['products']
        for tag in target:
            id = tag['id']
            if id not in item_recorded:
                item_recorded.add(id)
                item_id.append(id)
            name = tag['name']
            url = tag['url']
            price = tag['price'].replace('Rp ','').replace('.','')
            shop_id = tag['shop']['id']
            shop_name = tag['shop']['name']
            shop_url = tag['shop']['url']
            shop_gold = tag['shop']['is_gold']
            shop_location = tag['shop']['location']
            condition = tag['condition']
            department_id = tag['department_id']
            rating = tag['rating']
            count_review = tag['count_review']
            org_price = tag['original_price'].replace('Rp ','').replace('.','')
            discount_percentage = tag['discount_percentage']
            wholesale_price = tag['wholesale_price']
            if len(wholesale_price) < 1:
                wholesale = '-'
            if len(wholesale_price) > 0:
                wholesale = 'Y'
            label_l = list()
            if len(tag['labels']) == 0:
                label_l.append('-')
            elif len(tag['labels']) > 0:
                if len(tag['labels']) == 1:
                    label_l.append(tag['labels'][0]['title'])
                elif len(tag['labels']) > 1:
                    for tag in tag['labels']:
                        label_l.append(tag['title'])
            label = ', '.join(label_l)

            badge_l = list()
            if 'badges' not in tag:
                badge_l.append('-')
            elif 'badges' in tag:
                if len(tag['badges']) == 0:
                    label_l.append('-')
                elif len(tag['badges']) > 0:
                    if len(tag['badges']) == 1:
                        badge_l.append(tag['badges'][0]['title'])
                    elif len(tag['badges']) > 1:
                        for tag in tag['badges']:
                            badge_l.append(tag['title'])
            badge = ', '.join(badge_l)

            try:
                view_count_url = ("https://www.tokopedia.com/provi/check?pid={}&callback=show_product_view").format(id)
                view_count_data = url_to_json(view_count_url)
                view_count = view_count_data['view']
                time.sleep(random.uniform(0.5,1.25))
            except:
                view_count = 'error'

            try:
                sold_count_url = ("https://js.tokopedia.com/productstats/check?pid={}&callback=show_product_stats").format(id)
                sold_count_data = url_to_json(sold_count_url)
                item_sold = sold_count_data['item_sold']
                success = sold_count_data['success']
                reject = sold_count_data['reject']
            except:
                item_sold = 'error'
                success = 'error'
                reject = 'error'

            department_name = getdepartmentname(url)

            cur.execute('''INSERT OR IGNORE INTO Location (location_name) VALUES (?)''',(shop_location,))
            con.commit()
            cur.execute('''SELECT location_id FROM Location WHERE location_name = ? LIMIT 1''',(shop_location,))
            row_loc = cur.fetchone()
            location_id = row_loc[0]

            cur.execute('''INSERT OR IGNORE INTO ProductBadge (badge_name) VALUES (?)''',(badge,))
            con.commit()
            cur.execute('''SELECT badge_id FROM ProductBadge WHERE badge_name = ? LIMIT 1''',(badge,))
            row_badge = cur.fetchone()
            badge_id = row_badge[0]

            cur.execute('''INSERT OR IGNORE INTO ProductLabel (label_name) VALUES (?)''',(label,))
            con.commit()
            cur.execute('''SELECT label_id FROM ProductLabel WHERE label_name = ? LIMIT 1''',(label,))
            row_label = cur.fetchone()
            label_id = row_label[0]

            cur.execute('''INSERT OR IGNORE INTO Link (from_dept_id, to_dept_id) VALUES (?,?)''', (from_dept_id, department_id))
            cur.execute('''INSERT OR IGNORE INTO Store (store_id, store_name, location_id, gold_is_true, store_url) VALUES (?,?,?,?,?)''',
                        (shop_id, shop_name, location_id, shop_gold,shop_url))
            cur.execute('''INSERT OR IGNORE INTO Product(id, to_dept_id, name, condition, price, disc_percentage,
                        view_count, review_count, sold_count, success_count, reject_count, rating,
                        label_id, badge_id, wholesale, url, store_id, search_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (id, department_id, name, condition, price, discount_percentage,
                        view_count, count_review, item_sold, success, reject, rating,
                        label_id, badge_id, wholesale, url, shop_id, search_id))
            cur.execute('''INSERT OR IGNORE INTO Department (dept_id, dept_name) VALUES (?, ?)''',(department_id,department_name))
            con.commit()

            print(' ')
            count = count + 1
            num = num + 1
            print('No. of item retrieved:',len(item_id),
                '| No. of item parsed:', num,
                '| Page start:', start,
                '| Product id:', id,
                '| Product dept. id:', department_id,
                '| Product dept. name:', department_name,
                '| Product name:', name,
                '| Product condition:', condition,
                '| Product price:', price,
                '| Product discount:', discount_percentage,
                '| Product view:', view_count,
                '| Product no. of review:', count_review,
                '| Product no. of sold:', item_sold,
                '| Product no. of sucess:', success,
                '| Product no. of reject:', reject,
                '| Product rating:', rating,
                '| Product label:', label,
                '| Product badge:', badge,
                '| Wholesale:', wholesale,
                '| Product url:', url,
                '| Shop id:', shop_id,
                '| Shop name:', shop_name,
                '| Shop location:', shop_location,
                '| Shop gold:', shop_gold,
                '| Shop url:', shop_url)

            if count % rows == 0:
                count = 0
                start = start + rows
                print(' ')
                print('wait . . .')
                time.sleep(random.uniform(0.25,0.50))

cur.close()
