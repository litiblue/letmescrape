========================
letmescrape
========================

해외 쇼핑몰 사이트의 카테고리와 상품 정보를 스크래핑하기 위한 프로젝트.


Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/development.txt

For production::

    $ pip install -r requirements/production.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*


Splash
=============================
Javascript를 필요로 하는 사이트를 스크래핑하기 위해서는 Splash service가 실행 중이어야 합니다.
https://splash.readthedocs.org/ 참고

Tests
=============================
Test::

    $ py.test

Test with coverage::

    $ py.test --cov letmescrape tests/

Test with coverage reporting::

    $ py.test --cov letmescrape tests/ --cov-report html

import error가 발생할 경우 pip install -e . 명령을 수행해줍니다.
http://pytest.org/latest/goodpractises.html#choosing-a-test-layout-import-rules 참고
