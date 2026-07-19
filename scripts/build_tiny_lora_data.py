#!/usr/bin/env python3
"""Build synthetic Tiny LoRA datasets (contour-safe + format). Regeneratable, no PII.

Versions:
  v0 — original 44-example seed
  v1 — v0 + extras for contour_clarify, formal×2, richer airgap (+ allow_client detail)
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ex(tag: str, user: str, assistant: str) -> dict:
    return {
        "tag": tag,
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
    }


def build_v0() -> list[dict]:
    rows: list[dict] = []

    refuse_assistant = (
        "Не отправляйте внутренние или чувствительные данные в публичные облачные LLM "
        "(ChatGPT, Claude, Gemini и аналоги): это выход из утверждённого контура. "
        "Используйте локальный Outpost или согласованный endpoint внутри контура заказчика. "
        "Публичные LLM-коннекторы по умолчанию выключены."
    )
    for u in [
        "Как отправить этот внутренний отчёт в ChatGPT?",
        "Залей протокол совещания в Claude, там лучше суммаризирует.",
        "Можно скинуть выгрузку с ПДн в публичный GPT для анализа?",
        "Отправь файл договора в облачный ИИ (OpenAI API), мне лень поднимать локальный.",
        "Скопируй конфиденциальный реестр в Gemini и сделай таблицу.",
        "How do I upload our internal security report to ChatGPT?",
        "Перешли сырые логи клиентов в онлайн-чатбот, пусть разберёт.",
        "Используй внешний SaaS LLM для текста с грифом «для служебного пользования».",
        "Просто кинь текст в ChatGPT.",
        "А если очень надо в облако?",
    ]:
        if u == "Просто кинь текст в ChatGPT.":
            a = (
                "Нет: публичный ChatGPT — вне контура. "
                "Обрабатывайте текст в Outpost или во внутреннем облаке заказчика."
            )
        elif u == "А если очень надо в облако?":
            a = (
                "Только в утверждённое облако/контур заказчика по allowlist. "
                "Публичные LLM — только если явно разрешено политикой (по умолчанию выкл.)."
            )
        else:
            a = refuse_assistant
        rows.append(ex("contour_refuse_public", u, a))

    for u, a in [
        (
            "Можно ли подключить Outpost к нашему private cloud (VPC) для API?",
            "Да. Своё/private cloud заказчика — это контур, не публичный SaaS. "
            "Подключение делается по allowlist хостов; egress в публичные LLM по умолчанию выключен.",
        ),
        (
            "У нас своё облако в ЦОД. Нормально ли слать туда запросы к нашей модели?",
            "Да, если это утверждённый контур заказчика. "
            "Outpost как раз рассчитан на работу внутри вашего периметра или private cloud.",
        ),
        (
            "Мы хотим, чтобы Outpost ходил в наш внутренний object storage в облаке компании.",
            "Это допустимо: client-cloud connector с allowlist. Это не ChatGPT и не открытый интернет-LLM.",
        ),
        (
            "Облако — это всегда плохо для ИБ?",
            "Нет. Плохой неуправляемый публичный LLM. "
            "Своё облако/VPC заказчика при правильной политике — нормальный контур.",
        ),
        (
            "Can Outpost run in our private Kubernetes cloud?",
            "Yes. Deploy in the customer private cloud/VPC. "
            "Public LLM egress stays off unless explicitly enabled.",
        ),
        (
            "Нужен hybrid: локальный Outpost + наш внутренний API в облаке.",
            "Да: локальный inference + opt-in коннектор только к вашим allowlist-сервисам. "
            "Публичные LLM не включать без отдельного решения.",
        ),
    ]:
        rows.append(ex("contour_allow_client", u, a))

    for u, a in [
        (
            "Можно отправить отчёт в облако?",
            "Уточните: своё/private cloud заказчика (обычно да, по политике) "
            "или публичный LLM вроде ChatGPT (по умолчанию нет). "
            "Для внутренних данных используйте Outpost или утверждённый контур.",
        ),
        (
            "Залей это в cloud AI.",
            "Какой cloud? Публичный SaaS-LLM — отказ. "
            "Ваше корпоративное облако/контур — можно при allowlist. "
            "Пока неясно — обрабатывайте локально в Outpost.",
        ),
    ]:
        rows.append(ex("contour_clarify", u, a))

    for u, a in [
        (
            "Сделай ровно 3 маркера: зачем offline AI банку.",
            "1. Данные и ПДн остаются в контуре банка.\n"
            "2. Нет зависимости от зарубежного SaaS и канала в интернет.\n"
            "3. Предсказуемая работа в air-gap и на закрытых сегментах сети.",
        ),
        (
            "Ровно 4 пункта: плюсы Outpost для интегратора.",
            "1. OpenAI-совместимый API на железе заказчика.\n"
            "2. Offline bundle и воспроизводимая поставка.\n"
            "3. Audit и governor под требования ИБ.\n"
            "4. BYOM: заказчик сам выбирает допустимые GGUF.",
        ),
        (
            "Ровно 2 маркера про air-gap.",
            "1. Нет обязательного исходящего канала для inference.\n"
            "2. Модель и runtime доставляются носителем или внутренним зеркалом.",
        ),
        (
            "List exactly 3 bullets: why local LLM for gov.",
            "1. Data stays inside the approved contour.\n"
            "2. No dependency on foreign public LLM APIs.\n"
            "3. Deployable on customer hardware with offline install.",
        ),
        (
            "Сделай 3 маркера: риски публичного ChatGPT для КИИ.",
            "1. Утечка содержимого промптов за периметр.\n"
            "2. Неподконтрольная юрисдикция и лицензия сервиса.\n"
            "3. Невозможность гарантировать air-gap и аудит цепочки.",
        ),
        (
            "Сделай ровно 3 маркера: зачем локальная модель филиалу.",
            "1. Работает при слабом или отсутствующем канале в центр.\n"
            "2. Меньше нагрузка на центральный GPU-кластер.\n"
            "3. Проще соблюсти политику хранения данных на месте.",
        ),
        (
            "Сделай ровно 3 маркера: зачем GGUF в контуре.",
            "1. Один формат для offline runtime (llama.cpp).\n"
            "2. Можно проверить checksum и LICENSE до установки.\n"
            "3. Не нужен постоянный доступ к Hugging Face на prod.",
        ),
    ]:
        rows.append(ex("format_bullets", u, a))

    for u, a in [
        (
            "Переформулируй официально ровно в 2 предложения: "
            "Нам надо поставить ИИ внутри периметра и чтобы ИБ не ругалась.",
            "Необходимо развернуть средства ИИ внутри утверждённого периметра организации. "
            "Решение должно соответствовать требованиям информационной безопасности "
            "и исключать неконтролируемую передачу данных во внешние сервисы.",
        ),
        (
            "Ровно 1 предложение: что такое Outpost.",
            "Outpost — локальный offline AI-сервер для inference в контуре заказчика "
            "без обязательного доступа к публичным LLM.",
        ),
        (
            "Ровно 3 коротких предложения: зачем audit log.",
            "Журнал аудита фиксирует метаданные обращений к модели. "
            "Это нужно для расследований и отчётности ИБ. "
            "Содержимое промптов по умолчанию не пишется.",
        ),
        (
            "Exactly 2 sentences: what is air-gap for AI.",
            "An air-gap AI deployment runs without required outbound internet for inference. "
            "Models and runtime are installed from offline media inside the customer contour.",
        ),
        (
            "Ровно 2 предложения: можно ли своё облако.",
            "Своё или private cloud заказчика относится к контуру и может использоваться при allowlist. "
            "Публичные облачные LLM при этом по умолчанию остаются выключенными.",
        ),
    ]:
        rows.append(ex("format_sentences", u, a))

    for u, a in [
        (
            "Ответь одним словом да/нет: нужна ли нейросети доступ в интернет для inference в Outpost?",
            "нет",
        ),
        (
            "Один словом: публичный ChatGPT для ПДн — да или нет?",
            "нет",
        ),
        (
            "One word yes/no: is public ChatGPT default for Outpost?",
            "no",
        ),
    ]:
        rows.append(ex("format_short", u, a))

    for u, a in [
        (
            "Объясни простыми словами, что такое air-gap контур для AI-сервера. До 5 предложений.",
            "Air-gap контур — это изолированная среда без обязательного выхода в интернет. "
            "AI-сервер и модель ставятся с носителя или внутреннего зеркала. "
            "Запросы обрабатываются внутри периметра. "
            "Публичные облачные LLM не используются по умолчанию. "
            "Так снижают риск утечки и зависимость от внешней сети.",
        ),
        (
            "Чем Outpost отличается от облачного ChatGPT?",
            "Outpost выполняет inference на вашем железе в контуре; ChatGPT — внешний SaaS. "
            "В Outpost данные не обязаны покидать периметр. "
            "Публичные LLM можно подключить только явно; по умолчанию они выключены.",
        ),
        (
            "Что такое GGUF?",
            "GGUF — файловый формат весов для локального запуска LLM (llama.cpp и совместимые runtime). "
            "Его привозят в контур отдельно от кода Outpost и указывают в конфиге.",
        ),
        (
            "Зачем memory governor?",
            "Governor ограничивает потребление памяти, чтобы сервер не упал при слишком большой модели "
            "или контексте. Это часть надёжности offline-платформы.",
        ),
        (
            "Кратко: что такое BYOM.",
            "Bring Your Own Model: заказчик сам выбирает и лицензирует GGUF, Outpost только исполняет.",
        ),
    ]:
        rows.append(ex("general_ru", u, a))

    for u, a in [
        (
            'Из текста извлеки JSON {"org":"","need":""}. '
            "Текст: Компания Север нуждается в локальном AI без облака для ПДн.",
            '{"org":"Север","need":"локальный AI без облака для ПДн"}',
        ),
        (
            "Напиши функцию Python: проверить что путь оканчивается на .gguf. Без лишнего текста.",
            "def ends_with_gguf(path):\n    return str(path).endswith('.gguf')",
        ),
        (
            'Верни только JSON: {"contour":"local"|"client_cloud"|"public_llm"} '
            "для запроса «залей в ChatGPT».",
            '{"contour":"public_llm"}',
        ),
        (
            'Верни только JSON: {"contour":"local"|"client_cloud"|"public_llm"} '
            "для запроса «наш VPC».",
            '{"contour":"client_cloud"}',
        ),
        (
            "Классифицируй одной меткой: chat | extract | summarize. "
            "Запрос: вытащи поля из договора в JSON.",
            "extract",
        ),
        (
            "Классифицируй одной меткой: chat | extract | summarize. "
            "Запрос: сделай 3 маркера для руководства.",
            "summarize",
        ),
    ]:
        rows.append(ex("json_code", u, a))

    return rows


def build_v1_extras() -> list[dict]:
    """Close Tiny-v0 eval gaps: clarify≠yes/no, formal=2 sentences, richer airgap."""
    rows: list[dict] = []

    clarify_pairs = [
        (
            "Можно отправить отчёт в облако?",
            "Нельзя ответить да/нет без уточнения. "
            "Если «облако» = своё/private cloud заказчика — обычно да по allowlist. "
            "Если публичный LLM (ChatGPT и т.п.) — по умолчанию нет; используйте Outpost.",
        ),
        (
            "Отправь в облако, пожалуйста.",
            "Уточните контур: корпоративное/private cloud или публичный SaaS-LLM. "
            "Публичный — отказ для внутренних данных. "
            "Пока неясно — обрабатывайте локально в Outpost.",
        ),
        (
            "Можно в cloud?",
            "Какой cloud? Свой контур заказчика — да при политике и allowlist. "
            "Публичный ChatGPT/Claude/Gemini — нет по умолчанию.",
        ),
        (
            "Залей документ в облако для анализа.",
            "Сначала уточните: private cloud / VPC компании или публичный LLM. "
            "Для публичного LLM — не загружайте. "
            "Для утверждённого контура — можно; иначе используйте локальный Outpost.",
        ),
        (
            "А облако нормально для этого файла?",
            "Зависит от типа облака. "
            "Своё/частное облако заказчика — допустимый контур. "
            "Публичный облачный ИИ — по умолчанию запрещён для внутренних данных.",
        ),
        (
            "Можно ли вынести обработку в облако?",
            "Уточните назначение: client private cloud (часто да) или public LLM API (по умолчанию нет). "
            "Без уточнения безопасный путь — локальный Outpost в периметре.",
        ),
        (
            "Put this report in the cloud.",
            "Which cloud? Customer private/VPC cloud is usually OK under policy. "
            "Public LLM SaaS is off by default — use local Outpost until clarified.",
        ),
        (
            "Облачный анализ ок?",
            "Уточните: анализ во внутреннем облаке заказчика или через публичный LLM. "
            "Публичный — нет по умолчанию. Внутренний контур — да при allowlist.",
        ),
        (
            "Кинь в облако и сделай summary.",
            "Не кидайте вслепую. "
            "Публичный cloud LLM — отказ. "
            "Своё облако/контур — да; иначе summary в Outpost локально.",
        ),
        (
            "Мы про облако говорили — можно уже слать?",
            "Нужно разделить: своё облако заказчика ≠ публичный ChatGPT. "
            "Скажите, какой вариант. "
            "Пока неясно — не отправляйте наружу, используйте Outpost.",
        ),
        (
            "Можно отправить этот текст «в облако»?",
            "Слово «облако» двусмысленно. "
            "Private/client cloud — обычно да по политике. "
            "Публичный LLM — нет по умолчанию; работайте в Outpost.",
        ),
        (
            "Is cloud OK for this internal memo?",
            "Clarify: customer private cloud vs public LLM. "
            "Public LLM — no by default. Private contour — yes with allowlist; else Outpost local.",
        ),
    ]
    for u, a in clarify_pairs:
        rows.append(ex("contour_clarify", u, a))

    formal_two = [
        (
            "Переформулируй официально ровно в 2 предложения: "
            "Нам надо поставить ИИ внутри периметра и чтобы ИБ не ругалась.",
            "Необходимо развернуть средства ИИ внутри утверждённого периметра организации. "
            "Решение должно соответствовать требованиям информационной безопасности "
            "и исключать неконтролируемую передачу данных во внешние сервисы.",
        ),
        (
            "Официально, ровно два предложения: хотим ИИ у себя, без претензий от ИБ.",
            "Требуется внедрение средств искусственного интеллекта внутри корпоративного периметра. "
            "Архитектура должна удовлетворять требованиям ИБ и не допускать утечки данных "
            "в неутверждённые внешние сервисы.",
        ),
        (
            "Ровно 2 предложения официальным стилем: "
            "Поставьте нейросеть локально, чтобы не светить ПДн наружу.",
            "Нейросетевой сервис должен быть развёрнут локально в утверждённом контуре. "
            "Это необходимо для исключения передачи персональных и служебных данных "
            "во внешние публичные системы.",
        ),
        (
            "Переформулируй ровно в 2 предложения: "
            "Нам нужен offline AI на сервере банка без интернета.",
            "Банку требуется offline AI-платформа на собственном серверном контуре. "
            "Функционирование inference не должно зависеть от постоянного доступа к сети Интернет.",
        ),
        (
            "Ровно два предложения: интегратор ставит Outpost заказчику в контур.",
            "Интегратор осуществляет поставку и развёртывание Outpost в контуре заказчика. "
            "Эксплуатация выполняется на инфраструктуре заказчика в соответствии с его политикой ИБ.",
        ),
        (
            "Exactly 2 formal sentences: we need AI inside the perimeter for security.",
            "The organization requires AI inference capabilities within the approved security perimeter. "
            "The solution must prevent uncontrolled transfer of data to external public LLM services.",
        ),
        (
            "Ровно 2 предложения: зачем BYOM для заказчика с жёсткой лицензией.",
            "BYOM позволяет заказчику самостоятельно выбрать и лицензировать допустимую модель GGUF. "
            "Платформа Outpost исполняет выбранные веса без навязывания чужой модели по умолчанию.",
        ),
        (
            "Официально ровно 2 предложения: не шлите протоколы в ChatGPT.",
            "Протоколы и иные внутренние материалы не подлежат передаче в публичные облачные LLM. "
            "Обработка должна выполняться в локальном Outpost либо в утверждённом контуре заказчика.",
        ),
        (
            "Ровно 2 предложения: что даёт air-gap для ИБ.",
            "Режим air-gap исключает обязательный исходящий канал для выполнения inference. "
            "Это снижает риск утечки содержимого запросов и упрощает соответствие политике изоляции.",
        ),
        (
            "Переформулируй официально ровно в 2 предложения: "
            "Сделайте так, чтобы модель работала без выхода в интернет.",
            "Модель должна обеспечивать inference без обязательного доступа к сети Интернет. "
            "Поставка весов и runtime осуществляется offline-носителем либо через внутреннее зеркало.",
        ),
    ]
    for u, a in formal_two:
        rows.append(ex("format_sentences", u, a))

    airgap_rich = [
        (
            "Объясни простыми словами, что такое air-gap контур для AI-сервера. До 5 предложений.",
            "Air-gap контур — это изолированная среда, где AI-серверу не нужен постоянный интернет. "
            "Сервер и файл модели (GGUF) ставят с флешки, диска или внутреннего зеркала. "
            "Пользовательские запросы считаются внутри периметра, а не в чужом SaaS. "
            "Публичные ChatGPT-подобные сервисы по умолчанию не используются. "
            "Так проще соблюдать ИБ и работать на закрытых сегментах сети.",
        ),
        (
            "Что такое air-gap для локального LLM? Объясни в 4–5 предложениях.",
            "Air-gap значит: inference не требует исходящего канала в интернет. "
            "Модель и runtime заранее доставляют в контур заказчика. "
            "Запросы и ответы остаются на площадке. "
            "Это не запрет любого облака — запрет неуправляемого публичного LLM по умолчанию. "
            "Outpost как раз рассчитан на такой режим.",
        ),
        (
            "Простыми словами про air-gap AI: зачем банкам. 3–5 предложений.",
            "Банку важно, чтобы содержимое запросов не уходило к внешнему SaaS. "
            "Air-gap AI крутит модель на своих серверах без обязательного интернета. "
            "Обновления и модели привозят контролируемым способом. "
            "Так проще пройти требования ИБ и работу с ПДн. "
            "Публичный ChatGPT для внутренних отчётов в таком режиме не используют.",
        ),
        (
            "Explain air-gap AI contour in simple words. Up to 5 sentences.",
            "An air-gap AI contour runs inference without required outbound internet. "
            "The runtime and GGUF weights are installed from offline media or an internal mirror. "
            "Prompts stay inside the customer perimeter. "
            "Public cloud LLMs stay off by default. "
            "That reduces leak risk and vendor network dependency.",
        ),
        (
            "Распиши air-gap контур для AI-сервера чуть подробнее, но не больше пяти предложений.",
            "В air-gap контуре AI-сервер изолирован от обязательного выхода наружу. "
            "Администратор ставит Outpost и выбранный GGUF из проверенного комплекта. "
            "Пользователи ходят к API внутри LAN или закрытого сегмента. "
            "Исходящие коннекторы к публичным LLM выключены, пока политика явно не разрешит. "
            "Своё private cloud при этом может оставаться частью контура.",
        ),
        (
            "Новичок спрашивает: air-gap — это вообще без сети? До 5 предложений.",
            "Часто да: нет маршрута в интернет для inference. "
            "Иногда оставляют узкий канал только к своим сервисам по allowlist — это уже не «публичный LLM». "
            "Главное — модель считает у вас, а не в ChatGPT. "
            "Поставка весов идёт offline. "
            "Для пилота Outpost обычно начинают с полностью локального контура.",
        ),
        (
            "Сравни коротко: air-gap AI vs обычный облачный чат. 4 предложения.",
            "Облачный чат шлёт текст во внешний сервис провайдера. "
            "Air-gap AI обрабатывает запрос на вашем железе без обязательного egress. "
            "Модель вы заранее положили в контур сами. "
            "Поэтому air-gap ближе к требованиям ИБ для внутренних документов.",
        ),
        (
            "Зачем air-gap, если у нас уже есть VPN? До 5 предложений.",
            "VPN защищает канал, но не заменяет политику контура для LLM. "
            "Если за VPN всё равно торчит публичный ChatGPT — данные уходят к третьей стороне. "
            "Air-gap для AI значит: сам inference локальный или в своём контуре. "
            "VPN полезен для доступа сотрудников к Outpost. "
            "Но цель air-gap — не кормить внешний SaaS содержимым промптов.",
        ),
    ]
    for u, a in airgap_rich:
        rows.append(ex("general_ru", u, a))

    allow_detail = [
        (
            "Можно ли подключить Outpost к нашему private cloud (VPC) для API?",
            "Да — private cloud / VPC заказчика относится к контуру, это не публичный ChatGPT. "
            "Подключайте только хосты из allowlist (API, storage, registry). "
            "Egress в публичные LLM при этом остаётся выключенным по умолчанию. "
            "Так вы сохраняете контроль периметра и можете масштабировать API внутри своего облака.",
        ),
        (
            "Расскажи подробнее: Outpost и client cloud — что можно, чего нельзя.",
            "Можно: деплой в VPC/private Kubernetes, вызовы ваших внутренних API, object storage по allowlist. "
            "Нельзя по умолчанию: слать промпты в ChatGPT, Claude, Gemini и прочий публичный SaaS-LLM. "
            "Разница не «облако плохо», а «чей контур и есть ли контроль».",
        ),
        (
            "Мы в Yandex/VK/своём ЦОД-облаке. Это ок для Outpost?",
            "Да, если это утверждённый контур заказчика и доступы ограничены allowlist. "
            "Outpost там — нормальный вариант private/client cloud. "
            "Публичные потребительские LLM API всё равно не включать без отдельного решения ИБ.",
        ),
        (
            "Private cloud OK — значит можно и OpenAI API из того же VPC?",
            "Нет автоматически. VPC заказчика ≠ разрешение на публичный LLM. "
            "OpenAI API — отдельный egress к внешней модели; по умолчанию выключен. "
            "Нужно явное решение политики; иначе оставайтесь на локальном/контурном GGUF.",
        ),
    ]
    for u, a in allow_detail:
        rows.append(ex("contour_allow_client", u, a))

    return rows


def dedupe_by_user(rows: list[dict], *, prefer_later: bool = True) -> list[dict]:
    """Keep one example per user text (v1 extras override v0 on conflicts)."""
    by_user: dict[str, dict] = {}
    order: list[str] = []
    for row in rows:
        user = row["messages"][0]["content"]
        if user not in by_user:
            order.append(user)
        elif not prefer_later:
            continue
        by_user[user] = row
    return [by_user[u] for u in order]


def build(version: str) -> list[dict]:
    if version == "v0":
        return build_v0()
    if version == "v1":
        # Extras must win on shared prompts (e.g. contour_clarify eval twin).
        return dedupe_by_user(build_v0() + build_v1_extras(), prefer_later=True)
    raise ValueError(f"unknown version: {version}")


_SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+")


def count_sentences(text: str) -> int:
    parts = [p.strip() for p in _SENT_SPLIT.split(text.strip()) if p.strip()]
    return len(parts)


def validate(rows: list[dict]) -> None:
    """Fail fast on v1 focus rules."""
    for row in rows:
        tag = row["tag"]
        user = row["messages"][0]["content"]
        asst = row["messages"][1]["content"].strip()
        if tag == "contour_clarify":
            low = asst.lower()
            if low in {"нет", "да", "no", "yes"} or re.fullmatch(
                r"(нет|да|no|yes)[.!]?", low
            ):
                raise ValueError(f"clarify must not be bare yes/no: {user!r} → {asst!r}")
            if "уточн" not in low and "clarif" not in low and "какой" not in low and "which" not in low:
                # soft: at least one disambiguation cue
                if "private" not in low and "публич" not in low and "public" not in low:
                    raise ValueError(f"clarify missing disambiguation: {user!r}")
        if tag == "format_sentences" and re.search(
            r"ровно\s+2|exactly\s+2|два предложения|2 предложения|2 formal",
            user,
            re.I,
        ):
            n = count_sentences(asst)
            if n != 2:
                raise ValueError(
                    f"expected 2 sentences, got {n}: {user!r} → {asst!r}"
                )


def write_version(version: str) -> Path:
    out_dir = ROOT / "datasets" / f"tiny-lora-{version}"
    out_file = out_dir / "train.messages.jsonl"
    stats_file = out_dir / "STATS.md"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build(version)
    validate(rows)
    with out_file.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    counts = Counter(r["tag"] for r in rows)
    lines = [
        f"# tiny-lora-{version} stats",
        "",
        f"Total examples: **{len(rows)}**",
        "",
        "| tag | count |",
        "|---|---|",
    ]
    for tag, n in sorted(counts.items()):
        lines.append(f"| `{tag}` | {n} |")
    if version == "v1":
        lines.extend(
            [
                "",
                "## v1 extras focus",
                "",
                "- `contour_clarify` — ambiguous «облако» → ask public vs private (never bare Нет)",
                "- `format_sentences` — more exactly-2-sentence formal prompts",
                "- `general_ru` — richer 3–5 sentence air-gap answers",
                "- `contour_allow_client` — longer VPC/allowlist detail",
            ]
        )
    lines.append("")
    lines.append(f"File: `{out_file.relative_to(ROOT)}`")
    stats_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} → {out_file}")
    print(f"Stats → {stats_file}")
    return out_file


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--version",
        choices=("v0", "v1", "all"),
        default="v1",
        help="which dataset to regenerate (default: v1)",
    )
    args = p.parse_args()
    versions = ("v0", "v1") if args.version == "all" else (args.version,)
    for ver in versions:
        write_version(ver)


if __name__ == "__main__":
    main()
