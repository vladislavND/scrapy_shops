from aiogram import types
from aiogram.dispatcher import FSMContext


async def update_inline_keyboard(callback_data: str, state: FSMContext) -> types.InlineKeyboardMarkup:
    keyboards = await state.get_data()
    keyboard = keyboards['spiders']
    buttons = []
    for button in keyboard:
        if button == callback_data:
            buttons.append(button.replace('□', '✅'))
        if button != callback_data:
            buttons.append(button)
    btn_text = ((value, value) for value in buttons)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    start_button = types.InlineKeyboardButton(text='Запустить парсинг', callback_data='scrapy_start')
    async with state.proxy() as data:
        data['spiders'] = buttons
    keyboard_markup.add(*btn)
    keyboard_markup.add(start_button)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)


def clear_button(buttons: list) -> list:
    clear_buttons = []
    for button in buttons:
        if '✅' in button:
            clear_buttons.append(button.replace('✅ ', ''))

    return clear_buttons


def to_string(data) -> str:
    msg = f"Наименование: {data.get('name')}\nЦена: {data.get('price')}\nМагазин: {data.get('shop')}\n" \
          f"Артикул: {data.get('article')}\nUrl: {data.get('url')}\nЦена со скидкой: {data.get('sale_price')}\n" \
          f"Разница в цене: {data.get('different_price')}"
    return msg



