from base_class import Father_task
from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
import parsing






class que_cor_1(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.letters_list = ['a','b','c','d','e']
    
    async def answer_question_callback(self, message: types.Message):
        builder = InlineKeyboardBuilder()
        for i in self.letters_list:
            i_replaced = i.replace('a', 'А').replace('b','Б').replace('c','В').replace('d','Г').replace('e','Д')
            if i == self.true_answer:
                builder.button(text=i_replaced, callback_data='47293856')
            else:
                builder.button(text=i_replaced, callback_data='47293156')
        await self.question_send(message, builder)

class free_form_que_1(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
    
    async def answer_question_callback(self, message: types.Message):
        answer_list = parsing.wrong_answer_generate_free_form(self.true_answer)
        builder = InlineKeyboardBuilder()
        for i in answer_list:
            if float(i) == float(self.true_answer):
                builder.button(text=str(i), callback_data='47293856')
            else:
                builder.button(text = str(i), callback_data='47293156')
        await self.question_send(message, builder)



        
class sequence_que(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
    
    async def answer_question_callback(self, message: types.Message):
        answers_list = parsing.generate_wrong_answers(self.true_answer)
        answers_list.append(self.true_answer)
        builder = InlineKeyboardBuilder()
        for i in answers_list:
            i_replaced = i.replace('a', 'А').replace('b','Б').replace('c','В').replace('d','Г').replace('e','Д')
            if i == self.true_answer:
                builder.button(text=str(i_replaced), callback_data='47293856')
            else:
                builder.button(text=str(i_replaced), callback_data='47293156')
        await self.question_send(message, builder)


class right_3_question_7(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
    
    async def answer_question_callback(self, message: types.Message):
        builder = InlineKeyboardBuilder()
        done_answers = parsing.generate_random_7(self.true_answer)
        for answer in done_answers:
            if answer == self.true_answer:
                builder.button(text = answer, callback_data = '47293856')
            else:
                builder.button(text=answer, callback_data = '47293156')
        await self.question_send(message, builder)