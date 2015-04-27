from helpers import fake_response_from_file

from letmescrape.spiders.disney_product import DisneyProductSpider

import pytest

url = 'http://www.test.com'
site_category_id = 1
job_id = 2


@pytest.fixture
def spider():
    return DisneyProductSpider(start_url=url, site_category_id=site_category_id, job_id=job_id)


def test_convert_to_ajax_url(spider):
    list_url = 'http://www.disneystore.com/mn/1001152/'
    ajax_url = spider.get_ajax_url_for_list(list_url)
    assert ajax_url == 'http://www.disneystore.com/disney/store/DSIProcessWidget?' \
                       'storeId=10051&templateId=Width-3_4-ProductList&' \
                       'N=1001152&navNum=10000&Nao=0'


def test_list(spider):
    file_name = 'samples/disney_list.json'
    response = fake_response_from_file(file_name)
    result = list(spider.parse_list(response))
    request = result[0]

    assert len(result) == 472
    assert 'values_from_list' in request.meta


def test_product_not_in_sale(spider):
    list_image = 'http://www.test.com/image.jpg'
    product_number = '1234'
    meta = {
        'values_from_list': {
            'url': url,
            'list_images': list_image,
            'product_number': product_number
        }
    }

    file_name = 'samples/disney_product_not_in_sale.html'
    response = fake_response_from_file(file_name, url, meta)
    result = list(spider.parse_item(response))
    product = result[0]

    assert len(result) == 1
    assert 'original_price' not in product
    assert 'sale_price' in product

    assert product == {
        'url': url,
        'list_images': [list_image],
        'product_number': product_number,
        'site_category_id': site_category_id,
        'job_id': job_id,
        'brand': 'disney',
        'description': u"## Dream quest\n\nShe'll drift to dreamy adventures every night wearing Elsa's soft satin gown\nwith sheer, shimmering organza sleeves, decolletage, and glittering overlay\nskirt, plus embroidered cameo detailing.\xa0See more\n\n\n### Magic in the details...\n\n  * Elsa screen art appliqu\xe9\n  * Embroidered detailing and faceted gem\n  * Satin bodice and skirt\n  * Ruffled satin collar\n  * Sheer organza sleeves, decolletage, and overlay skirt with silver glitter snowflake accents\n  * Keyhole back with button\n\n### The bare necessities\n\n  * Polyester\n  * Imported\n\n",
        'images': [{'normal_size': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610?$yetidetail$',
                    'thumbnail': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610?$yetiProductThumb$',
                    'zoomed': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610?$yetizoom$'},
                   {
                   'normal_size': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-1?$yetidetail$',
                   'thumbnail': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-1?$yetiProductThumb$',
                   'zoomed': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-1?$yetizoom$'},
                   {
                   'normal_size': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-2?$yetidetail$',
                   'thumbnail': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-2?$yetiProductThumb$',
                   'zoomed': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-2?$yetizoom$'},
                   {
                   'normal_size': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-3?$yetidetail$',
                   'thumbnail': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-3?$yetiProductThumb$',
                   'zoomed': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251610-3?$yetizoom$'}],
        'reviews': [{'author': u'lovedisney1194 ',
                     'body': u'These nightgowns are wonderful. Been buying for years wish they made more.',
                     'date': '2015-04-02',
                     'max_stars': 5,
                     'stars': 5,
                     'title': u'Love it'},
                    {'author': u'Jenjen7824 ',
                     'body': u"Such a pretty night gown! My 2.5 year old daughter loved it, but like many other reviews on here, the sleeves ripped after only a couple of wears. We ended up having to cut the sleeves off because they ripped from the wrist up to the shoulder and made it uncomfortable and odd looking. Although it looks great sleeveless, I wish more care were put into the sleeves so they didn't rip so easily. I would NOT purchase this again.",
                     'date': '2015-03-28',
                     'max_stars': 5,
                     'stars': 1,
                     'title': u'Beautiful but ripped sleeves'},
                    {'author': u'KimcW ',
                     'body': u'We bought this nightgown for our 5 year old daughter. Initially, we loved it. However after only two weeks the sleeves began to rip and it has tears where the sleeves meet the satin gown. We are very disappointed in this product.',
                     'date': '2015-03-21',
                     'max_stars': 5,
                     'stars': 1,
                     'title': u'organza sleeves rip easily'},
                    {'author': u'AwesomeAuntieandMommy ',
                     'body': u'Bought this for my niece for Christmas and she LOVES it!! I think since the sleeves are so soft she finds it very comfortable. The cape is an awesome plus, I don\'t know much about frozen but this was definitely a hit! She got plenty of dresses (big poofy ones too) and this one is her "go to" princess dress. Her 3rd birthday is in March, so I got her a 3T and it fits perfect, with room to grow.',
                     'date': '2015-02-13',
                     'max_stars': 5,
                     'stars': 5,
                     'title': u'Niece loves it!'},
                    {'author': u'AuroraON ',
                     'body': u'I was browsing the site and was shocked that the overall rating on this was not higher. I read the reviews about the fabric ripping and I was truly surprised. I bought this the second it came out - I think November - my daughter received it same day. We have washed and dried this nightgown dozens of times without so much as a snag. It is beautiful and well made.',
                     'date': '2015-02-12',
                     'max_stars': 5,
                     'stars': 5,
                     'title': u'When I saw this did not get 5 stars I felt compelled to review'},
                    {'author': u'NJmommy1 ',
                     'body': u'My daughter received this for Christmas and was thrilled. Normally I would not spend so much on pajamas, but she really wanted this one and we have always found Disney products to be such a high quality I bought it. She has only gotten to wear it 4 nights and the sleeves are falling apart. She is very upset and I am very disappointed.',
                     'date': '2015-02-03',
                     'max_stars': 5,
                     'stars': 1,
                     'title': u'poor quality'},
                    {'author': u'PrincessLovingMommy ',
                     'body': u'My daughter received this nightgown for Christmas. She was thrilled with how beautiful it was. The fabric on the dress, however, was very thin. I was careful to follow the washing instructions on the dress, as I do with all her princess dresses. This dress did not make it through the first wash without disintegrating. After just the first wash we had to cut the sleeves off. After that when I washed it I would not put it in the dryer even on low setting because I was afraid that was the problem. This nightgown can not get wet because that is what breaks down the fabric. Very upset. Not like most Disney Store products.',
                     'date': '2015-01-15',
                     'max_stars': 5,
                     'stars': 1,
                     'title': u'Poor quality'},
                    {'author': u'TaRea ',
                     'body': u"I purchased this for my daughter's birthday. She absolutely loved it! It is her favorite nightgown by far. The parents at the party and their daughters too had many questions on where to purchase this! Very pleased. Though it is more of a Cinderella blue, it truly does not matter. It is beautiful and reminds me of something Elsa the Character would wear. Well done Disney!",
                     'date': '2015-01-11',
                     'max_stars': 5,
                     'stars': 4,
                     'title': u'Beautiful Elsa nightgown'}],
        'sale_price': 32.95,
        'site_category_id': 1,
        'sizes': [u'2', u'3', u'4', u'5/6', u'7/8', u'9/10'],
        'title': u'Elsa Nightgown for Girls - Frozen',
    }


def test_product_in_sale(spider):
    list_image = 'http://www.test.com/image.jpg'
    product_number = '1234'
    meta = {
        'values_from_list': {
            'url': url,
            'list_images': list_image,
            'product_number': product_number
        }
    }

    file_name = 'samples/disney_product_in_sale.html'
    response = fake_response_from_file(file_name, url, meta)
    result = list(spider.parse_item(response))
    product = result[0]

    assert len(result) == 1
    assert 'original_price' in product
    assert 'sale_price' in product

    assert product == {
        'url': url,
        'list_images': [list_image],
        'product_number': product_number,
        'site_category_id': site_category_id,
        'job_id': job_id,
        'brand': 'disney',
        'description': u'## Sleeper hit\n\nThis regal sleepwear is a lesson in bedtime style. The purple majesty of our\nSofia Nightgown for Girls is accented with shimmering silver foil and soft\norganza overskirts for a fit that will send her to sleep in enchanting\ncomfort.\xa0See more\n\n\n### Magic in the details...\n\n  * Sofia screen art appliqu\xe9 with embroidered detailing\n  * Purple satin bodice with purple and silver ric rac accent, and keyhole opening at back\n  * Organza puffed cap sleeves with gathered edge and silver foil accents\n  * Purple satin skirt \n  * Organza overskirt with wavy hem, and mid-length organza overlay with silver foil accents \n\n### The bare necessities\n\n  * Body: polyester, exclusive of decoration\n  * Overlay: nylon, exclusive of decoration\n  * Imported\n\n',
        'images': [{'normal_size': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251650?$yetidetail$',
                    'thumbnail': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251650?$yetiProductThumb$',
                    'zoomed': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251650?$yetizoom$'},
                   {
                   'normal_size': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251650-1?$yetidetail$',
                   'thumbnail': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251650-1?$yetiProductThumb$',
                   'zoomed': u'http://cdn.s7.disneystore.com/is/image/DisneyShopping/4975055251650-1?$yetizoom$'}],
        'original_price': 29.95,
        'reviews': [{'author': u'Gina1234 ',
                     'body': u'My daughter loves her new Sofia nightgown especially because it purple. It is very beautiful and well made. We also took pictures of her in it and the color really stands out because color is not to bright or dull.',
                     'date': '2015-03-24',
                     'max_stars': 5,
                     'stars': 5,
                     'title': u'Fit for a princess'}],
        'sale_price': 20.96,
        'site_category_id': 1,
        'sizes': [u'3', u'4', u'5/6', u'7/8', u'9/10'],
        'title': u'Sofia Nightgown for Girls',
    }