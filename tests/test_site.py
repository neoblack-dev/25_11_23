from time import sleep
import re
from playwright.sync_api import Page, expect, Route, Dialog, BrowserContext

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

def test_alert(page: Page):
    page.goto('https://demoblaze.com/')
    def accept_alert(alert: Dialog):
        print(alert.message)
        alert.accept()
    page.on('dialog',accept_alert)
    page.get_by_role('link', name='Samsung galaxy s6').click()
    page.get_by_role('link', name='Add to cart').click()
    page.wait_for_event('dialog')
    page.locator('#cartur').click()
    sleep(2)

def test_tabs(page: Page, context: BrowserContext):
    page.goto('https://nomads.com/', wait_until='domcontentloaded')
    with context.expect_page() as new_tab_event:
        page.get_by_alt_text('Get insured').click()
        new_tab = new_tab_event.value
    new_tab.get_by_role('link', name='Sign me up').click()
    sleep(5)

def test_iframe(page: Page):
    page.goto('https://www.w3schools.com/html/html_iframe.asp', wait_until='domcontentloaded')
    page.frame_locator('iframe[title="W3Schools HTML Tutorial"]').get_by_role('button', name='Sign in').click()
    sleep(3)

def test_select(page: Page):
    page.goto('https://www.sql-ex.ru/learn_exercises.php')
    page.select_option('select[name="lsttpl"]', label="English")
    sleep(5)
