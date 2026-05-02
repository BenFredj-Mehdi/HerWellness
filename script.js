const i18n = {
  en: {
    title: 'Pregnancy Month Guidance',
    lead: 'Select which month you\'re in to see common problems and suggested solutions.',
    labelMonth: 'Pregnancy Month',
    submit: 'Get Guidance',
    chooseMonth: '-- Select month --',
    notFound: 'If you don\'t see what you have, try talking to our chatbot.',
    chatLinkText: 'Open chatbot'
  },
  ar: {
    title: 'إرشادات للحامل حسب الشهر',
    lead: 'اختاري الشهر اللي انتِ فيه باش تشوفي المشاكل الشائعة والحلول المقترحة.',
    labelMonth: 'الشهر',
    submit: 'عرض الإرشادات',
    chooseMonth: '-- اختاري الشهر --',
    notFound: 'ما لقيتش اللي تحس به؟ تنجمي تحكي مع الشات بوت',
    chatLinkText: 'افتح الشات بوت'
  }
};

const data = {
  en: {
    1: { title: 'Month 1', problems: [
      {name:'Nausea / Morning sickness', solution:'Eat small, frequent bland meals; try ginger or peppermint; stay hydrated.', todo:'Keep plain snacks at hand; avoid strong smells; contact provider if vomiting is severe.'},
      {name:'Fatigue', solution:'Prioritize rest and light activity; eat balanced meals.', todo:'Nap when possible and ask for help with heavy tasks.'},
      {name:'Breast tenderness', solution:'Wear a supportive bra; use warm compresses for comfort.', todo:'Choose comfortable undergarments and monitor pain.'}
    ]},
    2: { title: 'Month 2', problems: [
      {name:'Continued nausea', solution:'Maintain small meals; try cold foods and electrolyte sips.', todo:'Track triggers; contact provider if unable to keep fluids down.'},
      {name:'Food aversions / cravings', solution:'Focus on nutrient-dense options.', todo:'Plan simple preferred foods to maintain calories.'},
      {name:'Mood swings', solution:'Rest and seek support.', todo:'Contact provider if mood changes feel overwhelming.'}
    ]},
    3: { title: 'Month 3', problems: [
      {name:'Frequent urination', solution:'Limit fluids before bed and empty bladder fully.', todo:'Report burning or pain to provider.'},
      {name:'Heartburn', solution:'Eat smaller meals and avoid spicy/fatty foods.', todo:'Try antacids approved by provider.'},
      {name:'Constipation', solution:'Increase fiber, fluids, and gentle activity.', todo:'Consider fiber supplement after checking with provider.'}
    ]},
    4: { title: 'Month 4', problems: [
      {name:'Round ligament pain', solution:'Change position slowly and use gentle stretching.', todo:'Avoid sudden twisting; contact provider if severe.'},
      {name:'Increased appetite', solution:'Choose nutrient-rich snacks and balanced meals.', todo:'Focus on protein, whole grains, fruits, and vegetables.'},
      {name:'Skin changes', solution:'Use gentle moisturizers and sun protection.', todo:'Report sudden rashes to provider.'}
    ]},
    5: { title: 'Month 5', problems: [
      {name:'Back pain', solution:'Maintain posture, try pelvic-support belts and gentle exercise.', todo:'Consider prenatal yoga or PT if recommended.'},
      {name:'Mild swelling', solution:'Elevate feet, avoid long standing, and hydrate.', todo:'Seek care for sudden or severe swelling.'},
      {name:'Stretch marks', solution:'Moisturize and maintain steady weight gain.', todo:'Prioritize hydration and skin care.'}
    ]},
    6: { title: 'Month 6', problems: [
      {name:'Leg cramps', solution:'Stretch calves and stay hydrated.', todo:'Talk to provider about supplements if frequent.'},
      {name:'Varicose veins', solution:'Elevate legs and wear compression stockings.', todo:'Discuss pain or swelling with clinician.'},
      {name:'Sleep issues', solution:'Use pillows for support and limit caffeine.', todo:'Try relaxation techniques before bed.'}
    ]},
    7: { title: 'Month 7', problems: [
      {name:'Shortness of breath', solution:'Slow down activity and sleep propped up.', todo:'Report sudden severe breathlessness immediately.'},
      {name:'Braxton Hicks contractions', solution:'Rest, change position, and hydrate.', todo:'If contractions become regular or painful, contact provider.'},
      {name:'Worse heartburn', solution:'Avoid late meals and fatty foods.', todo:'Use remedies approved by your care team.'}
    ]},
    8: { title: 'Month 8', problems: [
      {name:'Pelvic pressure', solution:'Use supportive belts and pelvic floor exercises.', todo:'Report severe pressure or leaking fluid.'},
      {name:'Insomnia', solution:'Short naps and relaxation; limit screen time.', todo:'Discuss sleep aids with clinician if needed.'},
      {name:'Urinary frequency', solution:'Plan bathroom access and avoid excess fluids before bed.', todo:'Watch for pain or burning and report infections.'}
    ]},
    9: { title: 'Month 9', problems: [
      {name:'Labor preparation questions', solution:'Attend childbirth classes and make a birth plan.', todo:'Know provider/hospital contact and packing list.'},
      {name:'Increased swelling', solution:'Rest, elevate feet, avoid salty foods.', todo:'Seek immediate care for sudden severe swelling or headache.'},
      {name:'Difficulty sleeping', solution:'Use pillows for support and short daytime rest.', todo:'Practice relaxation and breathing techniques.'}
    ]}
  },
  ar: {
    1: { title: 'الشهر 1', problems: [
      {name:'الغثيان / القيء', solution:'كلي وجبات صغيرة ومتكررة؛ جربي الزنجبيل أو النعناع؛ شربي برشا سوائل.', todo:'خلي كروسانات بسيطة معاك، وتجنبي الروائح القوية؛ إذا القيء شديد، تواصلي مع الطبيب.'},
      {name:'التعب', solution:'ريحي واعملي نشاط خفيف كيف المشي؛ كلي أكل متوازن.', todo:'نامي كيما تجي الفرصة وطلبي المساعدة في الأعمال الصعيبة.'},
      {name:'حساسية في الثدي', solution:'لبسي صدرية داعمة واستعملي كمادات دافية.', todo:'اختاري ملابس مريحة وراعي إذا كان الألم قوي.'}
    ]},
    2: { title: 'الشهر 2', problems: [
      {name:'استمرار الغثيان', solution:'كملي كلي وجبات صغيرة؛ جربي الماكلة الباردة ومشروبات إلكتروليت.', todo:'راقبي المحفزات؛ إذا ما تنجميش تحتفظي بالسوائل، تواصلي مع الطبيب.'},
      {name:'نفور أو شهوة للأكل', solution:'اختاري أطعمة مغذيّة.', todo:'حضري أكلات بسيطة تحبّيها باش تحافظي على السعرات.'},
      {name:'تقلبات المزاج', solution:'ارتاحي وشاركي اللي تحسي بيه مع حدّ يقربلك.', todo:'إذا حسيتي برقٍ كبير، تواصلي مع الطبيب.'}
    ]},
    3: { title: 'الشهر 3', problems: [
      {name:'كثرة التبول', solution:'نقصي شرب قبل النوم وفري بلاصة باش تتبولى.', todo:'إذا كان في حرقة ولا ألم، لازم الطبيب.'},
      {name:'حرقة المعدة', solution:'كلي وجبات أصغر وتجنبي المأكولات الحارة والدسمة.', todo:'اسألي الطبيب قبل تاخذي أدوية.'},
      {name:'إمساك', solution:'زيدي الألياف، اشربي ماء، وحركي جسمك.', todo:'استشيري الطبيب قبل أي مكملات.'}
    ]},
    4: { title: 'الشهر 4', problems: [
      {name:'ألم أربطة البطن', solution:'بدّلي الوضعية بشويّة وافركي برفق واستعملي حار خفيف.', todo:'تجنبي الحركات المفاجئة وإذا الألم قوي، تواصلي مع الطبيب.'},
      {name:'زيادة الشهية', solution:'اختاري سناكس مغذية ووجبات متوازنة.', todo:'ركزّي على البروتين والحبوب الكاملة والخضرة.'},
      {name:'تغيّرات في الجلد', solution:'استعملي مرطبات لطيفة وحماية من الشمس.', todo:'بلغي الطبيب إذا ظهرت حساسية قوية.'}
    ]},
    5: { title: 'الشهر 5', problems: [
      {name:'آلام الظهر', solution:'حافظي على الوقفة الصحيحة، استعملي حزام داعم وممارسة خفيفة.', todo:'جربي يوجا للحوامل أو العلاج الطبيعي إذا نصح الطبيب.'},
      {name:'تورم خفيف', solution:'رفعي رجليك، وتجنبي الوقوف الطويل، وابقاي مترطبة.', todo:'إذا التورم مفاجئ أو شديد، لازم مراجعة.'},
      {name:'علامات التمدد', solution:'رطّبي الجلد وحافظي على زيادة وزن معتدلة.', todo:'الوقاية مش مضمونة لكن الترطيب يساعد.'}
    ]},
    6: { title: 'الشهر 6', problems: [
      {name:'تشنجات الساق', solution:'فرّجي عضلات الساق وشربي ماء كافي.', todo:'اسألي الطبيب على مكملات إذا متكررة.'},
      {name:'دوالي', solution:'ارفعي رجليك ولبسي جوارب ضغط.', todo:'ناقشي أي ألم أو تورم مع الطبيب.'},
      {name:'مشكلة في النعاس', solution:'نظمي روتين، استعملي مخدات دعم، وقللي الكافيين.', todo:'جربي تقنيات الاسترخاء.'}
    ]},
    7: { title: 'الشهر 7', problems: [
      {name:'ضيق التنفس', solution:'بطّئي الحركة ونرّبّي الوسائد كي تنامي.', todo:'لو صار ضيق مفاجئ أو شديد، تواصلي مع الطبيب فوراً.'},
      {name:'انقباضات براكستون هيكس', solution:'ارتاحي وبدّلي الوضعية واشربي ماء.', todo:'إذا الانقباضات صارت منتظمة ومؤلمة، تواصلي مع الطبيب.'},
      {name:'سوء حرقة المعدة', solution:'تجنبي الوجبات المتأخرة والدسمة.', todo:'استعملي علاجات يوافق عليها الطبيب.'}
    ]},
    8: { title: 'الشهر 8', problems: [
      {name:'ضغط حوضي', solution:'استعملي أحزمة دعم وممارسة عضلات الحوض.', todo:'لو حسيتي بسيلان ماء أو ضغط قوي، تواصلي مع الطبيب.'},
      {name:'أرق', solution:'نامي نهارات قصيرة واستعملي تقنيات الاسترخاء.', todo:'ناقشي مع الطبيب إذا تحتاجي أدوية آمنة.'},
      {name:'كثرة التبول', solution:'نظمي شربك وتجنبي شرب كثير قبل النوم.', todo:'راقبي أي ألم أو حرقة وأبلغي الطبيب.'}
    ]},
    9: { title: 'الشهر 9', problems: [
      {name:'استعداد للولادة', solution:'حضري حقيبة الولادة واعملي خطة ولادة.', todo:'عرفي أرقام الطبيب والمستشفى.'},
      {name:'تورم شديد وعدم راحة', solution:'ارتاحي وارفعي رجليك وتجنبي الماكلة المالحة.', todo:'لو تورم مفاجئ مع صداع أو مشاكل في الرؤية، راجعي الطوارئ.'},
      {name:'صعوبة في النوم', solution:'استعملي مخدات دعم وارتاحي نهاراً.', todo:'تدرّبي تقنيات التنفس والاسترخاء للولادة.'}
    ]}
  }
};

