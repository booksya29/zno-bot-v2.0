import requests
from bs4 import BeautifulSoup
import os, json
from random import randint
from System.subject_list import subjects
from playwright.async_api import async_playwright
import shared
from aiogram import types

class Father_task():
    def __init__(self, chat_id):
        self.base_url = None 
        self.number_task = None #
        self.task_type = None #
      
        self.current_subject = None #
        self.chat_id = chat_id #
        self.true_answer = None
        self.browser = shared.browser

    


    async def parsing(self):
        self.get_current_subject()
        self.generate_number_task()
        self.base_url_get()
        self.url = self.base_url + str(self.number_task)
        await self.get_htlm_code()
        self.get_task_info()
        await self.get_task_photo()
    
    def base_url_get(self):
        self.base_url = subjects[self.current_subject]['url']

    def generate_number_task(self):
        max_task = subjects[self.current_subject]['tasks']
        self.number_task = randint(0, int(max_task))

    async def get_htlm_code(self):
        
        self.new_context = await self.browser.new_context()
        self.page = await self.new_context.new_page()
        await self.page.goto(self.url)
        html_text = await self.page.content()
        self.soup = BeautifulSoup(html_text, 'lxml')


    async def get_task_photo(self):
        self.photo_answers = None
        task_block = self.page.locator('div[class="task-card current"]')
        self.task_photo = await task_block.locator('form[class="q-test"]').screenshot()
        await self.new_context.close()

    def get_task_info(self):
        q_test = self.soup.find('form', class_='q-test')
        self.true_answer = q_test.find(name='input', attrs={'type':"hidden", 'name':"result"}).get('value')
        try:
            
            self.task_type = q_test.find_all('div', class_='description')[1].find('a').text
            
        except IndexError:
            
            self.task_type = q_test.find('div', class_='description').find('a').text
    def get_current_subject(self):
        f_path = os.path.join('System', 'stats.json')
        with open(f_path, 'rt', encoding='utf-8') as f:
            self.current_subject = json.load(f)[str(self.chat_id)]['cur_subject']
    
    def class_select(self):
        from types_classes import que_cor_1, free_form_que_1, sequence_que, right_3_question_7
        if self.task_type == 'Завдання з вибором однієї правильної відповіді':
            obj = que_cor_1(self.chat_id)
        elif self.task_type == 'Завдання відкритої форми з короткою відповіддю (1 вид)':
            obj = free_form_que_1(self.chat_id)
        elif self.task_type == 'Завдання на встановлення відповідності (логічні пари)' or self.task_type == 'Завдання на встановлення правильної послідовності':
            obj = sequence_que(self.chat_id)
        elif self.task_type == 'Завдання з вибором трьох правильних відповідей із семи запропонованих варіантів відповіді':
            obj = right_3_question_7(self.chat_id)
        else:
            print(f'Невідомий тип завдання: "{self.task_type}"')
            return None
        obj.soup = self.soup
        obj.url = self.url
        obj.task_type = self.task_type
        obj.true_answer = self.true_answer
        obj.number_task = self.number_task
        obj.task_photo = self.task_photo
        return obj
    
    
    
    async def question_send(self, message: types.Message, builder):
        await message.answer_photo(photo=types.BufferedInputFile(file=self.task_photo, filename='task.png'), caption='Оберіть правильну віповідь!', reply_markup=builder.as_markup())