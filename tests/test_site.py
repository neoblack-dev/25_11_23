from dataclasses import dataclass, replace
from time import sleep
import re
from playwright.sync_api import Page, expect, Route

# def test_wiki(page: Page):
#     page.goto('https://www.wikipedia.org/')
#     page.get_by_role('link', name='Русский').click()
#     expect(page.get_by_text('Добро пожаловать в Википедию,')).to_be_visible()

def test_wiki2(page:Page):
    page.goto('https://www.wikipedia.org/')
    page.get_by_role('link', name='Русский').click()
    page.get_by_role('link', name='Содержание').click()
    page.locator('#ca-talk').click()
    expect(page.locator('#firstHeading')).to_have_text('Обсуждение Википедии:Содержание')

def test_request(page:Page):
    def change_request(route: Route):
        data = route.request.post_data
        if data:
            data = data.replace('User', 'Usher')
        print(data)
        route.continue_(post_data=data)

    page.route(re.compile('profile/authenticate'), change_request)
    page.goto('https://gymlog.ru/profile/login/')
    page.locator('#email').fill('User412')
    page.locator('#password').fill('k9L-hL')
    page.get_by_role('button', name='Войти').click()
    sleep(5)

def test_response(page: Page):
    def change_response(route: Route):
        response = route.fetch()
        data = response.text()
        data = data.replace('User412','пирожок')
        route.fulfill(response=response, body=data)
    page.route(re.compile('profile/412'), change_response)
    page.goto('https://gymlog.ru/profile/login/')
    page.locator('#email').fill('User412')
    page.locator('#password').fill('k9L-hL')
    page.get_by_role('button', name='Войти').click()
    page.get_by_role('link', name='Мой профиль').click()
    sleep(7)