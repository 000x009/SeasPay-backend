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
    Row,
    Url,
    Button,
)
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import DynamicMedia

from src.presentation.telegram.dialogs.platform_product.getter import platform_product_getter, get_platform_product_getter
from src.presentation.telegram.states.platform_products import PlatformProductManagementSG
from src.presentation.telegram.dialogs.platform_product.handlers import (
    on_selected_product,
    delete_platform_product,
    on_edit_platform_product_name,
    on_edit_platform_product_instruction,
    on_edit_platform_product_purchase_url,
    on_edit_platform_product_image,
    on_edit_platform_product_price,
    on_new_platform_product_name,
    on_new_platform_product_instruction,
    on_new_platform_product_purchase_url,
    on_new_platform_product_price,
    on_new_platform_product_image,
    back_to_platform,
)



platform_product_dialog = Dialog(
    Window(
        Const("Продукты сервиса:", when=F["products"]),
        Const("Список продуктов пуст...", when=~F["products"]),
        StubScroll(id="scroll", pages=F["pages"]),
        Column(
            Select(
                Format("{item.name}"),
                item_id_getter=lambda item: item.id,
                type_factory=lambda x: int(x),
                items="products",
                on_click=on_selected_product,
                id="list",
            ),
        ),
        SwitchTo(
            Const("➕ Добавить продукт"),
            id="add_product",
            state=PlatformProductManagementSG.ADD_PRODUCT_NAME,
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
            when=F["products"] & (F["pages"] > 1),
        ),
        Button(
            id="back_to_platform",
            text=Const("◀️ Назад"),
            on_click=back_to_platform,
        ),
        getter=platform_product_getter,  # type: ignore
        state=PlatformProductManagementSG.PRODUCT_LIST,
    ),
    Window(
        DynamicMedia(selector="photo", when="photo"),
        Format("{text}"),
        Url(
            id="purchase_url",
            text=Const("Перейти к товару"),
            url=Format("{product.purchase_url}"),
        ),
        SwitchTo(
            Const("✏️ Изменить"),
            id="edit_platform_product",
            state=PlatformProductManagementSG.EDIT_PRODUCT,
        ),
        Button(
            id="delete_platform_product",
            text=Const("❌ Удалить"),
            on_click=delete_platform_product,
        ),
        state=PlatformProductManagementSG.PRODUCT,
        getter=get_platform_product_getter,  # type: ignore
    ),
    Window(
        DynamicMedia(selector="photo"),
        Format("{text}"),
        Row(
            SwitchTo(
                Const("Название"),
                id="edit_name",
                state=PlatformProductManagementSG.EDIT_PRODUCT_NAME,
            ),
            SwitchTo(
                Const("Инструкция по покупке"),
                id="edit_instruction", 
                state=PlatformProductManagementSG.EDIT_PRODUCT_INSTRUCTION,
            ),
        ),
        Row(
            SwitchTo(
                Const("Цена"),
                id="edit_price",
                state=PlatformProductManagementSG.EDIT_PRODUCT_PRICE,
            ),
            SwitchTo(
                Const("Изображение"),
                id="edit_image",
                state=PlatformProductManagementSG.EDIT_PRODUCT_IMAGE,
            ),
        ),
        SwitchTo(
            Const("URL покупки"),
            id="edit_purchase_url",
            state=PlatformProductManagementSG.EDIT_PRODUCT_PURCHASE_URL,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_platform_product",
            state=PlatformProductManagementSG.PRODUCT,
        ),
        getter=get_platform_product_getter,  # type: ignore
        state=PlatformProductManagementSG.EDIT_PRODUCT,
    ),
    Window(
        Const("Введите новое имя:"),
        TextInput(
            id="name",
            on_success=on_edit_platform_product_name,
            type_factory=str,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformProductManagementSG.EDIT_PRODUCT,
        ),
        state=PlatformProductManagementSG.EDIT_PRODUCT_NAME,
    ),
    Window(
        Const("Введите новую инструкцию по покупке:"),
        TextInput(
            id="instruction",
            on_success=on_edit_platform_product_instruction,
            type_factory=str,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformProductManagementSG.EDIT_PRODUCT,
        ),
        state=PlatformProductManagementSG.EDIT_PRODUCT_INSTRUCTION,
    ),
    Window(
        Const("Введите новую ссылку на покупку:"),
        TextInput(
            id="purchase_url",
            on_success=on_edit_platform_product_purchase_url,
            type_factory=str,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformProductManagementSG.EDIT_PRODUCT,
        ),
        state=PlatformProductManagementSG.EDIT_PRODUCT_PURCHASE_URL,
    ),
    Window(
        Const("Отправьте новое изображение:"),
        MessageInput(
            func=on_edit_platform_product_image,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformProductManagementSG.EDIT_PRODUCT,
        ),
        state=PlatformProductManagementSG.EDIT_PRODUCT_IMAGE,
    ),
    Window(
        Const("Введите новую цену:"),
        MessageInput(
            func=on_edit_platform_product_price,
        ),
        SwitchTo(
            Const("◀️ Назад"),
            id="back_to_edit",
            state=PlatformProductManagementSG.EDIT_PRODUCT,
        ),
        state=PlatformProductManagementSG.EDIT_PRODUCT_PRICE,
    ),
    Window(
        Const("Введите название продукта:"),
        TextInput(
            id="name",
            on_success=on_new_platform_product_name,
            type_factory=str,
        ),
        state=PlatformProductManagementSG.ADD_PRODUCT_NAME,
    ),
    Window(
        Const("Введите инструкцию по покупке:"),
        TextInput(
            id="instruction",
            on_success=on_new_platform_product_instruction,
            type_factory=str,
        ),
        state=PlatformProductManagementSG.ADD_PRODUCT_INSTRUCTION,
    ),
    Window(
        Const("Введите ссылку на покупку:"),
        TextInput(
            id="purchase_url",
            on_success=on_new_platform_product_purchase_url,
            type_factory=str,
        ),
        state=PlatformProductManagementSG.ADD_PRODUCT_PURCHASE_URL,
    ),
    Window(
        Const("Введите цену:"),
        TextInput(
            id="price",
            on_success=on_new_platform_product_price,
        ),
        state=PlatformProductManagementSG.ADD_PRODUCT_PRICE,
    ),
    Window(
        Const("Отправьте изображение:"),
        MessageInput(
            func=on_new_platform_product_image,
        ),
        state=PlatformProductManagementSG.ADD_PRODUCT_IMAGE,
    ),
)
