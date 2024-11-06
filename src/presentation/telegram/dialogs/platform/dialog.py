from aiogram import F

from aiogram_dialog import Dialog, Window, LaunchMode, ShowMode
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import (
    StubScroll,
    Column,
    Select,
    PrevPage,
    CurrentPage,
    NextPage,
    SwitchTo,
    Button,
    Row,
    Start,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiogram_dialog.widgets.media import DynamicMedia

from src.presentation.telegram.states.platform import PlatformManagementSG
from src.presentation.telegram.states.platform_products import PlatformProductManagementSG
from src.presentation.telegram.dialogs.platform.getter import (
    platform_list_getter,
    one_platform_getter,
    login_data_fields_getter,
)
from src.presentation.telegram.dialogs.platform.handlers import on_selected_platform
from src.presentation.telegram.dialogs.platform.handlers import (
    delete_platform,
    on_edit_platform_image,
    on_edit_platform_web_place,
    on_edit_platform_description,
    on_edit_platform_name,
    remove_login_field,
    add_login_field,
    on_new_platform_name,
    on_new_platform_description,
    on_new_platform_login_data,
    on_new_platform_image,
    email_password_login_data,
    start_platform_products,
)


PLATFORM_LIST_BACK_BTN = SwitchTo(
    Const("◀️ Назад"),
    id="platform_list",
    state=PlatformManagementSG.PLATFORM_LIST,
    show_mode=ShowMode.EDIT,
)


platform_dialog = Dialog(
    Window(
        Const('Список сервисов', when=F["platforms"]),
        Const("Список сервисов пуст", when=~F["platforms"]),
        StubScroll(id="scroll", pages=F["pages"]),
        Column(
            Select(
                Format("{item.name}"),
                item_id_getter=lambda item: item.platform_id,
                type_factory=lambda x: int(x),
                items="platforms",
                on_click=on_selected_platform,
                id="list",
            ),
        ),
        SwitchTo(
            Const("➕ Добавить сервис"),
            id="add_platform",
            state=PlatformManagementSG.ADD_PLATFORM_NAME,
        ),
        Row(
            PrevPage(
                scroll="scroll", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="scroll", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="scroll", text=Format("▶️"),
            ),
            when=F["platforms"] & (F["pages"] > 1),
        ),
        getter=platform_list_getter,  # type: ignore
        state=PlatformManagementSG.PLATFORM_LIST,
    ),
    Window(
        DynamicMedia(selector="photo"),
        Format("{text}"),
        SwitchTo(
            Const("✏️ Изменить"),
            id="edit_platform",
            state=PlatformManagementSG.PLATFORM_INFO,
        ),
        Button(
            Const("🛒 Товары сервиса"),
            id="platform_products",
            on_click=start_platform_products,
        ),
        Button(
            id="delete_platform",
            text=Const("❌ Удалить"),
            on_click=delete_platform,
        ),
        PLATFORM_LIST_BACK_BTN,
        getter=one_platform_getter,  # type: ignore
        state=PlatformManagementSG.PLATFORM,
    ),
    Window(
        DynamicMedia(selector="photo"),
        Format("{text}"),
        Row(
            SwitchTo(
                Const("Название"),
                id="edit_name",
                state=PlatformManagementSG.EDIT_NAME,
            ),
            SwitchTo(
                Const("Описание"),
                id="edit_description", 
                state=PlatformManagementSG.EDIT_DESCRIPTION,
            ),
        ),
        Row(
            SwitchTo(
                Const("Web place"),
                id="edit_web_app_place",
                state=PlatformManagementSG.EDIT_WEB_APP_PLACE,
            ),
            SwitchTo(
                Const("Изображение"),
                id="edit_image",
                state=PlatformManagementSG.EDIT_IMAGE,
            ),
        ),
        SwitchTo(
            Const("Поля логина"),
            id="edit_login_data",
            state=PlatformManagementSG.EDIT_LOGIN_DATA,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_platform",
            state=PlatformManagementSG.PLATFORM,
        ),
        getter=one_platform_getter,  # type: ignore
        state=PlatformManagementSG.PLATFORM_INFO,
    ),
    Window(
        Const("Введите новое имя:"),
        TextInput(
            id="name",
            on_success=on_edit_platform_name,
            type_factory=str,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformManagementSG.PLATFORM_INFO,
        ),
        state=PlatformManagementSG.EDIT_NAME,
    ),
    Window(
        Const("Введите новое описание:"),
        TextInput(
            id="description",
            on_success=on_edit_platform_description,
            type_factory=str,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformManagementSG.PLATFORM_INFO,
        ),
        state=PlatformManagementSG.EDIT_DESCRIPTION,
    ),
    Window(
        Const("Введите новое место на сайте:"),
        TextInput(
            id="web_place",
            on_success=on_edit_platform_web_place,
            type_factory=lambda x: int(x),
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformManagementSG.PLATFORM_INFO,
        ),
        state=PlatformManagementSG.EDIT_WEB_APP_PLACE,
    ),
    Window(
        Const("Отправьте новое изображение:"),
        MessageInput(
            func=on_edit_platform_image,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformManagementSG.PLATFORM_INFO,
        ),
        state=PlatformManagementSG.EDIT_IMAGE,
    ),
    Window(
        Multi(
            Const("Поля для логина:"),
            Const("<i>Для удаления поля просто нажмите на него</i>"),
            sep="\n",
            when=F["login_data"],
        ),
        Const("Полей для логина нет", when=~F["login_data"]),
        ScrollingGroup(
            Select(
                id="login_field",
                items="login_data",
                item_id_getter=lambda item: item,
                text=Format("{item}"),
                on_click=remove_login_field,
            ),
            id="login_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True,
            when="login_data"
        ),
        SwitchTo(
            id="add_login_field",
            text=Const("➕ Добавить поле"),
            state=PlatformManagementSG.ADD_LOGIN_FIELD,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformManagementSG.PLATFORM_INFO,
        ),
        getter=login_data_fields_getter,  # type: ignore
        state=PlatformManagementSG.EDIT_LOGIN_DATA,
    ),
    Window(
        Const("Введите название поля:"),
        TextInput(
            id="login_field",
            on_success=add_login_field,
            type_factory=str,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_login_data",
            state=PlatformManagementSG.EDIT_LOGIN_DATA,
        ),
        state=PlatformManagementSG.ADD_LOGIN_FIELD,
    ),
    Window(
        Const("Введите название сервиса:"),
        TextInput(
            id="name",
            on_success=on_new_platform_name,
            type_factory=str,
        ),
        state=PlatformManagementSG.ADD_PLATFORM_NAME,
    ),
    Window(
        Const("Введите описание:"),
        TextInput(
            id="description",
            on_success=on_new_platform_description,
            type_factory=str,
        ),
        state=PlatformManagementSG.ADD_PLATFORM_DESCRIPTION,
    ),
    Window(
        Const("Введите поля логина, через запятую:"),
        TextInput(
            id="login_data",
            on_success=on_new_platform_login_data,
            type_factory=str,
        ),
        Button(
            Const("Почта + пароль"),
            id="skip_login_data",
            on_click=email_password_login_data,
        ),
        state=PlatformManagementSG.ADD_PLATFORM_LOGIN_DATA,
    ),
    Window(
        Const("Отправьте изображение:"),
        MessageInput(
            func=on_new_platform_image,
        ),
        state=PlatformManagementSG.ADD_PLATFORM_IMAGE,
    ),
    launch_mode=LaunchMode.ROOT,
)
