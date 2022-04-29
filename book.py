import argparse
import logging
from logging import basicConfig, getLogger, DEBUG
import time
import datetime
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

basicConfig(level=DEBUG)
logger = getLogger(__name__)
for p in ['selenium', 'webdriver_manager', 'webdriver', 'selenium.webdriver', 'selenium.webdriver.chrome', 'urllib3']:
    logging.getLogger(p).setLevel(logging.WARNING)


URL = 'https://www.jr-odekake.net/goyoyaku/campaign/sunriseseto_izumo/form.html'
SEC_TO_WAIT = 10

CABIN_CHOICES = [
	3,	# 1人用　B寝台個室　シングルツイン
	6,	# 2人用　B寝台個室　サンライズツイン
]


def select_pull_down_by_text(driver, id_name, text, element_pos=0, exact_match=True):
	start_time = datetime.datetime.now()
	elapsed = 0
	while elapsed < SEC_TO_WAIT:
		els = [tag for tag in driver.find_elements(by='id', value=id_name)]
		try:
			logger.debug(els)
			el = els[element_pos]
		except IndexError:
			time.sleep(0.5)
			elapsed = (datetime.datetime.now() - start_time).seconds
			continue

		for option in el.find_elements(by='tag name', value='option'):
			if exact_match:
				if text == option.text:
					option.click()
					return True
			else:
				if text in option.text:
					option.click()
					return True

	return False


def click_radio_button(driver, for_name, element_pos=0):
	start_time = datetime.datetime.now()
	elapsed = 0
	while elapsed < SEC_TO_WAIT:
		els = [tag for tag in driver.find_elements(By.XPATH, '//label[@for="{}"]'.format(for_name))]
		try:
			logger.debug(els)
			el = els[element_pos]
			el.click()
			return True
		except IndexError:
			time.sleep(0.5)
			elapsed = (datetime.datetime.now() - start_time).seconds

	return False


def click_button(driver, id_name, element_pos=0):
	start_time = datetime.datetime.now()
	elapsed = 0
	while elapsed < SEC_TO_WAIT:
		els = [tag for tag in driver.find_elements(by='id', value=id_name)]
		try:
			logger.debug(els)
			el = els[element_pos]
			el.click()
			return True
		except IndexError:
			time.sleep(0.5)
			elapsed = (datetime.datetime.now() - start_time).seconds

	return False


def click_image(driver, alt_name, element_pos=0):
	start_time = datetime.datetime.now()
	elapsed = 0
	while elapsed < SEC_TO_WAIT:
		els = [tag for tag in driver.find_elements(By.XPATH, '//img[@alt="{}"]'.format(alt_name))]
		try:
			logger.debug(els)
			el = els[element_pos]
			el.click()
			return True
		except IndexError:
			time.sleep(0.5)
			elapsed = (datetime.datetime.now() - start_time).seconds

	return False


def main():
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('--userid', '-u', type=str, required=True)
	parser.add_argument('--password', '-p', type=str, required=True)
	parser.add_argument('--origin', '-o', type=str, default='東京')
	parser.add_argument('--destination', '-d', type=str, default='出雲市')
	parser.add_argument('--interval_month', type=int, default=1)
	parser.add_argument('--interval_day', type=int, default=0)
	parser.add_argument('--departure_hour', type=int, default=22)
	parser.add_argument('--departure_minute', type=int, default=0)
	parser.add_argument('--train_name', type=str, default='サンライズ出雲')
	parser.add_argument('--cabin_class', choices=[3, 6], default=3)

	args = parser.parse_args()
	userid = args.userid
	password = args.password
	origin = args.origin
	destination = args.destination
	cabin_class = 'radio-box-{}'.format(args.cabin_class)

	target_date = datetime.date.today() + relativedelta(months=args.interval_month, days=args.interval_day)
	logger.debug(f'Target date: {target_date}')

	browser = webdriver.Chrome(ChromeDriverManager().install())
	browser.get(URL)

	# 条件選択画面
	logger.debug(browser.title)
	select_pull_down_by_text(browser, 'jsSelectYear', '{}年'.format(target_date.year))
	select_pull_down_by_text(browser, 'jsSelectMonth', '{}月'.format(target_date.month))
	select_pull_down_by_text(browser, 'jsSelectDay', '{}日'.format(target_date.day))
	select_pull_down_by_text(browser, 'jsSelectHour', '{:02d}'.format(args.departure_hour))
	select_pull_down_by_text(browser, 'jsSelectMinute', '{:02d}'.format(args.departure_minute))
	select_pull_down_by_text(browser, 'jsSelectTrainType', args.train_name)
	select_pull_down_by_text(browser, 'inputDepartStName', origin)
	select_pull_down_by_text(browser, 'inputArriveStName', destination)
	click_radio_button(browser, cabin_class)

	click_button(browser, 'submitButton')

	# ログイン画面
	start_time = datetime.datetime.now()
	elapsed = 0
	while elapsed < SEC_TO_WAIT:
		try:
			logger.debug(browser.title)
			textbox = [tag for tag in browser.find_elements(By.XPATH, '//input[@name="id"]')][0]
			textbox.send_keys(userid)

			textbox = [tag for tag in browser.find_elements(By.XPATH, '//input[@name="password"]')][0]
			textbox.send_keys(password)

			browser.execute_script("document.getElementById('formHiddenSubmitJSButton').click();")
			break

		except Exception as e:
			logger.error(e)
			elapsed = (datetime.datetime.now() - start_time).seconds

	# ログイン完了画面
	start_time = datetime.datetime.now()
	elapsed = 0
	while elapsed < SEC_TO_WAIT:
		try:
			logger.debug(browser.title)
			iframe = browser.find_element_by_tag_name('iframe')
			browser.switch_to.frame(iframe)
			browser.find_element(By.XPATH, '//*[@id="submitBtn"]/p/a').click()

		except Exception as e:
			logger.error(e)
			elapsed = (datetime.datetime.now() - start_time).seconds


	time.sleep(30)



if __name__ == '__main__':
	main()
