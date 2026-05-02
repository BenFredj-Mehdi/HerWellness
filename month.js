const i18n = {
  en: {
    guidanceTitle: 'Pregnancy Months',
    guidanceLead: 'Pick the month you are in to see tailored suggestions.',
    monthLabel: 'Month',
    aiCtaTitle: 'Need more help?',
    aiCtaBody: 'If you do not find your answer here, talk to the AI expert.',
    aiCtaButton: 'Talk to the AI expert',
  },
  ar: {
    guidanceTitle: 'أشهر الحمل',
    guidanceLead: 'اختاري الشهر اللي إنتِ فيه باش تشوفي الإرشادات المناسبة.',
    monthLabel: 'الشهر',
    aiCtaTitle: 'تحبي مساعدة أكثر؟',
    aiCtaBody: 'إذا ما لقيتيش الحل هنا، تنجمي تهضري مع الخبير الذكي.',
    aiCtaButton: 'تحدثي مع الخبير الذكي',
  }
};

const monthData = {
  en: {
    1: { title: 'Month 1', subtitle: 'Common first-month guidance', items: [
      { name: 'Nausea / Morning sickness', solution: 'Eat small, frequent bland meals and stay hydrated.', todo: 'Avoid strong smells and call your provider if vomiting is severe.' },
      { name: 'Fatigue', solution: 'Prioritize rest and light activity.', todo: 'Sleep when possible and ask for help with heavy tasks.' },
      { name: 'Breast tenderness', solution: 'Wear a supportive bra and use warm compresses.', todo: 'Choose comfortable clothes and monitor pain.' }
    ]},
    2: { title: 'Month 2', subtitle: 'Common second-month guidance', items: [
      { name: 'Continued nausea', solution: 'Keep small meals and try cold foods.', todo: 'Track triggers and seek help if you cannot keep fluids down.' },
      { name: 'Food aversions / cravings', solution: 'Focus on nutrient-dense choices.', todo: 'Plan simple foods you tolerate well.' },
      { name: 'Mood swings', solution: 'Rest and seek support from loved ones.', todo: 'Contact your provider if the mood changes feel overwhelming.' }
    ]},
    3: { title: 'Month 3', subtitle: 'Common third-month guidance', items: [
      { name: 'Frequent urination', solution: 'Limit fluids before bed and empty the bladder fully.', todo: 'Report burning or pain to your provider.' },
      { name: 'Heartburn', solution: 'Eat smaller meals and avoid spicy or fatty foods.', todo: 'Ask about approved antacids if needed.' },
      { name: 'Constipation', solution: 'Increase fiber, fluids, and gentle activity.', todo: 'Check with your provider before using supplements.' }
    ]},
    4: { title: 'Month 4', subtitle: 'Common fourth-month guidance', items: [
      { name: 'Round ligament pain', solution: 'Move slowly and use gentle stretching.', todo: 'Avoid sudden twisting and call your provider if severe.' },
      { name: 'Increased appetite', solution: 'Choose nutrient-rich snacks and balanced meals.', todo: 'Focus on protein, fruits, vegetables, and whole grains.' },
      { name: 'Skin changes', solution: 'Use gentle moisturizers and sun protection.', todo: 'Report sudden rashes or itching to your provider.' }
    ]},
    5: { title: 'Month 5', subtitle: 'Common fifth-month guidance', items: [
      { name: 'Back pain', solution: 'Keep good posture and try gentle exercise.', todo: 'Consider prenatal yoga or physical therapy if recommended.' },
      { name: 'Mild swelling', solution: 'Elevate your feet, avoid long standing, and hydrate.', todo: 'Seek care for sudden or severe swelling.' },
      { name: 'Stretch marks', solution: 'Moisturize and maintain steady weight gain.', todo: 'Hydration and skin care help comfort, even if marks still appear.' }
    ]},
    6: { title: 'Month 6', subtitle: 'Common sixth-month guidance', items: [
      { name: 'Leg cramps', solution: 'Stretch calves and stay hydrated.', todo: 'Talk to your provider about supplements if cramps are frequent.' },
      { name: 'Varicose veins', solution: 'Elevate your legs and wear compression stockings.', todo: 'Discuss pain or swelling with your clinician.' },
      { name: 'Sleep issues', solution: 'Use pillows for support and limit caffeine.', todo: 'Try relaxation techniques before bed.' }
    ]},
    7: { title: 'Month 7', subtitle: 'Common seventh-month guidance', items: [
      { name: 'Shortness of breath', solution: 'Slow down activity and sleep propped up.', todo: 'Report sudden severe breathlessness immediately.' },
      { name: 'Braxton Hicks contractions', solution: 'Rest, change position, and hydrate.', todo: 'If contractions become regular or painful, contact your provider.' },
      { name: 'Worse heartburn', solution: 'Avoid late meals and fatty foods.', todo: 'Use remedies approved by your care team.' }
    ]},
    8: { title: 'Month 8', subtitle: 'Common eighth-month guidance', items: [
      { name: 'Pelvic pressure', solution: 'Use supportive belts and pelvic floor exercises.', todo: 'Report severe pressure or leaking fluid.' },
      { name: 'Insomnia', solution: 'Short naps and relaxation; limit screen time.', todo: 'Discuss sleep aids with your clinician if needed.' },
      { name: 'Urinary frequency', solution: 'Plan bathroom access and reduce fluids before bed.', todo: 'Watch for pain or burning and report infections.' }
    ]},
    9: { title: 'Month 9', subtitle: 'Common ninth-month guidance', items: [
      { name: 'Labor preparation questions', solution: 'Attend childbirth classes and make a birth plan.', todo: 'Know your provider and hospital contact details.' },
      { name: 'Increased swelling', solution: 'Rest, elevate your feet, and avoid salty foods.', todo: 'Seek immediate care for sudden severe swelling or headache.' },
      { name: 'Difficulty sleeping', solution: 'Use pillows for support and short daytime rest.', todo: 'Practice relaxation and breathing techniques.' }
    ]}
  },
  ar: {
    1: { title: 'الشهر 1', subtitle: 'إرشادات الشهر الأول', items: [
      { name: 'الغثيان / القيء', solution: 'كلي وجبات صغيرة ومتكررة، وشرّبي الماء برشا.', todo: 'تجنبي الروائح القوية وإذا القيء شديد، تواصلي مع الطبيب.' },
      { name: 'التعب', solution: 'ريحي واعملي نشاط خفيف كيف المشي.', todo: 'نامي وقت اللي تنجمي واطلبي المساعدة في الأعمال الثقيلة.' },
      { name: 'حساسية الثدي', solution: 'لبسي صدرية داعمة واستعملي كمادات دافية.', todo: 'اختاري ملابس مريحة وراقبي إذا الألم قوي.' }
    ]},
    2: { title: 'الشهر 2', subtitle: 'إرشادات الشهر الثاني', items: [
      { name: 'استمرار الغثيان', solution: 'كمّلي وجبات صغيرة وجربي الأكل البارد.', todo: 'راقبي المحفزات وإذا ما تنجميش تحتفظي بالسوائل، تواصلي مع الطبيب.' },
      { name: 'نفور أو شهوة للأكل', solution: 'اختاري أطعمة مغذية ومفيدة.', todo: 'حضري أكلات بسيطة تحبيها باش تحافظي على الطاقة.' },
      { name: 'تقلبات المزاج', solution: 'ارتاحي وشاركي اللي تحسي به مع حد قريب.', todo: 'إذا حسيتي بثقل كبير، تواصلي مع الطبيب.' }
    ]},
    3: { title: 'الشهر 3', subtitle: 'إرشادات الشهر الثالث', items: [
      { name: 'كثرة التبول', solution: 'نقصي الشرب قبل النوم وافرغي المثانة مليح.', todo: 'إذا كان في حرقة أو ألم، لازم الطبيب.' },
      { name: 'حرقة المعدة', solution: 'كلي وجبات أصغر وتجنبي الحار والدسم.', todo: 'اسألي الطبيب قبل أي دواء.' },
      { name: 'إمساك', solution: 'زيدي الألياف والماء والحركة الخفيفة.', todo: 'استشيري الطبيب قبل أي مكملات.' }
    ]},
    4: { title: 'الشهر 4', subtitle: 'إرشادات الشهر الرابع', items: [
      { name: 'ألم أربطة البطن', solution: 'بدّلي الوضعية بشويّة واستعملي تمدد خفيف.', todo: 'تجنبي الحركات المفاجئة وإذا الألم قوي، تواصلي مع الطبيب.' },
      { name: 'زيادة الشهية', solution: 'اختاري سناكات مغذية ووجبات متوازنة.', todo: 'ركزي على البروتين والخضرة والحبوب الكاملة.' },
      { name: 'تغيّرات في الجلد', solution: 'استعملي مرطبات لطيفة وحماية من الشمس.', todo: 'بلّغي الطبيب إذا ظهرت حساسية قوية.' }
    ]},
    5: { title: 'الشهر 5', subtitle: 'إرشادات الشهر الخامس', items: [
      { name: 'آلام الظهر', solution: 'حافظي على الوقفة الصحيحة واعملي حركة خفيفة.', todo: 'جربي يوجا للحامل أو العلاج الطبيعي إذا نصح الطبيب.' },
      { name: 'تورم خفيف', solution: 'ارفعي رجليك وتجنبي الوقوف الطويل وابقاي مترطبة.', todo: 'إذا التورم مفاجئ أو شديد، لازم مراجعة.' },
      { name: 'علامات التمدد', solution: 'رطّبي الجلد وحافظي على زيادة وزن معتدلة.', todo: 'الترطيب يساعد في الراحة حتى لو العلامات تظهر.' }
    ]},
    6: { title: 'الشهر 6', subtitle: 'إرشادات الشهر السادس', items: [
      { name: 'تشنجات الساق', solution: 'فرّجي عضلات الساق واشربي ماء كافي.', todo: 'اسألي الطبيب على مكملات إذا التشنجات متكررة.' },
      { name: 'دوالي', solution: 'ارفعي رجليك ولبسي جوارب ضغط.', todo: 'ناقشي أي ألم أو تورم مع الطبيب.' },
      { name: 'مشكلة في النوم', solution: 'استعملي مخدات دعم وقللي الكافيين.', todo: 'جربي تقنيات الاسترخاء قبل النوم.' }
    ]},
    7: { title: 'الشهر 7', subtitle: 'إرشادات الشهر السابع', items: [
      { name: 'ضيق التنفس', solution: 'بطّئي الحركة ونومي بمساندة.', todo: 'لو صار ضيق مفاجئ أو شديد، تواصلي مع الطبيب فوراً.' },
      { name: 'انقباضات براكستون هيكس', solution: 'ارتاحي وبدّلي الوضعية واشربي ماء.', todo: 'إذا صارت منتظمة ومؤلمة، تواصلي مع الطبيب.' },
      { name: 'حرقة أسوأ', solution: 'تجنبي الوجبات المتأخرة والدسمة.', todo: 'استعملي علاجات يوافق عليها الطبيب.' }
    ]},
    8: { title: 'الشهر 8', subtitle: 'إرشادات الشهر الثامن', items: [
      { name: 'ضغط الحوض', solution: 'استعملي أحزمة دعم وممارسة عضلات الحوض.', todo: 'لو حسّيتي بسيلان ماء أو ضغط قوي، تواصلي مع الطبيب.' },
      { name: 'الأرق', solution: 'نامي نهارات قصيرة واستعملي تقنيات الاسترخاء.', todo: 'ناقشي مع الطبيب إذا تحتاجي حلول آمنة.' },
      { name: 'كثرة التبول', solution: 'نظمي شربك وتجنبي شرب كثير قبل النوم.', todo: 'راقبي أي ألم أو حرقة وأبلغي الطبيب.' }
    ]},
    9: { title: 'الشهر 9', subtitle: 'إرشادات الشهر التاسع', items: [
      { name: 'التحضير للولادة', solution: 'حضري حقيبة الولادة واعملي خطة ولادة.', todo: 'اعرفي أرقام الطبيب والمستشفى.' },
      { name: 'تورم شديد', solution: 'ارتاحي وارفعي رجليك وتجنبي الماكلة المالحة.', todo: 'لو تورم مفاجئ مع صداع أو تشويش في النظر، راجعي الطوارئ.' },
      { name: 'صعوبة النوم', solution: 'استعملي مخدات دعم وخذي راحة نهاراً.', todo: 'تدربي على التنفس والاسترخاء للولادة.' }
    ]}
  }
};

