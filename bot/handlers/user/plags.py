from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router(name=__name__)

not_implemented = [
    'report_client_for_admin', 'get_bonus',
    #'report_for_adm', 
    'TODO',
    'reports_for_extra', 'admin_reports',
    'admin_service_catalog', 'change_unit_services'
]


@router.callback_query(F.data.in_(iterable=not_implemented))
async def plugs(
    callback: CallbackQuery,
):
    await callback.bot.send_sticker(
        chat_id=callback.from_user.id,
        sticker='CAACAgIAAxkBAAEE5ApmJWuVg0DS5KY29U'
                'TbBOHOKFzqLAAChhQAAmKy8EsG14-Zws0O-TQE'
    )
    await callback.message.answer(
        text=('Мы не успели это сделать, не бейте нас😭'
              '\nИ нажмите кнопку /start')
    )
