import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from research_text import MABAHITH_DATA, INTRO, CONCLUSION, GLOSSARY, REFERENCES

# قراءة التوكن مباشرة من متغيرات البيئة في Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

QUIZ_DATA = [
    {"q": "ما المنطقة التي ارتبطت بعلاقات تجارية مع مصر الفرعونية؟", "options": ["بلاد بونت", "زيمبابوي", "أثينا"], "correct": 0},
    {"q": "ما الميناء الرئيسي لأكسوم؟", "options": ["الإسكندرية", "أدوليس", "جدة"], "correct": 1},
    {"q": "في عهد أي ملك اعتنقت أكسوم المسيحية؟", "options": ["الملك كالب", "الملك عيزانا", "حتشبسوت"], "correct": 1}
]

# ================== لوحات المفاتيح ==================

def main_menu():
    b = InlineKeyboardBuilder()
    b.button(text="🏛️ ابدأ الرحلة", callback_data="start_journey")
    b.button(text="📚 المباحث", callback_data="explore_sections")
    b.button(text="📜 الخاتمة والنتائج", callback_data="conclusion")
    b.button(text="📖 المصطلحات", callback_data="glossary")
    b.button(text="🗺️ أطلس الحضارات", callback_data="atlas")
    b.button(text="🖼️ معرض الصور", callback_data="gallery")
    b.button(text="⏳ الخط الزمني", callback_data="timeline")
    b.button(text="🎯 اختبر معلوماتك", callback_data="quiz")
    b.button(text="📑 المراجع", callback_data="references")
    b.button(text="ℹ️ حول", callback_data="about")
    b.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    return b.as_markup()

def intro_nav(page, total):
    b = InlineKeyboardBuilder()
    if page > 0: b.button(text="⬅️", callback_data=f"intro:{page-1}")
    if page < total - 1: b.button(text="➡️", callback_data=f"intro:{page+1}")
    b.button(text="⏭️ تخطَّ", callback_data="explore_sections")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(2, 1, 1)
    return b.as_markup()

def sections_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="المبحث الأول: الجذور", callback_data="sec:1")
    b.button(text="المبحث الثاني: أكسوم", callback_data="sec:2")
    b.button(text="المبحث الثالث: المظاهر", callback_data="sec:3")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(1, 1, 1, 1)
    return b.as_markup()

def topic_nav(sec_id, topic_idx, total_topics):
    b = InlineKeyboardBuilder()
    if topic_idx > 0: b.button(text="⬅️ السابق", callback_data=f"topic:{sec_id}:{topic_idx-1}")
    if topic_idx < total_topics - 1: b.button(text="التالي ➡️", callback_data=f"topic:{sec_id}:{topic_idx+1}")
    b.button(text="⬅️ المبحث", callback_data=f"sec:{sec_id}")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(2, 1, 1)
    return b.as_markup()

# ================== المعالجات ==================

@dp.message(CommandStart())
async def start(message: Message):
    welcome_text = (
        "🏛️ **ذاكرة الحضارات**\n"
        "رحلة عبر حضارات القرن الإفريقي\n\n"
        "اختر من القائمة أدناه للبدء:\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👨‍🎓 *إعداد الطلبة:* كراع عبد الغفور، تواتي صالح، بتيش وصال، وصال حداد."
    )
    await message.answer(welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "main_menu")
async def back_main(c: CallbackQuery):
    await c.message.edit_text("🏛️ ذاكرة الحضارات\nاختر من القائمة:", reply_markup=main_menu())

@dp.callback_query(F.data == "about")
async def about(c: CallbackQuery):
    text = (
        "ℹ️ **حول المشروع**\n\n"
        "موسوعة رقمية تفاعلية مبنية على بحث جامعي بعنوان:\n"
        "«الحضارات المبكرة في القرن الإفريقي»\n\n"
        "👨‍🎓 **إعداد الطلبة:**\n"
        "• كراع عبد الغفور (المبرمج)\n"
        "• تواتي صالح\n"
        "• بتيش وصال\n"
        "• وصال حداد\n\n"
        "*(تحت إشراف أستاذ مادة التاريخ)*"
    )
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "start_journey")
async def journey(c: CallbackQuery): await show_intro(c, 0)

