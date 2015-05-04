import pytest

from helpers import fake_response_from_file
from letmescrape.spiders.disney_category import DisneyCategorySpider


@pytest.fixture
def spider():
    return DisneyCategorySpider()


def test_parse(spider):
    file_name = 'samples/disney_main.html'
    response = fake_response_from_file(file_name, url=spider.start_urls[0])
    result = list(spider.parse(response))

    assert result == [
        {'link': u'http://www.disneystore.com/mn/1000995/',
         'sub_categories': [{'link': u'http://www.disneystore.com/girls/mn/1000763+1000995/',
                             'title': u'New Arrivals for Girls'},
                            {'link': u'http://www.disneystore.com/boys/mn/1000762+1000995/',
                             'title': u'New Arrivals for Boys'},
                            {'link': u'http://www.disneystore.com/disney-baby/mn/1014201+1000995/',
                             'title': u'New Arrivals for Baby'},
                            {'link': u'http://www.disneystore.com/adults/mn/1000777+1000995/',
                             'title': u'New Arrivals for Adults'},
                            {'link': u'http://www.disneystore.com/disney-parks-product/mn/1001081+1000995/',
                             'title': u'New Arrivals for Disney Parks'},
                            {'link': u'http://www.disneystore.com/mn/1000995/',
                             'title': u'See All New Arrivals'}],
         'title': u'NEW!'}, {'link': u'http://www.disneystore.com/d-characters/mn/1000001/',
                             'sub_categories': [{'link': u'http://www.disneystore.com/101-dalmatians/mn/1010002/',
                                                 'title': u'101 Dalmatians'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/aladdin/mn/1000002/',
                                                'title': u'Aladdin'},
                                                {'link': u'http://www.disneystore.com/alice-in-wonderland/mn/1000003/',
                                                 'title': u'Alice in Wonderland'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/beauty-and-the-beast/mn/1000008/',
                                                'title': u'Beauty and the Beast'},
                                                {'link': u'http://www.disneystore.com/big-hero-6/mn/1025018/',
                                                 'title': u'Big Hero 6'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/brave/mn/1010606/',
                                                'title': u'Brave'},
                                                {'link': u'http://www.disneystore.com/cars/mn/1000012/',
                                                 'title': u'Cars'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/cinderella/mn/1000014/',
                                                'title': u'Cinderella'},
                                                {'link': u'http://www.disneystore.com/disney-junior/mn/1001079/',
                                                 'title': u'Disney Junior'},
                                                {'link': u'http://www.disneystore.com/disney-pixar/mn/1001073/',
                                                 'title': u'Disney Pixar Films'},
                                                {'link': u'http://www.disneystore.com/disney-princess/mn/1000016/',
                                                 'title': u'Disney Princess'},
                                                {'link': u'http://www.disneystore.com/disney-villains/mn/1000017/',
                                                 'title': u'Disney Villains'},
                                                {'link': u'http://www.disneystore.com/doc-mcstuffins/mn/1013903/',
                                                 'title': u'Doc McStuffins'},
                                                {'link': u'http://www.disneystore.com/finding-nemo/mn/1000020/',
                                                 'title': u'Finding Nemo'},
                                                {'link': u'http://www.disneystore.com/frozen/mn/1021701/',
                                                 'title': u'Frozen'},
                                                {
                                                'link': u'http://www.disneystore.com/jake-and-the-never-land-pirates/mn/1008304/',
                                                'title': u'Jake and the Never Land Pirates'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/the-little-mermaid/mn/1000031/',
                                                'title': u'The Little Mermaid'},
                                                {'link': u'http://www.disneystore.com/mickey-friends/mn/1000034/',
                                                 'title': u'Mickey & Friends'},
                                                {
                                                'link': u'http://www.disneystore.com/miles-from-tomorrowland/mn/1026802/',
                                                'title': u'Miles from Tomorrowland'},
                                                {'link': u'http://www.disneystore.com/monsters/mn/1000035/',
                                                 'title': u'Monsters'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/mulan/mn/1000036/',
                                                'title': u'Mulan'},
                                                {'link': u'http://www.disneystore.com/muppets/mn/1000037/',
                                                 'title': u'The Muppets'},
                                                {'link': u'http://www.disneystore.com/peter-pan/mn/1000039/',
                                                 'title': u'Peter Pan'},
                                                {'link': u'http://www.disneystore.com/phineas-and-ferb/mn/1000040/',
                                                 'title': u'Phineas and Ferb'},
                                                {'link': u'http://www.disneystore.com/planes/mn/1019303/',
                                                 'title': u'Planes'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/pocahontas/mn/1000043/',
                                                'title': u'Pocahontas'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/the-princess-and-the-frog/mn/1000047/',
                                                'title': u'The Princess and the Frog'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/sleeping-beauty/mn/1000049/',
                                                'title': u'Sleeping Beauty'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/snow-white-and-the-seven-dwarfs/mn/1000050/',
                                                'title': u'Snow White and the Seven Dwarfs'},
                                                {'link': u'http://www.disneystore.com/sofia-the-first/mn/1015502/',
                                                 'title': u'Sofia the First'},
                                                {'link': u'http://www.disneystore.com/star-wars/mn/1023301/',
                                                 'title': u'Star Wars'},
                                                {
                                                'link': u'http://www.disneystore.com/disney-princess/tangled/mn/1000052/',
                                                'title': u'Tangled'},
                                                {
                                                'link': u'http://www.disneystore.com/the-nightmare-before-christmas/mn/1000038/',
                                                'title': u"Tim Burton's The Nightmare Before Christmas"},
                                                {'link': u'http://www.disneystore.com/tinker-bell-fairies/mn/1000054/',
                                                 'title': u'Tinker Bell & Fairies'},
                                                {'link': u'http://www.disneystore.com/tomorrowland/mn/1028302/',
                                                 'title': u'Tomorrowland'},
                                                {'link': u'http://www.disneystore.com/toy-story/mn/1000055/',
                                                 'title': u'Toy Story'},
                                                {'link': u'http://www.disneystore.com/winnie-the-pooh/mn/1000044/',
                                                 'title': u'Winnie the Pooh'},
                                                {'link': u'http://www.disneystore.com/wreck-it-ralph/mn/1014703/',
                                                 'title': u'Wreck-It Ralph'},
                                                {'link': u'http://www.disneystore.com/marvel/mn/1000032/',
                                                 'sub_categories': [{
                                                                    'link': u'http://www.disneystore.com/marvel/the-avengers/mn/1011501/',
                                                                    'title': u'The Avengers'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/captain-america/mn/1000011/',
                                                                    'title': u'Captain America'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/marvel/guardians-of-the-galaxy/mn/1024507/',
                                                                    'title': u'Guardians of the Galaxy'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/hulk/mn/1000053/',
                                                                    'title': u'Hulk'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/iron-man/mn/1000025/',
                                                                    'title': u'Iron Man'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/marvel/thor/mn/1004304/',
                                                                    'title': u'Thor'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/spider-man/mn/1000051/',
                                                                    'title': u'Spider-Man'}],
                                                 'title': u'Marvel Characters'}],
                             'title': u'Characters'}, {'link': u'http://www.disneystore.com/d-products/mn/1000201/',
                                                       'sub_categories': [
                                                           {'link': u'http://www.disneystore.com/clothes/mn/1000204/',
                                                            'sub_categories': [{
                                                                               'link': u'http://www.disneystore.com/clothes/costumes-costume-accessories/mn/1000395/',
                                                                               'title': u'Costume Shop'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/swim-shop/mn/1017701/',
                                                                               'title': u'Swim Shop'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/sleepwear/mn/1000224/',
                                                                               'title': u'Sleep Shop'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/tees-tops-shirts/mn/1000228/',
                                                                               'title': u'Tees, Tops & Shirts'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/dresses-skirts/mn/1000217/',
                                                                               'title': u'Dresses & Skirts'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/fleece-outerwear/mn/1000219/',
                                                                               'title': u'Fleece & Outerwear'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/sets/mn/1000229/',
                                                                               'title': u'Top & Bottom Sets'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/rompers/mn/1010601/',
                                                                               'title': u'Rompers'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/clothes/mn/1000204/',
                                                                               'title': u'See All Clothes'}],
                                                            'title': u'Clothes'},
                                                           {
                                                           'link': u'http://www.disneystore.com/accessories/mn/1000216/',
                                                           'sub_categories': [{
                                                                              'link': u'http://www.disneystore.com/accessories/bags-totes/mn/1000291/',
                                                                              'title': u'Bags & Totes'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/jewelry/mn/1000295/',
                                                                              'title': u'Jewelry'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/tech-accessories/mn/1000235/',
                                                                              'title': u'Tech Accessories'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/backpacks-lunch-totes/mn/1000290/',
                                                                              'title': u'Backpacks & Lunch Totes'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/luggage/mn/1000366/',
                                                                              'title': u'Luggage'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/watches/mn/1000302/',
                                                                              'title': u'Watches'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/shoes-socks/mn/1000222/',
                                                                              'title': u'Shoes & Socks'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/accessories/mn/1000216/',
                                                                              'title': u'See All Accessories'}],
                                                           'title': u'Accessories'},
                                                           {'link': u'http://www.disneystore.com/toys/mn/1000208/',
                                                            'sub_categories': [{
                                                                               'link': u'http://www.disneystore.com/toys/plush/mn/1000267/',
                                                                               'title': u'Plush'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/dolls/mn/1000259/',
                                                                               'title': u'Dolls'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/play-sets-more/mn/1000265/',
                                                                               'title': u'Play Sets & More'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/action-figures/mn/1000255/',
                                                                               'title': u'Action Figures'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/small-toys-more/mn/1014307/',
                                                                               'title': u'Small Toys & More'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/games/mn/1014601/',
                                                                               'title': u'Games'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/die-cast-cars/mn/1011302/',
                                                                               'title': u'Die Cast Cars'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/die-cast-planes/mn/1019304/',
                                                                               'title': u'Die Cast Planes'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/toys/mn/1000208/',
                                                                               'title': u'See All Toys'}],
                                                            'title': u'Toys'},
                                                           {
                                                           'link': u'http://www.disneystore.com/home-decor/mn/1000207/',
                                                           'sub_categories': [{
                                                                              'link': u'http://www.disneystore.com/home-decor/kitchen-dinnerware/mn/1000248/',
                                                                              'title': u'Kitchen & Dinnerware'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/bed-bath/mn/1000242/',
                                                                              'title': u'Bed & Bath'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/stationery-office/mn/1000252/',
                                                                              'title': u'Stationery & Office'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/bed-bath/fleece-throws-blankets/mn/1000334/',
                                                                              'title': u'Fleece Throws & Blankets'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/seasonal/mn/1000399/',
                                                                              'title': u'Seasonal'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/photo-memories/mn/1000251/',
                                                                              'title': u'Photo & Memories'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/home-accents-lighting/mn/1000247/',
                                                                              'title': u'Home Accents & Lighting'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/home-decor/mn/1000207/',
                                                                              'title': u'See All Home & D\xe9cor'}],
                                                           'title': u'Home & D\xe9cor'},
                                                           {
                                                           'link': u'http://www.disneystore.com/entertainment/mn/1000205/',
                                                           'sub_categories': [{
                                                                              'link': u'http://www.disneystore.com/entertainment/movies/mn/1000233/',
                                                                              'title': u'Movies'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/toys/games/video-games/mn/1000261/',
                                                                              'title': u'Video Games'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/entertainment/books/mn/1000232/',
                                                                              'title': u'Books'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/entertainment/mn/1000205/',
                                                                              'title': u'See All Entertainment'}],
                                                           'title': u'Entertainment'},
                                                           {
                                                           'link': u'http://www.disneystore.com/collectibles/mn/1000202/',
                                                           'sub_categories': [{
                                                                              'link': u'http://www.disneystore.com/vinylmation/mn/1000828/',
                                                                              'title': u'Vinylmation'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/collectibles/pins/mn/1000211/',
                                                                              'title': u'Pins'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/collectibles/figurines-keepsakes/mn/1000276/',
                                                                              'title': u'Figurines & Keepsakes'},
                                                                              {
                                                                              'link': u'http://www.disneystore.com/collectibles/mn/1000202/',
                                                                              'title': u'See All Collectibles'}],
                                                           'title': u'Collectibles'},
                                                           {'sub_categories': [{
                                                                               'link': u'http://www.disneystore.com/personalization-shop/mn/1001279/',
                                                                               'title': u'Personalization Shop'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/disney-tsum-tsum/mn/1024503/',
                                                                               'title': u'Tsum Tsum'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/moments-that-made-disney/mn/1025033/',
                                                                               'title': u'Monthly Collectible Ornaments'}],
                                                            'title': u'In the Spotlight'},
                                                           {'sub_categories': [{
                                                                               'link': u'http://www.disneystore.com/summer-fun-collection/mn/1010602/',
                                                                               'title': u'Summer Fun'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/disney-animators-collection/mn/1007201/',
                                                                               'title': u"Animators' Dolls"},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/i-love-mickey-collection/mn/1009302/',
                                                                               'title': u'I Love Mickey'},
                                                                               {
                                                                               'link': u'http://www.disneystore.com/walt-disney-studios-collection/mn/1006105/',
                                                                               'title': u'Walt Disney Studios'}],
                                                            'title': u'Collections'},
                                                           {
                                                           'link': u'http://www.disneystore.com/gift-cards/mn/1001265/',
                                                           'title': u'Gift Cards'}],
                                                       'title': u'Products'},
        {'link': u'http://www.disneystore.com/girls/mn/1000763/',
         'sub_categories': [{'link': u'http://www.disneystore.com/d-characters/mn/1000001/',
                             'sub_categories': [
                                 {'link': u'http://www.disneystore.com/frozen/mn/1021701/', 'title': u'Frozen'},
                                 {'link': u'http://www.disneystore.com/disney-princess/the-little-mermaid/mn/1000031/',
                                  'title': u'The Little Mermaid'},
                                 {'link': u'http://www.disneystore.com/disney-princess/cinderella/mn/1000014/',
                                  'title': u'Cinderella'},
                                 {'link': u'http://www.disneystore.com/mickey-friends/minnie-mouse/mn/1000132/',
                                  'title': u'Minnie Mouse'},
                                 {'link': u'http://www.disneystore.com/disney-princess/tangled/mn/1000052/',
                                  'title': u'Tangled'},
                                 {'link': u'http://www.disneystore.com/tinker-bell-fairies/mn/1000054/',
                                  'title': u'Tinker Bell & Fairies'},
                                 {'link': u'http://www.disneystore.com/disney-princess/sleeping-beauty/mn/1000049/',
                                  'title': u'Sleeping Beauty'},
                                 {
                                 'link': u'http://www.disneystore.com/disney-princess/beauty-and-the-beast/mn/1000008/',
                                 'title': u'Beauty and the Beast'},
                                 {'link': u'http://www.disneystore.com/d-characters/mn/1000001/',
                                  'title': u'See All Characters'}],
                             'title': u'Characters'},
                            {'link': u'http://www.disneystore.com/clothes/girls/mn/1000204+1000763/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/clothes/costumes-costume-accessories/girls/mn/1000395+1000763/',
                                                'title': u'Costumes'},
                                                {
                                                'link': u'http://www.disneystore.com/girls/swim-shop/mn/1000763+1017701/',
                                                'title': u'Swimwear'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/sleepwear/girls/mn/1000224+1000763/',
                                                'title': u'Sleepwear'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/tees-tops-shirts/girls/mn/1000228+1000763/',
                                                'title': u'Tees, Tops & Shirts'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/girls/mn/1000204+1000763/',
                                                'title': u'See All Clothes'}],
                             'title': u'Clothes'},
                            {'link': u'http://www.disneystore.com/accessories/girls/mn/1000216+1000763/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/accessories/shoes-socks/girls/mn/1000222+1000763/',
                                                'title': u'Shoes & Socks'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/bags-totes/girls/mn/1000291+1000763/',
                                                'title': u'Bags & Totes'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/girls/mn/1000216+1000763/',
                                                'title': u'See All Accessories'}],
                             'title': u'Accessories'},
                            {'link': u'http://www.disneystore.com/toys/girls/mn/1000208+1000763/',
                             'sub_categories': [{'link': u'http://www.disneystore.com/toys/dolls/mn/1000259/',
                                                 'title': u'Dolls'},
                                                {'link': u'http://www.disneystore.com/toys/plush/mn/1000267/',
                                                 'title': u'Plush'},
                                                {'link': u'http://www.disneystore.com/toys/play-sets-more/mn/1000265/',
                                                 'title': u'Play Sets & More'},
                                                {'link': u'http://www.disneystore.com/toys/action-figures/mn/1000255/',
                                                 'title': u'Action Figures'},
                                                {'link': u'http://www.disneystore.com/toys/girls/mn/1000208+1000763/',
                                                 'title': u'See All Toys'}],
                             'title': u'Toys'},
                            {'link': u'http://www.disneystore.com/home-decor/girls/mn/1000207+1000763/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/home-decor/bed-bath/bedding/girls/mn/1000327+1000763/',
                                                'title': u'Bedding'},
                                                {
                                                'link': u'http://www.disneystore.com/home-decor/stationery-office/girls/mn/1000252+1000763/',
                                                'title': u'Stationery'},
                                                {
                                                'link': u'http://www.disneystore.com/home-decor/girls/mn/1000207+1000763/',
                                                'title': u'See All Home & D\xe9cor'}],
                             'title': u'Home & D\xe9cor'},
                            {'sub_categories': [{'link': u'http://www.disneystore.com/personalization-shop/mn/1001279/',
                                                 'title': u'Personalization Shop'},
                                                {'link': u'http://www.disneystore.com/disney-tsum-tsum/mn/1024503/',
                                                 'title': u'Tsum Tsum'},
                                                {'link': u'http://www.disneystore.com/disney-infinity/mn/1017501/',
                                                 'title': u'Disney Infinity'},
                                                {'link': u'http://www.disneystore.com/kids-meal-time-magic/mn/1000859/',
                                                 'title': u'Meal Time Magic'}],
                             'title': u'In the Spotlight'},
                            {'link': u'http://www.disneystore.com/entertainment/mn/1000205/',
                             'title': u'Entertainment'},
                            {'link': u'http://www.disneystore.com/gift-cards/mn/1001265/',
                             'title': u'Gift Cards'}],
         'title': u'Girls'}, {'link': u'http://www.disneystore.com/boys/mn/1000762/',
                              'sub_categories': [{'link': u'http://www.disneystore.com/d-characters/mn/1000001/',
                                                  'sub_categories': [
                                                      {'link': u'http://www.disneystore.com/big-hero-6/mn/1025018/',
                                                       'title': u'Big Hero 6'},
                                                      {'link': u'http://www.disneystore.com/cars/mn/1000012/',
                                                       'title': u'Cars'},
                                                      {'link': u'http://www.disneystore.com/mickey-friends/mn/1000034/',
                                                       'title': u'Mickey & Friends'},
                                                      {'link': u'http://www.disneystore.com/d-characters/mn/1000001/',
                                                       'title': u'See All Characters'}],
                                                  'title': u'Characters'},
                                                 {'link': u'http://www.disneystore.com/marvel/mn/1000032/',
                                                  'sub_categories': [
                                                      {'link': u'http://www.disneystore.com/spider-man/mn/1000051/',
                                                       'title': u'Spider-Man'},
                                                      {
                                                      'link': u'http://www.disneystore.com/marvel/the-avengers/mn/1011501/',
                                                      'title': u'The Avengers'},
                                                      {
                                                      'link': u'http://www.disneystore.com/marvel/guardians-of-the-galaxy/mn/1024507/',
                                                      'title': u'Guardians of the Galaxy'},
                                                      {'link': u'http://www.disneystore.com/marvel/mn/1000032/',
                                                       'title': u'See All Marvel Characters'}],
                                                  'title': u'Marvel Characters'},
                                                 {
                                                 'link': u'http://www.disneystore.com/clothes/boys/mn/1000204+1000762/',
                                                 'sub_categories': [{
                                                                    'link': u'http://www.disneystore.com/clothes/tees-tops-shirts/boys/mn/1000228+1000762/',
                                                                    'title': u'Tees, Tops & Shirts'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/clothes/sleepwear/boys/mn/1000224+1000762/',
                                                                    'title': u'Sleepwear'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/clothes/costumes-costume-accessories/boys/mn/1000395+1000762/',
                                                                    'title': u'Costumes'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/boys/swim-shop/mn/1000762+1017701/',
                                                                    'title': u'Swimwear'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/clothes/boys/mn/1000204+1000762/',
                                                                    'title': u'See All Clothes'}],
                                                 'title': u'Clothes'},
                                                 {
                                                 'link': u'http://www.disneystore.com/accessories/boys/mn/1000216+1000762/',
                                                 'sub_categories': [{
                                                                    'link': u'http://www.disneystore.com/accessories/shoes-socks/boys/mn/1000222+1000762/',
                                                                    'title': u'Shoes & Socks'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/accessories/hats-gloves-scarves/boys/mn/1000294+1000762/',
                                                                    'title': u'Hats, Gloves & Scarves'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/accessories/boys/mn/1000216+1000762/',
                                                                    'title': u'See All Accessories'}],
                                                 'title': u'Accessories'},
                                                 {'link': u'http://www.disneystore.com/toys/boys/mn/1000208+1000762/',
                                                  'sub_categories': [
                                                      {'link': u'http://www.disneystore.com/toys/plush/mn/1000267/',
                                                       'title': u'Plush'},
                                                      {
                                                      'link': u'http://www.disneystore.com/toys/action-figures/mn/1000255/',
                                                      'title': u'Action Figures'},
                                                      {
                                                      'link': u'http://www.disneystore.com/toys/die-cast-cars/mn/1011302/',
                                                      'title': u'Die Cast Cars'},
                                                      {
                                                      'link': u'http://www.disneystore.com/toys/play-sets-more/mn/1000265/',
                                                      'title': u'Play Sets & More'},
                                                      {
                                                      'link': u'http://www.disneystore.com/toys/boys/mn/1000208+1000762/',
                                                      'title': u'See All Toys'}],
                                                  'title': u'Toys'},
                                                 {
                                                 'link': u'http://www.disneystore.com/home-decor/boys/mn/1000207+1000762/',
                                                 'sub_categories': [{
                                                                    'link': u'http://www.disneystore.com/home-decor/bed-bath/bedding/boys/mn/1000327+1000762/',
                                                                    'title': u'Bedding'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/home-decor/stationery-office/boys/mn/1000252+1000762/',
                                                                    'title': u'Stationery'},
                                                                    {
                                                                    'link': u'http://www.disneystore.com/home-decor/boys/mn/1000207+1000762/',
                                                                    'title': u'See All Home & D\xe9cor'}],
                                                 'title': u'Home & D\xe9cor'},
                                                 {'sub_categories': [{
                                                                     'link': u'http://www.disneystore.com/personalization-shop/mn/1001279/',
                                                                     'title': u'Personalization Shop'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-tsum-tsum/mn/1024503/',
                                                                     'title': u'Tsum Tsum'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-infinity/mn/1017501/',
                                                                     'title': u'Disney Infinity'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/kids-meal-time-magic/mn/1000859/',
                                                                     'title': u'Meal Time Magic'}],
                                                  'title': u'In the Spotlight'},
                                                 {'link': u'http://www.disneystore.com/entertainment/mn/1000205/',
                                                  'title': u'Entertainment'},
                                                 {'link': u'http://www.disneystore.com/gift-cards/mn/1001265/',
                                                  'title': u'Gift Cards'}],
                              'title': u'Boys'}, {'link': u'http://www.disneystore.com/disney-baby/mn/1014201/',
                                                  'sub_categories': [{'sub_categories': [{
                                                                                         'link': u'http://www.disneystore.com/disney-baby/dressing-baby/mn/1000902/',
                                                                                         'title': u'Dressing Baby'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/in-the-nursery/mn/1000906/',
                                                                                         'title': u'In the Nursery'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/bathtime/mn/1000907/',
                                                                                         'title': u'Bathtime'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/playtime/mn/1000903/',
                                                                                         'title': u'Playtime'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/baby-s-first/mn/1000911/',
                                                                                         'title': u"Baby's Firsts"},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/on-the-go/mn/1000909/',
                                                                                         'title': u'On the Go'}],
                                                                      'title': u'Moments of the Day'},
                                                                     {'sub_categories': [{
                                                                                         'link': u'http://www.disneystore.com/disney-baby/minnie-fashion-collection/mn/1014201+1014210/',
                                                                                         'title': u'Minnie Fashion'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/mickey-fashion-collection/mn/1014201+1014209/',
                                                                                         'title': u'Mickey Fashion'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/nemo-fashion-collection/mn/1014201+1018703/',
                                                                                         'title': u'Finding Nemo Fashion'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/winnie-the-pooh-fashion-collection/mn/1014201+1016907/',
                                                                                         'title': u'Winnie the Pooh Fashion'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/storybook-collection/mn/1014201+1007604/',
                                                                                         'title': u'Storybook Collection'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/dumbo/layette-collection/mn/1000018+1017403/',
                                                                                         'title': u'Dumbo Layette'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/mickey-friends/disney-baby/layette-collection/mn/1000034+1014201+1017403/',
                                                                                         'title': u'Mickey & Minnie Layette'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/thumper-layette-collection/mn/1014201+1024202/',
                                                                                         'title': u'Thumper & Miss Bunny Layette'}],
                                                                      'title': u'Collections'},
                                                                     {'sub_categories': [{
                                                                                         'link': u'http://www.disneystore.com/disney-baby/mn/1014201+1001222/',
                                                                                         'title': u'Personalized Gifts'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/layette-collection/mn/1014201+1017403/',
                                                                                         'title': u'Layette'},
                                                                                         {
                                                                                         'link': u'http://www.disneystore.com/disney-baby/swim-shop/mn/1014201+1017701/',
                                                                                         'title': u'Swimwear'}],
                                                                      'title': u'In the Spotlight'}],
                                                  'title': u'Baby'},
        {'link': u'http://www.disneystore.com/adults/mn/1000777/',
         'sub_categories': [{'link': u'http://www.disneystore.com/clothes/women/mn/1000204+1000765/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/clothes/tees-tops-shirts/women/mn/1000228+1000765/',
                                                'title': u'Tees, Tops & Shirts'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/sleepwear/women/mn/1000224+1000765/',
                                                'title': u'Sleepwear'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/fleece-outerwear/women/mn/1000219+1000765/',
                                                'title': u'Fleece & Outerwear'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/women/mn/1000204+1000765/',
                                                'title': u'See All Clothes for Women'}],
                             'title': u'Clothes for Women'},
                            {'link': u'http://www.disneystore.com/clothes/men/mn/1000204+1000764/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/clothes/tees-tops-shirts/men/mn/1000228+1000764/',
                                                'title': u'Tees, Tops & Shirts'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/sleepwear/men/mn/1000224+1000764/',
                                                'title': u'Sleepwear'},
                                                {
                                                'link': u'http://www.disneystore.com/clothes/fleece-outerwear/men/mn/1000219+1000764/',
                                                'title': u'Fleece & Outerwear'},
                                                {'link': u'http://www.disneystore.com/clothes/men/mn/1000204+1000764/',
                                                 'title': u'See All Clothes for Men'}],
                             'title': u'Clothes for Men'},
                            {'link': u'http://www.disneystore.com/accessories/adults/mn/1000216+1000777/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/accessories/bags-totes/adults/mn/1000291+1000777/',
                                                'title': u'Bags & Totes'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/jewelry/adults/mn/1000295+1000777/',
                                                'title': u'Jewelry'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/watches/adults/mn/1000302+1000777/',
                                                'title': u'Watches'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/tech-accessories/adults/mn/1000235+1000777/',
                                                'title': u'Tech Accessories'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/ear-hats-mickey-mitts/adults/mn/1000292+1000777/',
                                                'title': u"Ear Hats & ''Mickey Mitts''"},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/hats-gloves-scarves/adults/mn/1000294+1000777/',
                                                'title': u'Hats, Gloves & Scarves'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/luggage/adults/mn/1000366+1000777/',
                                                'title': u'Luggage'},
                                                {
                                                'link': u'http://www.disneystore.com/accessories/adults/mn/1000216+1000777/',
                                                'title': u'See All Accessories'}],
                             'title': u'Accessories'},
                            {'link': u'http://www.disneystore.com/entertainment/mn/1000205/',
                             'title': u'Entertainment'},
                            {'link': u'http://www.disneystore.com/home-decor/mn/1000207/',
                             'sub_categories': [{
                                                'link': u'http://www.disneystore.com/home-decor/kitchen-dinnerware/adults/mn/1000248+1000777/',
                                                'title': u'Kitchen & Dinnerware'},
                                                {
                                                'link': u'http://www.disneystore.com/home-decor/stationery-office/adults/mn/1000252+1000777/',
                                                'title': u'Stationery & Office'},
                                                {
                                                'link': u'http://www.disneystore.com/home-decor/home-accents-lighting/adults/mn/1000247+1000777/',
                                                'title': u'Home Accents & Lighting'},
                                                {'link': u'http://www.disneystore.com/home-decor/mn/1000207/',
                                                 'title': u'See All Home & D\xe9cor'}],
                             'title': u'Home & D\xe9cor'},
                            {'link': u'http://www.disneystore.com/collectibles/mn/1000202/',
                             'sub_categories': [{'link': u'http://www.disneystore.com/vinylmation/mn/1000828/',
                                                 'title': u'Vinylmation'},
                                                {
                                                'link': u'http://www.disneystore.com/collectibles/figurines-keepsakes/mn/1000276/',
                                                'title': u'Figurines & Keepsakes'},
                                                {'link': u'http://www.disneystore.com/collectibles/pins/mn/1000211/',
                                                 'title': u'Pins'},
                                                {'link': u'http://www.disneystore.com/collectibles/mn/1000202/',
                                                 'title': u'See All Collectibles'}],
                             'title': u'Collectibles'},
                            {'sub_categories': [{'link': u'http://www.disneystore.com/personalization-shop/mn/1001279/',
                                                 'title': u'Personalization Shop'},
                                                {
                                                'link': u'http://www.disneystore.com/moments-that-made-disney/mn/1025033/',
                                                'title': u'Monthly Collectible Ornaments'}],
                             'title': u'In the Spotlight'},
                            {
                            'sub_categories': [{'link': u'http://www.disneystore.com/summer-fun-collection/mn/1010602/',
                                                'title': u'Summer Fun'},
                                               {
                                               'link': u'http://www.disneystore.com/i-love-mickey-collection/mn/1009302/',
                                               'title': u'I Love Mickey'},
                                               {
                                               'link': u'http://www.disneystore.com/walt-disney-studios-collection/mn/1006105/',
                                               'title': u'Walt Disney Studios'},
                                               {'link': u'http://www.disneystore.com/disney-on-broadway/mn/1001075/',
                                                'title': u'Disney on Broadway'}],
                            'title': u'Collections'},
                            {'link': u'http://www.disneystore.com/gift-cards/mn/1001265/',
                             'title': u'Gift Cards'}],
         'title': u'Adults'}, {'link': u'http://www.disneystore.com/disney-parks-product/mn/1001081/',
                               'sub_categories': [{
                                                  'link': u'http://www.disneystore.com/disney-parks-product/clothes/mn/1001081+1000204/',
                                                  'sub_categories': [{
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/clothes/women/mn/1001081+1000204+1000765/',
                                                                     'title': u'Clothes for Women'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/clothes/men/mn/1001081+1000204+1000764/',
                                                                     'title': u'Clothes for Men'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/clothes/girls/mn/1001081+1000204+1000763/',
                                                                     'title': u'Clothes for Girls'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/clothes/boys/mn/1001081+1000204+1000762/',
                                                                     'title': u'Clothes for Boys'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/clothes/mn/1001081+1000204/',
                                                                     'title': u'See All Clothes'}],
                                                  'title': u'Clothes'},
                                                  {
                                                  'link': u'http://www.disneystore.com/disney-parks-product/accessories/mn/1001081+1000216/',
                                                  'sub_categories': [{
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/accessories/bags-totes/mn/1001081+1000291/',
                                                                     'title': u'Bags & Totes'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/accessories/jewelry/mn/1001081+1000295/',
                                                                     'title': u'Jewelry'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/accessories/tech-accessories/mn/1001081+1000235/',
                                                                     'title': u'Tech Accessories'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/accessories/hats-gloves-scarves/mn/1001081+1000294/',
                                                                     'title': u'Hats, Gloves & Scarves'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/accessories/mn/1001081+1000216/',
                                                                     'title': u'See All Accessories'}],
                                                  'title': u'Accessories'},
                                                  {
                                                  'link': u'http://www.disneystore.com/disney-parks-product/home-decor/mn/1001081+1000207/',
                                                  'sub_categories': [{
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/home-decor/kitchen-dinnerware/mn/1001081+1000248/',
                                                                     'title': u'Kitchen & Dinnerware'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/home-decor/bed-bath/mn/1001081+1000242/',
                                                                     'title': u'Bed & Bath'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/home-decor/stationery-office/mn/1001081+1000252/',
                                                                     'title': u'Stationery & Office'},
                                                                     {
                                                                     'link': u'http://www.disneystore.com/disney-parks-product/home-decor/mn/1001081+1000207/',
                                                                     'title': u'See All Home & D\xe9cor'}],
                                                  'title': u'Home & D\xe9cor'},
                                                  {
                                                  'link': u'http://www.disneystore.com/disney-parks-product/collectibles/mn/1001081+1000202/',
                                                  'sub_categories': [
                                                      {'link': u'http://www.disneystore.com/vinylmation/mn/1000828/',
                                                       'title': u'Vinylmation'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/collectibles/pins/mn/1001081+1000211/',
                                                      'title': u'Pins'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/collectibles/figurines-keepsakes/mn/1001081+1000276/',
                                                      'title': u'Figurines & Keepsakes'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/collectibles/art/mn/1001081+1000209/',
                                                      'title': u'Art'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/collectibles/mn/1001081+1000202/',
                                                      'title': u'See All Collectibles'}],
                                                  'title': u'Collectibles'},
                                                  {
                                                  'link': u'http://www.disneystore.com/disney-parks-product/toys/mn/1001081+1000208/',
                                                  'title': u'Toys'},
                                                  {
                                                  'link': u'http://www.disneystore.com/disney-parks-product/travel-vacation/mn/1001081+1000254/',
                                                  'sub_categories': [
                                                      {'link': u'http://www.disneystore.com/magicband/mn/1024701/',
                                                       'title': u'MagicBand'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/accessories/ear-hats-mickey-mitts/mn/1001081+1000292/',
                                                      'title': u'Ear Hats'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/home-decor/photo-memories/mn/1001081+1000251/',
                                                      'title': u'Photo & Memories'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/accessories/luggage/mn/1001081+1000366/',
                                                      'title': u'Luggage'},
                                                      {
                                                      'link': u'http://www.disneystore.com/2015-dated-merchandise/mn/1025901/',
                                                      'title': u'Dated 2015'},
                                                      {
                                                      'link': u'http://www.disneystore.com/disney-parks-product/travel-vacation/mn/1001081+1000254/',
                                                      'title': u'See All Vacation FUNdamentals'}],
                                                  'title': u'Vacation FUNdamentals'},
                                                  {'link': u'http://www.disneystore.com/resorts-more/mn/1025028/',
                                                   'sub_categories': [{
                                                                      'link': u'http://www.disneystore.com/resorts-more/walt-disney-world/mn/1001080/',
                                                                      'title': u'Walt Disney World'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/resorts-more/disneyland/mn/1001076/',
                                                                      'title': u'Disneyland'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/resorts-more/mn/1025028/',
                                                                      'title': u'See All Resorts & More'}],
                                                   'title': u'Resorts & More'},
                                                  {'sub_categories': [{
                                                                      'link': u'http://www.disneystore.com/the-haunted-mansion-collection/mn/1020302/',
                                                                      'title': u'The Haunted Mansion'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/disney-parks-product/holiday/mn/1001081+1000882/',
                                                                      'title': u"Disney's Days of Christmas"},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/marketplace-co-op-collection/mn/1024702/',
                                                                      'title': u'Marketplace Co-Op'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/star-wars-collection-disney-parks/mn/1023302/',
                                                                      'title': u'Star Wars'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/disney-parks-product/wedding/mn/1001081+1014207/',
                                                                      'title': u'Wedding'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/disney-parks-product/the-nightmare-before-christmas/mn/1001081+1000038/',
                                                                      'title': u'The Nightmare Before Christmas'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/disney-dream-collection-jewelry/mn/1012901/',
                                                                      'title': u'Disney Dream Fine Jewelry'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/disney-parks-storybook-attractions-collection/mn/1006805/',
                                                                      'title': u'Storybook'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/boutique/mn/1027902/',
                                                                      'title': u'Boutique'}],
                                                   'title': u'Collections'},
                                                  {'sub_categories': [{
                                                                      'link': u'http://www.disneystore.com/disney-parks-product/mn/1001081+1000995/',
                                                                      'title': u'New Arrivals'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/disney-parks-special-events/mn/1009902/',
                                                                      'title': u'Limited Release Items'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/made-with-magic/mn/1028303/',
                                                                      'title': u'Made with Magic'}],
                                                   'title': u'In the Spotlight'},
                                                  {'sub_categories': [{
                                                                      'link': u'http://www.disneystore.com/disney-parks-collection-by-pandora/mn/1025021/',
                                                                      'title': u'PANDORA'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/dooney-bourke/mn/1000812/',
                                                                      'title': u'Dooney & Bourke'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/alex-and-ani/mn/1014204/',
                                                                      'title': u'Alex and Ani'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/vera-bradley/mn/1023101/',
                                                                      'title': u'Vera Bradley'},
                                                                      {
                                                                      'link': u'http://www.disneystore.com/arribas-bros-collection/mn/1003801/',
                                                                      'title': u'Arribas Bros.'}],
                                                   'title': u'Classic Collaborations'},
                                                  {
                                                  'link': u'http://www.disneystore.com/disney-parks-product/mn/1001081+1001152/',
                                                  'title': u'Sale'}],
                               'title': u'Disney Parks Product'},
        {'link': u'http://www.disneystore.com/swim-shop/mn/1017701/',
         'sub_categories': [{'link': u'http://www.disneystore.com/girls/swim-shop/mn/1000763+1017701/',
                             'title': u'Swimwear for Girls'},
                            {'link': u'http://www.disneystore.com/boys/swim-shop/mn/1000762+1017701/',
                             'title': u'Swimwear for Boys'},
                            {'link': u'http://www.disneystore.com/baby/swim-shop/mn/1000772+1017701/',
                             'title': u'Swimwear for Baby'},
                            {'link': u'http://www.disneystore.com/accessories/sunglasses/swim-shop/mn/1000298+1017701/',
                             'title': u'Sunglasses & Swim Goggles'},
                            {
                            'link': u'http://www.disneystore.com/accessories/shoes-socks/swim-shop/mn/1000222+1017701/',
                            'title': u'Flip Flops & Swim Shoes'},
                            {
                            'link': u'http://www.disneystore.com/accessories/hats-gloves-scarves/swim-shop/mn/1000294+1017701/',
                            'title': u'Swim Hats'},
                            {'link': u'http://www.disneystore.com/accessories/bags-totes/swim-shop/mn/1000291+1017701/',
                             'title': u'Swim Bags'},
                            {
                            'link': u'http://www.disneystore.com/accessories/beach-towels/swim-shop/mn/1000367+1017701/',
                            'title': u'Beach Towels'},
                            {
                            'link': u'http://www.disneystore.com/clothes/swimwear/cover-ups/swim-shop/mn/1000309+1017701/',
                            'title': u'Cover-Ups'},
                            {'link': u'http://www.disneystore.com/swim-shop/mn/1017701+1001222/',
                             'title': u'Personalized Swimwear'}],
         'title': u'Swim Shop'}, {'link': u'http://www.disneystore.com/mn/1001152/',
                                  'sub_categories': [
                                      {'link': u'http://www.disneystore.com/mn/1001152/', 'title': u'Sale'},
                                      {'link': u'http://www.disneystore.com/special-offers/mn/1001266/',
                                       'title': u'Special Offers'},
                                      {'link': u'http://www.disneystore.com/tink-s-treasure/mn/1001232/',
                                       'title': u"Tink's Treasure"}],
                                  'title': u'Sale'}
    ]