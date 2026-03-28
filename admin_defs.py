from aiogram import types, Router, F


admin_rt = Router()

@admin_rt.message(F.text == '/logs')
async def logs_def(message: types.Message):
    if str(message.from_user.id) != '5220142834': 
        await message.answer('На жаль, у вас немає доступу до команди.')
        return
    await message.answer(text='Готую логі..')
    await message.answer_document(document=types.FSInputFile('debug.txt'))