# Buying guides content. Each guide: slug, title/lead per language, sections (h, paragraphs/bullets), picks (product slugs), deals tab, faq.
GUIDES = [
 {
  "slug": "rfid-blocking-cards",
  "picks": ["rfid-nfc-blocking-card"],
  "deals": "rfid",
  "ar": {
   "title": "بطاقات حماية RFID: هل تحتاجها فعلاً؟",
   "card": "أفضل بطاقات ومحافظ حماية RFID",
   "cardp": "ما الذي يحمي بطاقاتك فعلاً، وما الذي مجرّد تسويق.",
   "lead": "دليل صريح لمن يحمل بطاقات دفع لاتلامسية أو جواز سفر حديثاً: كيف تعمل الحماية، ومتى تفيد، وكيف تختار وتستعمل بطاقة الحجب بشكل صحيح.",
   "sections": [
    ("ما هي قراءة RFID وNFC؟", ["بطاقات الدفع باللمس وجوازات السفر البيومترية تحتوي شريحة صغيرة تعمل بتردد 13.56 ميغاهرتز. عندما تقترب من جهاز قارئ تتبادل معه بعض البيانات دون لمس.", "الفكرة وراء بطاقات الحجب بسيطة: طبقة معدنية تشوّش على هذا التردد، فيصعب على أي قارئ قريب أن يتواصل مع البطاقات المجاورة لها."]),
    ("ما حجم الخطر حقيقةً؟", ["بصراحة: سرقة بيانات البطاقات لاسلكياً في الشارع نادرة، لأن القارئ يجب أن يقترب جداً، والبيانات التي تُقرأ محدودة ولا تشمل عادة الرمز السري.", "لكن بطاقة الحجب رخيصة وخفيفة، وتعطيك راحة بال في الأماكن المزدحمة مثل المطارات ووسائل النقل والأسواق. لذلك نعتبرها احتياطاً بسيطاً، لا ضرورة قصوى."]),
    ("بطاقة حجب أم محفظة بحماية RFID؟", ["• بطاقة الحجب: تضعها في محفظتك الحالية، رخيصة، وتحمي البطاقات الملاصقة لها فقط.", "• المحفظة المحمية: الحماية مدمجة في كل الجيوب، فتحمي كل البطاقات معاً، لكنها أغلى وتعني تغيير محفظتك.", "إن كانت محفظتك جيدة وتريد حلاً سريعاً، ابدأ بالبطاقة."]),
    ("كيف تستعملها بشكل صحيح؟", ["• ضع البطاقة في نفس الخانة مع بطاقاتك، أو بين بطاقتين.", "• لا تتوقع أن تحمي بطاقة في جيب آخر.", "• جرّبها بنفسك: عند جهاز الدفع، قرّب محفظتك دون إخراج البطاقة. إن لم يقرأها الجهاز فالحجب يعمل.", "• عند الدفع باللمس أخرج بطاقتك من المحفظة."]),
    ("ما الذي نتجنّبه عند الاختيار؟", ["• عبارات مثل «حماية 100%» أو «أقوى تقنية في العالم»: لا توجد حماية مطلقة.", "• البطاقات السميكة جداً التي تضغط المحفظة.", "• المنتجات دون صور واضحة للبطاقة نفسها أو دون تقييمات حقيقية."])
   ],
   "faq": [("هل تؤثر بطاقة الحجب على بطاقتي البنكية؟", "لا، هي لا تمسح بيانات البطاقة ولا تتلفها، فقط تمنع قراءتها لاسلكياً ما دامت بجانبها."), ("هل تحمي جواز السفر؟", "نعم إن وضعتها ملاصقة لصفحة الشريحة داخل غلاف الجواز."), ("هل أحتاج بطاقة لكل بطاقة بنكية؟", "غالباً تكفي بطاقة واحدة لحماية البطاقات الملاصقة لها في نفس الخانة.")]
  },
  "en": {
   "title": "RFID blocking cards: do you really need one?",
   "card": "Best RFID blocking cards and wallets",
   "cardp": "What actually protects your cards, and what is marketing.",
   "lead": "An honest guide for anyone carrying contactless bank cards or a modern passport: how blocking works, when it helps, and how to choose and use a blocking card properly.",
   "sections": [
    ("What is RFID and NFC skimming?", ["Tap-to-pay cards and biometric passports carry a small chip that works at 13.56 MHz. When a reader comes close, the chip exchanges some data without contact.", "A blocking card uses a metal layer that interferes with this frequency, so nearby readers struggle to talk to the cards next to it."]),
    ("How big is the risk, really?", ["Honestly, wireless card theft on the street is rare: a reader has to get very close, and the data it can read is limited and usually excludes your PIN.", "Still, a blocking card is cheap and light, and gives peace of mind in crowded places such as airports, public transport and markets. Think of it as a simple precaution, not an essential."]),
    ("Blocking card or RFID wallet?", ["• Blocking card: goes into the wallet you already own, cheap, protects only the cards right next to it.", "• RFID wallet: shielding is built into every slot, so all cards are covered, but it costs more and means replacing your wallet.", "If your wallet is fine and you want a quick fix, start with a card."]),
    ("How to use it properly", ["• Put the card in the same slot as your bank cards, or between two of them.", "• Do not expect it to protect a card in another pocket.", "• Test it yourself: hold your closed wallet to a payment terminal. If the terminal cannot read your card, the blocking works.", "• Take your card out of the wallet when you pay by tap."]),
    ("What we avoid when choosing", ["• Claims such as \"100% protection\" or \"the strongest technology in the world\": no protection is absolute.", "• Very thick cards that stretch your wallet.", "• Listings without clear photos of the card itself or without real reviews."])
   ],
   "faq": [("Does a blocking card harm my bank card?", "No. It does not erase or damage your card; it only stops wireless reading while it sits next to it."), ("Does it protect a passport?", "Yes, if you place it against the chip page inside the passport cover."), ("Do I need one per bank card?", "Usually one card protects the cards right next to it in the same slot.")]
  }
 },
 {
  "slug": "online-teacher-kit",
  "picks": ["lenovo-thinkplus-tws-earbuds", "8-in-2-usb-hub-with-card-reader", "foldable-laptop-stand-10-heights", "11-5-inch-lcd-writing-pad-with-folio-case", "lenovo-xiaoxin-pad-11-2025-6-gb-128-gb"],
  "deals": "class",
  "ar": {
   "title": "حقيبة الأستاذ للتدريس عن بعد",
   "card": "حقيبة الأستاذ للتدريس عن بعد",
   "cardp": "سماعات وموزّع وحامل ولوح كتابة لدروس واضحة ومريحة.",
   "lead": "ما يحتاجه الأستاذ فعلاً ليقدّم درساً عن بعد بصوت واضح ووضعية مريحة وشرح مرئي، مرتّب حسب الأولوية، مع ما يناسب الميزانية الصغيرة.",
   "sections": [
    ("ابدأ بالصوت: أهم من الكاميرا", ["التلاميذ يتحمّلون صورة متوسطة، لكنهم لا يتحمّلون صوتاً متقطعاً أو بعيداً. سماعات لاسلكية بميكروفون قريب من فمك تحسّن الدرس أكثر من أي كاميرا غالية.", "اختر سماعات ببلوتوث حديث واتصال ثابت، وتأكّد أنها مريحة لساعة كاملة."]),
    ("وضعية جلوس صحيحة: حامل الحاسوب", ["ساعات أمام حاسوب محمول على الطاولة تعني رقبة منحنية. حامل يرفع الشاشة إلى مستوى العين يخفّف التعب، ويجعل الكاميرا أمام وجهك بدل أن تصوّر ذقنك.", "إن رفعت الحاسوب، فاستعمل لوحة مفاتيح وفأرة منفصلتين إن أمكن."]),
    ("منافذ إضافية: الموزّع", ["الحواسيب الحديثة فيها منافذ قليلة. الموزّع يتيح لك توصيل الفأرة ولوحة المفاتيح وقارئ بطاقة الذاكرة معاً.", "انتبه: إن كنت تريد توصيل الحاسوب بجهاز العرض (البروجكتور) في القسم، فاختر موزّعاً فيه منفذ HDMI."]),
    ("الشرح المرئي: لوح الكتابة أو الجهاز اللوحي", ["• لوح الكتابة LCD: رخيص، دون شاشة مضيئة، ممتاز للمسودات والحساب السريع، لكنه لا يحفظ ولا يرسل ما تكتبه.", "• الجهاز اللوحي: يتيح الكتابة على الشرائح ومشاركة الشاشة في الحصة، لكنه أغلى ويحتاج إعداداً.", "إن كانت ميزانيتك محدودة، ابدأ باللوح وصوّر ما تكتبه بالهاتف."]),
    ("ترتيب الشراء حسب الميزانية", ["1. السماعات (الأهم).", "2. حامل الحاسوب.", "3. الموزّع إن كانت منافذك لا تكفي.", "4. لوح الكتابة أو الجهاز اللوحي للشرح المرئي."])
   ],
   "faq": [("هل تكفي سماعات الهاتف العادية؟", "تعمل، لكن الميكروفون البعيد يلتقط ضجيج الغرفة. السماعات اللاسلكية بميكروفون قريب أوضح."), ("هل يصلح الموزّع لجهاز العرض؟", "فقط إن كان فيه منفذ HDMI. الموزّع الذي نعرضه حالياً ليس فيه HDMI."), ("لوح LCD أم جهاز لوحي؟", "اللوح للمسودات السريعة والميزانية الصغيرة، والجهاز اللوحي لمن يريد الكتابة على الدرس ومشاركته مباشرة.")]
  },
  "en": {
   "title": "The online teacher's starter kit",
   "card": "The online teacher's starter kit",
   "cardp": "Earbuds, a hub, a stand and a writing pad for clear, comfortable lessons.",
   "lead": "What a teacher actually needs to give a remote lesson with clear sound, a comfortable posture and visual explanations, in order of priority and with options for a small budget.",
   "sections": [
    ("Start with sound, not the camera", ["Pupils tolerate an average picture, but not choppy or distant sound. Wireless earbuds with a microphone near your mouth improve a lesson more than any expensive webcam.", "Choose earbuds with recent Bluetooth and a stable connection, and make sure they stay comfortable for a full hour."]),
    ("Posture: a laptop stand", ["Hours in front of a laptop flat on the desk mean a bent neck. A stand that lifts the screen to eye level reduces fatigue and puts the camera in front of your face instead of under your chin.", "If you raise the laptop, use a separate keyboard and mouse when you can."]),
    ("More ports: a USB hub", ["Modern laptops have few ports. A hub lets you connect a mouse, a keyboard and a memory card reader at once.", "Note: to connect your laptop to a classroom projector, choose a hub with an HDMI port."]),
    ("Visual explanations: writing pad or tablet", ["• LCD writing pad: cheap, no glowing screen, great for drafts and quick sums, but it cannot save or send what you write.", "• Tablet: lets you annotate slides and share your screen in class, but costs more and needs setting up.", "On a tight budget, start with the pad and photograph what you write with your phone."]),
    ("What to buy first", ["1. Earbuds (most important).", "2. Laptop stand.", "3. USB hub if your ports are not enough.", "4. Writing pad or tablet for visual explanations."])
   ],
   "faq": [("Are ordinary phone earphones enough?", "They work, but a distant microphone picks up room noise. Wireless earbuds with a close microphone sound clearer."), ("Does the hub work with a projector?", "Only if it has an HDMI port. The hub we list right now has no HDMI."), ("LCD pad or tablet?", "The pad suits quick drafts and small budgets; the tablet suits teachers who want to annotate and share lessons live.")]
  }
 },
 {
  "slug": "carry-on-tech-checklist",
  "picks": ["pocket-monocular-with-phone-clip", "v500-obd2-car-diagnostic-scanner", "rfid-nfc-blocking-card"],
  "deals": "travel",
  "ar": {
   "title": "قائمة تقنيات حقيبة اليد للسفر",
   "card": "قائمة تقنيات حقيبة اليد",
   "cardp": "محوّلات وبطاريات وأجهزة تتبّع وما يُسمح به في الطائرة.",
   "lead": "قائمة عملية لما تضعه في حقيبة اليد قبل أي رحلة، بالطائرة أو بالسيارة، مع القواعد التي يجب معرفتها عن البطاريات في المطار.",
   "sections": [
    ("الأساسيات قبل أي رحلة", ["• محوّل سفر عالمي، لأن أشكال المقابس تختلف بين الدول.", "• بطارية خارجية وكابل شحن قصير.", "• شريحة تتبّع في الحقيبة المشحونة لتعرف مكانها إن تأخرت.", "• بطاقة حماية RFID لبطاقاتك وجوازك في المطار والأماكن المزدحمة."]),
    ("قواعد البطاريات في الطائرة", ["القاعدة العامة لدى أغلب شركات الطيران: البطاريات الخارجية تُحمل في حقيبة اليد فقط، وليس في الحقيبة المشحونة، والبطاريات حتى 100 واط/ساعة مسموحة عادة دون إذن خاص.", "بطارية 10,000 ميلي أمبير تعادل نحو 37 واط/ساعة، فهي ضمن المسموح بسهولة. لكن تحقّق دائماً من شروط شركة الطيران قبل السفر."]),
    ("محوّل السفر: ما الذي تبحث عنه؟", ["• يغطي المقابس الأوروبية والبريطانية والأمريكية والأسترالية.", "• فيه منافذ USB-C وUSB-A لشحن الهاتف والسماعات معاً.", "• تذكّر أن المحوّل لا يغيّر الجهد الكهربائي، فتأكّد أن شاحن جهازك يدعم 100 إلى 240 فولت (أغلب شواحن الهواتف تدعم ذلك)."]),
    ("لرحلات الطريق بالسيارة", ["جهاز تشخيص OBD2 يقرأ رموز أعطال المحرك قبل الانطلاق، فتعرف هل ضوء «فحص المحرك» تحذير بسيط أم يحتاج ميكانيكياً. وهو مفيد أيضاً عند شراء سيارة مستعملة.", "وللنزهات في الطبيعة، منظار صغير للجيب يضيف متعة لمراقبة الطيور والمناظر البعيدة، بتوقعات واقعية للتكبير."]),
    ("نصيحة أخيرة", ["ضع كل الكابلات والمحوّل في حقيبة صغيرة واحدة، فهذا يسرّع التفتيش الأمني ولا تنسى شيئاً في الفندق."])
   ],
   "faq": [("هل أضع البطارية الخارجية في الحقيبة المشحونة؟", "لا. أغلب شركات الطيران تشترط حملها في حقيبة اليد."), ("هل يحوّل المحوّل الجهد الكهربائي؟", "لا، هو يغيّر شكل القابس فقط. تأكّد أن شاحنك يدعم 100 إلى 240 فولت."), ("هل تعمل شريحة التتبّع في كل مكان؟", "تعتمد على البلوتوث والهواتف القريبة، فتعمل أفضل في المطارات والمدن.")]
  },
  "en": {
   "title": "Carry-on tech checklist for travel",
   "card": "Carry-on tech checklist",
   "cardp": "Adapters, power banks, trackers, and what airlines allow.",
   "lead": "A practical list of what to pack in your carry-on before any trip, by plane or by car, with the battery rules you should know at the airport.",
   "sections": [
    ("The essentials for any trip", ["• A universal travel adapter, because plug shapes differ between countries.", "• A power bank and a short charging cable.", "• A tracker tag inside checked luggage, so you know where it is if it is delayed.", "• An RFID blocking card for your cards and passport at the airport and in crowds."]),
    ("Battery rules on planes", ["The general rule with most airlines: power banks go in carry-on only, never in checked luggage, and batteries up to 100 Wh are usually allowed without special approval.", "A 10,000 mAh power bank is about 37 Wh, well within the limit. Always check your airline's rules before you fly."]),
    ("Travel adapters: what to look for", ["• Covers European, UK, US and Australian sockets.", "• Has USB-C and USB-A ports to charge a phone and earbuds together.", "• An adapter does not convert voltage, so check that your charger supports 100–240 V (most phone chargers do)."]),
    ("For road trips", ["An OBD2 scanner reads engine fault codes before you set off, so you know whether a check-engine light is a minor warning or needs a mechanic. It also helps when buying a used car.", "For outings in nature, a pocket monocular adds fun for birdwatching and distant views, with realistic zoom expectations."]),
    ("One last tip", ["Keep every cable and the adapter in one small pouch. Security checks go faster and you will not leave anything in the hotel."])
   ],
   "faq": [("Can a power bank go in checked luggage?", "No. Most airlines require it in your carry-on."), ("Does an adapter convert voltage?", "No, it only changes the plug shape. Make sure your charger supports 100–240 V."), ("Do tracker tags work everywhere?", "They rely on Bluetooth and nearby phones, so they work best in airports and cities.")]
  }
 }
 ,{
  "slug": "wireless-qr-scanner-guide",
  "picks": [],
  "deals": "qrscan",
  "ar": {
   "title": "كيف تختار قارئ QR لاسلكياً لمحلك أو مؤسستك (دليل 2026)",
   "card": "أفضل قارئ QR لاسلكي للمحلات",
   "cardp": "2.4G أم بلوتوث؟ 1D أم 2D؟ وما مشكلة لوحة المفاتيح الفرنسية؟",
   "lead": "دليل عملي لأصحاب المحلات والصيدليات والمكتبات والمؤسسات: ما الفرق بين أنواع القارئات اللاسلكية، وما المواصفات التي تهمّك فعلاً، وكيف تتجنّب أشهر مشكلة عند الاستعمال في الجزائر.",
   "sections": [
    ("أولاً: هل تحتاج 1D أم 2D؟", ["القارئ 1D (ليزر أو CCD) يقرأ الباركود العادي ذا الخطوط فقط، ولا يقرأ رموز QR إطلاقاً.", "القارئ 2D (Imager) يقرأ الاثنين: الباركود العادي ورموز QR، ويقرأ أيضاً من شاشة الهاتف، وهذا ضروري للتذاكر والقسائم والدفع الإلكتروني وبطاقات الحضور المطبوعة بـQR.", "نصيحتنا: اختر 2D حتى لو كنت تستعمل الباركود العادي اليوم، فالفرق في السعر صار صغيراً."]),
    ("ثانياً: 2.4G أم بلوتوث أم الاثنان؟", ["• 2.4G: يأتي مع مستقبل USB صغير تضعه في الحاسوب. يعمل فوراً بلا إعداد، ومداه أكبر عادةً. مناسب للمحلات والمخازن.", "• بلوتوث: يتصل مباشرة بالهاتف أو اللوحة الإلكترونية أو الحاسوب دون مستقبل. مناسب لمن يعمل على تطبيق في الهاتف.", "• ثلاثي الاتصال (2.4G + بلوتوث + كابل USB): الخيار الأمرن، وإذا فرغت البطارية تستعمله بالكابل.", "انتبه: الأرقام المكتوبة في الإعلانات عن المدى (مثل 100 متر) تُقاس في مكان مفتوح بلا جدران. داخل المحل توقّع مدى أقل بكثير، وهو كافٍ عادةً."]),
    ("ثالثاً: المواصفات التي تهمّك فعلاً", ["• قراءة الشاشات: تأكّد أن الوصف يذكر قراءة الرموز من شاشة الهاتف (Screen reading).", "• وضع التخزين (Offline / Storage mode): يحفظ المسحات عندما تبتعد عن المستقبل، ثم يرسلها عند العودة. مفيد في الجرد.", "• البطارية: من 1500 إلى 2500 ميلي أمبير تكفي يوم عمل كامل في أغلب المحلات.", "• المتانة: ابحث عن مقاومة السقوط (مثلاً 1.5 متر)، فالقارئ يسقط كثيراً على أرضية المحل.", "• القاعدة (Stand): بعض القارئات تأتي بحامل يتحول فيه القارئ إلى مسح تلقائي دون ضغط الزر، وهذا مريح في نقطة البيع."]),
    ("أشهر مشكلة في الجزائر: لوحة المفاتيح الفرنسية AZERTY", ["القارئ يعمل كأنه لوحة مفاتيح تكتب الأرقام بسرعة. إذا كانت لوحة حاسوبك بالفرنسية (AZERTY) والقارئ مضبوط على الإنجليزية (QWERTY)، ستظهر رموز غريبة مثل «à&é» بدل الأرقام.", "الحل بسيط: في دليل القارئ صفحة رموز إعداد، امسح رمز «French keyboard / AZERTY» مرة واحدة فقط. أو اجعل لغة الإدخال في الحاسوب إنجليزية أثناء المسح.", "إذا لم تجد الدليل، اطلب ملف PDF من البائع في رسالة على علي إكسبريس قبل الشراء."]),
    ("ما الذي نتجنّبه عند الاختيار؟", ["• قارئ 1D يُباع على أنه «يقرأ كل الرموز».", "• منتج تقييمه أقل من 85% أو بلا مبيعات تُذكر.", "• وعود مثل «يقرأ أي رمز تالف» أو «مدى غير محدود»."])
   ],
   "faq": [("هل يحتاج القارئ اللاسلكي برنامج تعريف؟", "في الغالب لا. أغلب القارئات تعمل كلوحة مفاتيح (HID) مع Windows والهاتف دون تعريفات. ضع المؤشر في الخانة وامسح."), ("هل يعمل مع برنامج المحاسبة أو المخزون الذي أستعمله؟", "إذا كان برنامجك يقبل كتابة الرمز بلوحة المفاتيح، فسيعمل معه القارئ. الاستثناء النادر هو البرامج التي تتطلّب قارئاً بواجهة خاصة."), ("ما الفرق بينه وبين ماسح الخاتم؟", "ماسح الخاتم يُلبس في الإصبع ويترك اليدين حرّتين، وهو مناسب للمخازن والتغليف. لكن بطاريته أصغر وسعره أعلى عادةً."), ("كم يدوم شحن البطارية؟", "يختلف حسب الطراز وعدد المسحات. أغلب القارئات تكفي يوم عمل، وتُشحن ليلاً بكابل USB.")]
  },
  "en": {
   "title": "How to choose a wireless QR scanner for your shop or office (2026 guide)",
   "card": "Best wireless QR scanners for shops",
   "cardp": "2.4G or Bluetooth? 1D or 2D? And the AZERTY keyboard trap.",
   "lead": "A practical guide for shops, pharmacies, bookstores and offices: the difference between wireless scanner types, the specs that actually matter, and how to avoid the most common setup problem.",
   "sections": [
    ("First: 1D or 2D?", ["A 1D scanner (laser or CCD) reads classic line barcodes only. It cannot read QR codes at all.", "A 2D imager reads both line barcodes and QR codes, including from a phone screen, which you need for tickets, coupons, e-payments and QR attendance cards.", "Our advice: pick 2D even if you only use line barcodes today; the price gap is now small."]),
    ("Second: 2.4G, Bluetooth, or both?", ["• 2.4G: comes with a small USB receiver. Works instantly with no setup and usually has more range. Good for shops and storerooms.", "• Bluetooth: connects straight to a phone, tablet or computer with no receiver. Good if you work in a phone app.", "• Tri-mode (2.4G + Bluetooth + USB cable): the most flexible; if the battery dies, use it wired.", "Note: range figures in listings (e.g. 100 m) are measured in open space. Indoors, expect much less, which is usually still plenty."]),
    ("Third: the specs that actually matter", ["• Screen reading: make sure the listing mentions reading codes from phone screens.", "• Storage / offline mode: keeps scans when you walk out of range and sends them later. Useful for stocktaking.", "• Battery: 1500–2500 mAh covers a full working day in most shops.", "• Durability: look for a drop rating (e.g. 1.5 m); scanners get dropped a lot.", "• Stand: some come with a cradle that turns on hands-free auto-scan, handy at the checkout."]),
    ("The most common problem: AZERTY keyboards", ["The scanner types like a keyboard. If your computer uses a French AZERTY layout and the scanner is set to US QWERTY, you get symbols like \"à&é\" instead of digits.", "The fix: scan the \"French keyboard / AZERTY\" setup code in the scanner manual once, or switch your input language to English while scanning.", "No manual? Ask the seller for the PDF on AliExpress before you buy."]),
    ("What we avoid when choosing", ["• A 1D scanner sold as \"reads every code\".", "• Products rated under 85% or with almost no sales.", "• Promises like \"reads any damaged code\" or \"unlimited range\"."])
   ],
   "faq": [("Does a wireless scanner need drivers?", "Usually not. Most work as a keyboard (HID) with Windows and phones. Click into the field and scan."), ("Will it work with my billing or stock software?", "If your software accepts typed codes from a keyboard, the scanner will work. Rare exceptions need a special scanner interface."), ("How is it different from a ring scanner?", "A ring scanner is worn on a finger and leaves both hands free, ideal for picking and packing, but it has a smaller battery and usually costs more."), ("How long does the battery last?", "It depends on the model and scan count. Most last a working day and recharge overnight over USB.")]
  }
 },
 {
  "slug": "wireless-charger-guide",
  "picks": [],
  "deals": "wcharge",
  "ar": {
   "title": "كيف تختار شاحناً لاسلكياً: Qi أم Qi2؟ وهل 3 في 1 يناسب هاتفك؟",
   "card": "كيف تختار شاحناً لاسلكياً",
   "cardp": "Qi وQi2 والمغناطيس والساعة: ما يناسب هاتفك فعلاً.",
   "lead": "قبل أن تشتري محطة شحن لاسلكية 3 في 1، تأكّد من أربعة أشياء: معيار الشحن الذي يدعمه هاتفك، ونوع ساعتك، والمحوّل الكهربائي، وسُمك الغطاء. هذا الدليل يشرحها ببساطة.",
   "sections": [
    ("Qi أم Qi2؟", ["Qi هو المعيار القديم الشائع: تضع الهاتف على القاعدة فيشحن، لكن يجب أن يكون في المكان الصحيح تماماً.", "Qi2 هو المعيار الأحدث: فيه مغناطيس يثبّت الهاتف في الموضع الصحيح تلقائياً، وقدرته تصل إلى 15 واط. تدعمه هواتف iPhone الحديثة وعدد متزايد من هواتف أندرويد.", "إذا كان هاتفك لا يدعم الشحن المغناطيسي، فالشاحن المغناطيسي يحتاج غطاءً مغناطيسياً أو حلقة لاصقة ليثبت."]),
    ("انتبه للساعة قبل شراء 3 في 1", ["أغلب محطات 3 في 1 مصمّمة لساعة Apple Watch، أو تأتي بقاعدة لنوع معيّن من ساعات Samsung.", "ساعات كثيرة أخرى تُشحن بكابل خاص بها ولا تعمل على هذه المحطات. اقرأ قائمة الأجهزة المتوافقة في صفحة المنتج قبل الشراء."]),
    ("المحوّل الكهربائي: السبب الأول للشحن البطيء", ["كثير من المحطات تأتي بكابل فقط بلا محوّل، وتحتاج محوّلاً سريعاً (PD) بقدرة 20 واط أو أكثر حسب ما يذكره البائع.", "مع محوّل ضعيف تشحن ببطء أو تتوقف عن شحن أحد الأجهزة."]),
    ("الغطاء والحرارة: توقعات واقعية", ["• الغطاء السميك (أكثر من نحو 5 ملم) أو الذي فيه بطاقات أو معدن يضعف الشحن أو يمنعه.", "• الشحن اللاسلكي أبطأ من الكابل، ويسخن الهاتف قليلاً، وهذا طبيعي.", "• ميزته الحقيقية الراحة والترتيب: تضع أجهزتك ليلاً وتنسى الكوابل."]),
    ("ما الذي نتجنّبه عند الاختيار؟", ["• أرقام قدرة مبالغ فيها لا يدعمها هاتفك أصلاً.", "• منتجات بلا قائمة توافق واضحة للساعات.", "• تقييم أقل من 85%."])
   ],
   "faq": [("هل الشحن اللاسلكي يضر البطارية؟", "لا يضرها بشكل يُذكر عند استعمال شاحن جيد. الحرارة الزائدة هي ما يضر، لذلك تجنّب الشحن تحت الوسادة أو في الشمس."), ("هل يعمل الشاحن اللاسلكي مع أي هاتف؟", "فقط مع الهواتف التي تدعم الشحن اللاسلكي Qi أو Qi2. تحقّق من مواصفات هاتفك."), ("لماذا يتوقف الشحن أحياناً؟", "غالباً بسبب محوّل ضعيف، أو غطاء سميك، أو أن الهاتف ليس في المكان الصحيح على القاعدة."), ("هل أحتاج شاحناً بـ15 واط؟", "فقط إذا كان هاتفك يدعم هذه القدرة. وإلا فسيشحن بالقدرة القصوى لهاتفه.")]
  },
  "en": {
   "title": "How to choose a wireless charger: Qi or Qi2? Is a 3-in-1 right for you?",
   "card": "How to choose a wireless charger",
   "cardp": "Qi, Qi2, magnets and watches: what really fits your phone.",
   "lead": "Before you buy a 3-in-1 wireless station, check four things: the charging standard your phone supports, your watch type, the power adapter, and your case thickness. This guide keeps it simple.",
   "sections": [
    ("Qi or Qi2?", ["Qi is the common older standard: put the phone on the pad and it charges, but placement must be just right.", "Qi2 is newer: magnets snap the phone into the right spot, with up to 15 W. Recent iPhones and a growing number of Android phones support it.", "If your phone has no magnetic charging, a magnetic charger needs a magnetic case or stick-on ring to hold it."]),
    ("Check your watch before buying a 3-in-1", ["Most 3-in-1 stations are built for Apple Watch, or include a puck for specific Samsung watches.", "Many other watches use their own cable and will not work. Read the compatibility list on the product page first."]),
    ("The adapter: the #1 cause of slow charging", ["Many stations ship with a cable only and need a fast PD adapter of 20 W or more, as stated by the seller.", "With a weak adapter they charge slowly or drop one of the devices."]),
    ("Case and heat: realistic expectations", ["• Thick cases (over roughly 5 mm) or cases with cards or metal weaken or block charging.", "• Wireless charging is slower than a cable and the phone gets a little warm; that is normal.", "• The real benefit is comfort and a tidy desk: drop your devices at night and forget the cables."]),
    ("What we avoid when choosing", ["• Inflated wattage your phone cannot even use.", "• Products without a clear watch compatibility list.", "• Ratings under 85%."])
   ],
   "faq": [("Does wireless charging damage the battery?", "Not meaningfully with a good charger. Excess heat is what hurts, so avoid charging under a pillow or in the sun."), ("Does it work with any phone?", "Only with phones that support Qi or Qi2 wireless charging. Check your phone specs."), ("Why does charging stop sometimes?", "Usually a weak adapter, a thick case, or the phone being off-center on the pad."), ("Do I need a 15 W charger?", "Only if your phone supports it; otherwise it charges at your phone's own maximum.")]
  }
 }
]

# ---- Guides added by the weekly guides agent (JSON, same structure; lists instead of tuples) ----
import json as _json, os as _os
_EXTRA = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "guides_extra.json")
if _os.path.exists(_EXTRA):
    for _g in _json.load(open(_EXTRA, encoding="utf-8")):
        for _L in ("ar", "en"):
            _g[_L]["sections"] = [tuple(s) for s in _g[_L]["sections"]]
            _g[_L]["faq"] = [tuple(f) for f in _g[_L]["faq"]]
        _g.setdefault("picks", [])
        GUIDES.append(_g)