@dp.callback_query(F.data.startswith("intro:"))
async def intro_page(c: CallbackQuery): await show_intro(c, int(c.data.split(":")[1]))

async def show_intro(c: CallbackQuery, page: int):
    data = INTRO[page]
    await c.message.edit_text(f"📜 {data['t']}\nصفحة {page+1} من {len(INTRO)}\n\n{data['b']}", reply_markup=intro_nav(page, len(INTRO)))

@dp.callback_query(F.data == "explore_sections")
async def sections(c: CallbackQuery):
    await c.message.edit_text("📚 المباحث:", reply_markup=sections_keyboard())

@dp.callback_query(F.data.startswith("sec:"))
async def sec_cover(c: CallbackQuery):
    sec_id = int(c.data.split(":")[1])
    sec = MABAHITH_DATA[sec_id]
    b = InlineKeyboardBuilder()
    for idx, topic in enumerate(sec["topics"]):
        b.button(text=f"📖 {topic['t']}", callback_data=f"topic:{sec_id}:{idx}")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(1, 1, 1, 1)
    await c.message.edit_text(f"🏛️ {sec['title']}\nاختر المطلب:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("topic:"))
async def topic_reading(c: CallbackQuery):
    _, sec_id, topic_idx = c.data.split(":")
    sec_id, topic_idx = int(sec_id), int(topic_idx)
    sec = MABAHITH_DATA[sec_id]
    topic = sec["topics"][topic_idx]
    caption = f"📌 {topic['t']}\n\n{topic['b']}"
    try:
        await c.message.delete()
        await c.message.answer_photo(photo=topic['img'], caption=caption, reply_markup=topic_nav(sec_id, topic_idx, len(sec["topics"])))
    except Exception:
        await c.message.answer(caption, reply_markup=topic_nav(sec_id, topic_idx, len(sec["topics"])))

@dp.callback_query(F.data == "conclusion")
async def conclusion(c: CallbackQuery):
    await c.message.edit_text(f"📜 **الخاتمة والنتائج**\n\n{CONCLUSION}", reply_markup=InlineKeyboardBuilder().button(text="⬅️ الرئيسية", callback_data="main_menu").as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "glossary")
async def glossary(c: CallbackQuery):
    b = InlineKeyboardBuilder()
    for k in GLOSSARY.keys():
        b.button(text=k, callback_data=f"term:{k}")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(2, 2, 2, 2, 1)
    await c.message.edit_text("📖 **موسوعة المصطلحات**\nاختر مصطلحاً:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("term:"))
async def term_def(c: CallbackQuery):
    term = c.data.split(":")[1]
    def_text = GLOSSARY[term]
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ المصطلحات", callback_data="glossary")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(1, 1)
    await c.message.edit_text(f"📖 **{term}**\n\n{def_text}", reply_markup=b.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "references")
async def references(c: CallbackQuery):
    await c.message.edit_text(REFERENCES, reply_markup=InlineKeyboardBuilder().button(text="⬅️ الرئيسية", callback_data="main_menu").as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "timeline")
async def timeline(c: CallbackQuery):
    text = "⏳ **الخط الزمني**\n\n🔹 الألفية الأولى ق.م: ظهور مملكة دعمت.\n🔹 القرن 15 ق.م: بعثة حتشبسوت إلى بونت.\n🔹 القرون الأولى م: بروز أكسوم.\n🔹 القرن 3 م: العملات الأكسومية.\n🔹 القرن 4 م: اعتناق عيزانا للمسيحية.\n🔹 عام 525 م: حملة كالب على حِمْيَر.\n🔹 القرنان 12 و 13 م: كنائس لاليبيلا."
    await c.message.edit_text(text, reply_markup=InlineKeyboardBuilder().button(text="⬅️ الرئيسية", callback_data="main_menu").as_markup())

@dp.callback_query(F.data == "atlas")
async def atlas(c: CallbackQuery):
    text = "🗺️ **أطلس الحضارات**\n\nالمواقع الجغرافية التقريبية:\n\n🔸 **بلاد بونت:** القرن الإفريقي (السواحل).\n🔸 **مملكة دعمت (يحا):** شمال إثيوبيا / جنوب إريتريا.\n🔸 **أكسوم:** المرتفعات الإثيوبية.\n🔸 **أدوليس:** ساحل البحر الأحمر (إريتريا).\n🔸 **مروي:** السودان (نهر النيل).\n🔸 **حِمْيَر:** اليمن (جنوب الجزيرة العربية)."
    b = InlineKeyboardBuilder()
    b.button(text="🖼️ عرض الخريطة التاريخية", callback_data="map_view")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(1, 1)
    await c.message.edit_text(text, reply_markup=b.as_markup())

@dp.callback_query(F.data == "map_view")
async def map_view(c: CallbackQuery):
    try:
        await c.message.delete()
        await c.message.answer_photo(photo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Red_Sea_map.jpg/800px-Red_Sea_map.jpg", caption="🗺️ **خريطة البحر الأحمر.**", reply_markup=InlineKeyboardBuilder().button(text="⬅️ الأطلس", callback_data="atlas").as_markup())
    except Exception:
        await c.answer("تعذر تحميل الصورة.", show_alert=True)

@dp.callback_query(F.data == "gallery")
async def gallery(c: CallbackQuery):
    b = InlineKeyboardBuilder()
    b.button(text="🗿 مسلات أكسوم", callback_data="img:aksum")
    b.button(text="🪙 العملات", callback_data="img:coins")
    b.button(text="⛪ لاليبيلا", callback_data="img:lalibela")
    b.button(text="⬅️ الرئيسية", callback_data="main_menu")
    b.adjust(1, 1, 1, 1)
    await c.message.edit_text("🖼️ **معرض الآثار**\nاختر أثراً:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("img:"))
async def show_img(c: CallbackQuery):
    img_type = c.data.split(":")[1]
    imgs = {
        "aksum": ("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Aksum_Stelae.jpg/800px-Aksum_Stelae.jpg", "🗿 مسلات أكسوم."),
        "coins": ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Aksumite_coins.jpg/800px-Aksumite_coins.jpg", "🪙 العملات الأكسومية."),
        "lalibela": ("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Lalibela_Church.jpg/800px-Lalibela_Church.jpg", "⛪ كنائس لاليبيلا.")
    }
    img, cap = imgs[img_type]
    try:
        await c.message.delete()
        await c.message.answer_photo(photo=img, caption=cap, reply_markup=InlineKeyboardBuilder().button(text="⬅️ المعرض", callback_data="gallery").as_markup())
    except Exception:
        await c.answer("تعذر تحميل الصورة.", show_alert=True)

@dp.callback_query(F.data == "quiz")
async def start_quiz(c: CallbackQuery):
    await quiz_question(c, 0)

async def quiz_question(c: CallbackQuery, idx: int):
    q = QUIZ_DATA[idx]
    b = InlineKeyboardBuilder()
    for i, opt in enumerate(q["options"]):
        b.button(text=opt, callback_data=f"quiz_ans:{idx}:{i}")
    b.adjust(1)
    await c.message.edit_text(f"❓ السؤال {idx+1}:\n\n{q['q']}", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("quiz_ans:"))
async def quiz_answer(c: CallbackQuery):
    _, q_idx, ans_idx = c.data.split(":")
    q_idx, ans_idx = int(q_idx), int(ans_idx)
    q = QUIZ_DATA[q_idx]
    text = "✅ **إجابة صحيحة!**" if ans_idx == q["correct"] else "❌ **إجابة خاطئة.**"
    if q_idx + 1 < len(QUIZ_DATA):
        b = InlineKeyboardBuilder().button(text="التالي ➡️", callback_data=f"quiz_next:{q_idx+1}")
    else:
        text += "\n\n🎉 **أكملت الاختبار!**"
        b = InlineKeyboardBuilder().button(text="⬅️ الرئيسية", callback_data="main_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("quiz_next:"))
async def quiz_next(c: CallbackQuery):
    idx = int(c.data.split(":")[1])
    await quiz_question(c, idx)

# ================== تشغيل البوت والسيرفر ==================

async def web_server():
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()

async def main():
    print("✅ متحف ذاكرة الحضارات يعمل الآن...")
    await web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