let currentLang = 'ar';

function setLanguage(lang){
  currentLang = lang;
  const ui = i18n[lang];
  document.getElementById('site-title').textContent = ui.title;
  document.getElementById('site-lead').textContent = ui.lead;
  document.getElementById('label-month').textContent = ui.labelMonth;
  document.getElementById('submit-btn').textContent = ui.submit;
  // update select placeholder option text
  const sel = document.getElementById('month');
  sel.options[0].text = ui.chooseMonth;
  // update month option labels
  for(let i=1;i<=9;i++){ sel.options[i].text = (lang==='ar'? `الشهر ${i}` : `Month ${i}`); }
  // re-render current selection if any
  const month = document.getElementById('month').value;
  if(month) renderMonth(month);
}

function renderMonth(month){
  const results = document.getElementById('results');
  results.innerHTML = '';
  const info = data[currentLang][month];
  const chatSuggestion = document.getElementById('chat-suggestion');
  chatSuggestion.innerHTML = '';
  if(!info){
    const p = document.createElement('p');
    p.className = 'muted';
    p.textContent = i18n[currentLang].notFound;
    results.appendChild(p);
    const a = document.createElement('a');
    a.href = 'chatbot.html';
    a.textContent = i18n[currentLang].chatLinkText;
    a.style.display = 'inline-block';
    a.style.marginTop = '8px';
    a.className = 'button-link';
    chatSuggestion.appendChild(a);
    return;
  }

  const h = document.createElement('h2');
  h.textContent = info.title;
  results.appendChild(h);

  info.problems.forEach(p => {
    const box = document.createElement('div');
    box.className = 'problem';
    const name = document.createElement('h3');
    name.textContent = p.name;
    const sol = document.createElement('p');
    sol.innerHTML = '<strong>' + (currentLang==='ar' ? 'الاقتراح:' : 'Suggested:') + '</strong> ' + p.solution;
    const todo = document.createElement('p');
    todo.className = 'muted';
    todo.innerHTML = '<strong>' + (currentLang==='ar' ? 'ما تعمل:' : 'To do:') + '</strong> ' + p.todo;
    box.appendChild(name);
    box.appendChild(sol);
    box.appendChild(todo);
    results.appendChild(box);
  });
}

document.getElementById('month-form').addEventListener('submit', e => {
  e.preventDefault();
  const month = document.getElementById('month').value;
  renderMonth(month);
});

document.getElementById('lang').addEventListener('change', e => {
  setLanguage(e.target.value);
});

// initialize default language
setLanguage(currentLang);