function getLang() {
  return localStorage.getItem('language') || 'ar';
}

function setLang(lang) {
  localStorage.setItem('language', lang);
  document.documentElement.lang = lang === 'en' ? 'en' : 'ar';
  document.documentElement.dir = 'rtl';
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderGuidancePage() {
  const grid = document.getElementById('month-grid');
  if (!grid) return;
  const lang = getLang();
  const ui = i18n[lang];
  const data = monthData[lang];
  const titleEl = document.getElementById('site-title');
  const leadEl = document.getElementById('site-lead');
  if (titleEl) titleEl.textContent = ui.guidanceTitle;
  if (leadEl) leadEl.textContent = ui.guidanceLead;
  grid.innerHTML = '';
  for (let month = 1; month <= 9; month += 1) {
    const entry = data[month];
    const card = document.createElement('a');
    card.className = 'month-card';
    card.href = `month-${month}.html`;
    card.innerHTML = `
      <span class="month-card__badge">${ui.monthLabel} ${month}</span>
      <h2>${escapeHtml(entry.title)}</h2>
      <p>${escapeHtml(entry.subtitle)}</p>
      <span class="month-card__cta">${lang === 'ar' ? 'افتحي الصفحة' : 'Open page'} →</span>
    `;
    grid.appendChild(card);
  }
}

function renderMonthPage() {
  const page = document.querySelector('[data-month-page]');
  if (!page) return;
  const lang = getLang();
  const month = Number(page.getAttribute('data-month-page'));
  const data = monthData[lang][month];
  const ui = i18n[lang];
  const content = document.getElementById('month-content');
  if (!content || !data) return;
  const itemsHtml = data.items.map((item) => `
    <article class="problem problem--month">
      <h3>${escapeHtml(item.name)}</h3>
      <p><strong>${lang === 'ar' ? 'الاقتراح:' : 'Suggested:'}</strong> ${escapeHtml(item.solution)}</p>
      <p class="muted"><strong>${lang === 'ar' ? 'ما تعمل:' : 'To do:'}</strong> ${escapeHtml(item.todo)}</p>
    </article>
  `).join('');
  content.innerHTML = `
    <header class="month-hero">
      <p class="eyebrow">${ui.monthLabel} ${month}</p>
      <h1>${escapeHtml(data.title)}</h1>
      <p class="lead">${escapeHtml(data.subtitle)}</p>
    </header>
    <section class="month-items">${itemsHtml}</section>
    <section class="ai-cta">
      <h2>${escapeHtml(ui.aiCtaTitle)}</h2>
      <p>${escapeHtml(ui.aiCtaBody)}</p>
      <a class="start-btn ai-cta-btn" href="ai_agent.html">${escapeHtml(ui.aiCtaButton)}</a>
    </section>
  `;
}

function bindLanguageSelector() {
  const selector = document.getElementById('lang');
  const current = getLang();
  setLang(current);
  if (selector) {
    selector.value = current;
    selector.addEventListener('change', () => {
      setLang(selector.value);
      renderGuidancePage();
      renderMonthPage();
    });
  }
}

bindLanguageSelector();
renderGuidancePage();
renderMonthPage();
