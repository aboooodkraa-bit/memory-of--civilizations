# features.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# 1. الخط الزمني
@router.callback_query(F.data == "timeline")
async def show_timeline(c: CallbackQuery):
    text = (
        "⏳ **الخط الزمني لتاريخ القرن الإفريقي**\n\n"
        "🔹 **الألفية الأولى ق.م:** ظهور مملكة دعمت.\n"
        "🔹 **القرن 15 ق.م:** بعثة الملكة حتشبسوت إلى بلاد بونت.\n"
        "🔹 **القرون الأولى م:** بروز أكسوم كقوة تجارية.\n"
        "🔹 **القرن 3 م:** إصدار العملات الأكسومية.\n"
        "🔹 **القرن 4 م:** اعتناق الملك عيزانا للمسيحية.\n"
        "🔹 **عام 525 م:** حملة الملك كالب على حِمْيَر.\n"
        "🔹 **القرنان 12 و 13 م:** بناء كنائس لاليبيلا."
    )
    b = InlineKeyboardBuilder().button(text="⬅️ القائمة الرئيسية", callback_data="main_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")

# 2. المقارنات العلمية
@router.callback_query(F.data == "compare")
async def show_compare(c: CallbackQuery):
    text = (
        "⚖️ **قارن واكتشف: الحضارات الثلاث**\n\n"
        "🟢 **بلاد بونت:**\n"
        "- طبيعة الكيان: شبكة تجارية/كيان حضاري.\n"
        "- الموقع: غير محدد بدقة (القرن الإفريقي).\n"
        "- الاقتصاد: البخور، المر، الذهب، العاج.\n\n"
        "🟡 **مملكة دعمت:**\n"
        "- طبيعة الكيان: مملكة سياسية مبكرة.\n"
        "- الموقع: شمال إثيوبيا وجنوب إريتريا.\n"
        "- الاقتصاد: الزراعة، التجارة مع جنوب الجزيرة.\n\n"
        "🔵 **إمبراطورية أكسوم:**\n"
        "- طبيعة الكيان: إمبراطورية كبرى.\n"
        "- الموقع: المرتفعات + ميناء أدوليس.\n"
        "- الاقتصاد: الزراعة، التجارة الدولية، النظام النقدي."
    )
    b = InlineKeyboardBuilder().button(text="⬅️ القائمة الرئيسية", callback_data="main_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")

# 3. الاختبارات التفاعلية (Quiz)
QUIZ_QUESTIONS = [
    {
        "q": "ما المنطقة التي ارتبطت بعلاقات تجارية مع مصر الفرعونية؟",
        "options": ["بلاد بونت", "زيمبابوي", "أثينا"],
        "correct": 0
    },
    {
        "q": "ما الميناء الذي مثّل المنفذ التجاري الرئيسي لأكسوم؟",
        "options": ["الإسكندرية", "أدوليس", "جدة"],
        "correct": 1
    },
    {
        "q": "في عهد أي ملك ارتبط اعتناق أكسوم للمسيحية؟",
        "options": ["الملك كالب", "الملك عيزانا", "حتشبسوت"],
        "correct": 1
    }
]

@router.callback_query(F.data == "quiz")
async def start_quiz(c: CallbackQuery):
    await c.message.edit_text("🎯 **اختبار المعلومات**\n\nهل أنت مستعد؟", 
                              reply_markup=InlineKeyboardBuilder().button(text="ابدأ الاختبار", callback_data="quiz_q:0").as_markup())

@router.callback_query(F.data.startswith("quiz_q:"))
async def quiz_question(c: CallbackQuery):
    idx = int(c.data.split(":")[1])
    q = QUIZ_QUESTIONS[idx]
    
    b = InlineKeyboardBuilder()
    for i, opt in enumerate(q["options"]):
        b.button(text=opt, callback_data=f"quiz_ans:{idx}:{i}")
    b.adjust(1)
    
    await c.message.edit_text(f"❓ السؤال {idx+1}:\n\n{q['q']}", reply_markup=b.as_markup())

@router.callback_query(F.data.startswith("quiz_ans:"))
async def quiz_answer(c: CallbackQuery):
    _, q_idx, ans_idx = c.data.split(":")
    q_idx, ans_idx = int(q_idx), int(ans_idx)
    q = QUIZ_QUESTIONS[q_idx]
    
    if ans_idx == q["correct"]:
        text = "✅ **إجابة صحيحة!** أحسنت."
    else:
        text = "❌ **إجابة خاطئة.**"
        
    if q_idx + 1 < len(QUIZ_QUESTIONS):
        text += f"\n\nالسؤال التالي جاهز."
        cb_data = f"quiz_q:{q_idx+1}"
        btn_text = "التالي ➡️"
    else:
        text += "\n\n🎉 **أكملت الاختبار بنجاح!**"
        cb_data = "main_menu"
        btn_text = "⬅️ القائمة الرئيسية"
        
    b = InlineKeyboardBuilder().button(text=btn_text, callback_data=cb_data)
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")

# 4. المصادر
@router.callback_query(F.data == "references")
async def show_references(c: CallbackQuery):
    text = (
        "📑 **المصادر والمراجع الأساسية**\n\n"
        "• **UNESCO:** تقارير عن مواقع التراث العالمي (أكسوم، لاليبيلا، زيمبابوي).\n"
        "• **British Museum:** مقتنيات ونقوش أكسومية.\n"
        "• **Metropolitan Museum:** العملات القديمة والآثار.\n"
        "• **Stuart Munro-Hay:** دراسات أكاديمية عن أكسوم.\n"
        "• **دراسات يحا:** أبحاث أثرية عن مملكة دعمت."
    )
    b = InlineKeyboardBuilder().button(text="⬅️ القائمة الرئيسية", callback_data="main_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")
