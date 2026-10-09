import google.generativeai as genai


# ==================================================
# SECTION 1: TOPIC BREAKDOWN
# ==================================================

def prompt_topic_breakdown(user_text):
    lines = []
    lines.append("তুমি একজন BCS/সরকারি চাকরি পরীক্ষার বিশেষজ্ঞ শিক্ষক।")
    lines.append("")
    lines.append("নিচের টপিক/আর্টিকেলটা পড়ো এবং বিশ্লেষণ করো এই বিষয়টা সম্পূর্ণভাবে বুঝতে একজন পরীক্ষার্থীর কী কী উপ-বিষয়/দিক জানা দরকার।")
    lines.append("")
    lines.append("মূল টপিক/টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## ১. বিষয়ের পরিচিতি ও সংজ্ঞা")
    lines.append("(টপিকটা আসলে কী, সংক্ষিপ্ত সংজ্ঞা/প্রেক্ষাপট)")
    lines.append("")
    lines.append("## ২. মূল উপ-বিষয়সমূহ (যা জানা দরকার)")
    lines.append("- পয়েন্ট আকারে ৬-৮টা উপ-বিষয়/দিক লেখো যেগুলো এই টপিক বুঝতে গুরুত্বপূর্ণ")
    lines.append("- প্রতিটা পয়েন্টের সাথে ১ লাইন ব্যাখ্যা দাও")
    lines.append("")
    lines.append("## ৩. এই টপিক কেন গুরুত্বপূর্ণ (পরীক্ষার দৃষ্টিকোণ থেকে)")
    lines.append("(২-৩ লাইনে বলো কেন এটা BCS/সরকারি চাকরির জন্য গুরুত্বপূর্ণ)")
    lines.append("")
    lines.append("নিয়ম: তথ্য নির্ভুল রাখো, বানিয়ে কিছু বোলো না।")
    return "\n".join(lines)


# ==================================================
# SECTION 2: BANGLADESH LAW MAPPING
# ==================================================

def prompt_bd_law_mapping(user_text, context_institutions):
    context_lines = []
    if context_institutions:
        for i in context_institutions:
            name_bn = i.get("name_bn", "")
            name_en = i.get("name_en", "")
            abbr = i.get("abbr", "")
            role = i.get("role", "")
            context_lines.append("- " + name_bn + " (" + name_en + ", " + abbr + ") - " + role)
    if not context_lines:
        context_lines.append("কোনো প্রাসঙ্গিক প্রতিষ্ঠান ডেটাবেসে পাওয়া যায়নি, নিজের নির্ভুল জ্ঞান ব্যবহার করো।")
    context_str = "\n".join(context_lines)

    lines = []
    lines.append("তুমি একজন বাংলাদেশের আইন ও সংবিধান বিশেষজ্ঞ।")
    lines.append("")
    lines.append("মূল টপিক/টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("প্রাসঙ্গিক প্রতিষ্ঠান/মন্ত্রণালয় তথ্য (সহায়ক):")
    lines.append(context_str)
    lines.append("")
    lines.append("কাজ: এই টপিকের সাথে বাংলাদেশের কোন কোন আইন, নীতিমালা, অধ্যাদেশ বা বিধি সম্পর্কিত তা খুঁজে বের করো এবং কিভাবে সম্পর্কিত তা ব্যাখ্যা করো।")
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## বাংলাদেশের প্রাসঙ্গিক আইন ও নীতিমালা")
    lines.append("")
    lines.append("| আইন/নীতিমালার নাম | প্রণয়নকাল | এই টপিকের সাথে সম্পর্ক |")
    lines.append("|---|---|---|")
    lines.append("| ... | ... | ... |")
    lines.append("")
    lines.append("## দায়িত্বপ্রাপ্ত মন্ত্রণালয়/প্রতিষ্ঠান")
    lines.append("- প্রতিষ্ঠানের নাম (সংক্ষিপ্ত রূপ) - এই টপিকে তার ভূমিকা/দায়িত্ব")
    lines.append("")
    lines.append("নিয়ম:")
    lines.append("- বাস্তবে অস্তিত্ব নেই এমন আইনের নাম বানিয়ে বোলো না")
    lines.append("- আইনের নাম সঠিক ও হালনাগাদ রাখো")
    lines.append("- যদি কোনো সুনির্দিষ্ট আইন না থাকে, স্পষ্ট করে বলো যে নেই")
    return "\n".join(lines)


# ==================================================
# SECTION 3: CONSTITUTION
# ==================================================

def prompt_constitution(user_text):
    lines = []
    lines.append("তুমি বাংলাদেশের সংবিধান বিশেষজ্ঞ।")
    lines.append("")
    lines.append("মূল টপিক/টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("কাজ: বাংলাদেশের সংবিধানের কোন কোন অনুচ্ছেদ (Article) এই বিষয়ের সাথে সরাসরি বা পরোক্ষভাবে সম্পর্কিত তা খুঁজে বের করো।")
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## সংবিধান কী বলে")
    lines.append("")
    lines.append("| অনুচ্ছেদ নম্বর | অনুচ্ছেদের বিষয়বস্তু | এই টপিকের সাথে সম্পর্ক |")
    lines.append("|---|---|---|")
    lines.append("| ... | ... | ... |")
    lines.append("")
    lines.append("## মূলনীতি হিসেবে প্রাসঙ্গিকতা")
    lines.append("(যদি মৌলিক অধিকার বা রাষ্ট্র পরিচালনার মূলনীতির সাথে সম্পর্কিত হয়, তা ব্যাখ্যা করো)")
    lines.append("")
    lines.append("নিয়ম:")
    lines.append("- ভুল অনুচ্ছেদ নম্বর বানিয়ে বোলো না")
    lines.append("- নিশ্চিত না হলে বলো যে সাধারণভাবে সম্পর্কিত, নির্দিষ্ট অনুচ্ছেদ যাচাই করা উচিত")
    return "\n".join(lines)


# ==================================================
# SECTION 4: INTERNATIONAL LAW
# ==================================================

def prompt_international_law(user_text):
    lines = []
    lines.append("তুমি আন্তর্জাতিক আইন ও সম্পর্ক বিশেষজ্ঞ।")
    lines.append("")
    lines.append("মূল টপিক/টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("কাজ: এই বিষয়ের সাথে সম্পর্কিত আন্তর্জাতিক আইন, কনভেনশন, চুক্তি, প্রোটোকল বা তাত্ত্বিক ধারণা থাকলে তা ব্যাখ্যা করো।")
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## আন্তর্জাতিক আইন/কনভেনশন/চুক্তি")
    lines.append("- নাম (সংক্ষিপ্ত রূপ, সাল) - মূল বিষয়বস্তু ও সম্পর্ক")
    lines.append("- বাংলাদেশ স্বাক্ষরকারী কিনা উল্লেখ করো (জানা থাকলে)")
    lines.append("")
    lines.append("## প্রাসঙ্গিক তত্ত্ব/ধারণা (যদি থাকে)")
    lines.append("- তত্ত্বের নাম - প্রবক্তা - মূল বক্তব্য - সংযোগ")
    lines.append("")
    lines.append("## আন্তর্জাতিক সংস্থার ভূমিকা")
    lines.append("- সংস্থার নাম (UN, World Bank, IMF, UNDP, WHO ইত্যাদি) - ভূমিকা/সূচক")
    lines.append("")
    lines.append("নিয়ম: সরাসরি প্রযোজ্য না হলে স্পষ্ট করে বলো কোনো সুনির্দিষ্ট আন্তর্জাতিক আইন নেই, বানিয়ে বোলো না।")
    return "\n".join(lines)


# ==================================================
# SECTION 5: COMPARATIVE COUNTRIES
# ==================================================

def prompt_comparative_countries(user_text):
    lines = []
    lines.append("তুমি তুলনামূলক নীতি বিশ্লেষণ বিশেষজ্ঞ।")
    lines.append("")
    lines.append("মূল টপিক/টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("কাজ: যদি এটি একটি সমস্যা/চ্যালেঞ্জ হয়ে থাকে, তাহলে বিশ্বের অন্তত ২-৩টি দেশ এই একই ধরনের সমস্যা কিভাবে মোকাবেলা করেছে তার বিস্তারিত বিবরণ দাও।")
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## আন্তর্জাতিক দৃষ্টান্ত (কেস স্টাডি)")
    lines.append("")
    lines.append("### দেশ ১: (দেশের নাম লেখো)")
    lines.append("- সমস্যা কেমন ছিল")
    lines.append("- কী পদক্ষেপ নেওয়া হয়েছিল (সুনির্দিষ্ট নীতি/প্রকল্প/আইনের নাম সহ)")
    lines.append("- ফলাফল কী হয়েছে")
    lines.append("")
    lines.append("### দেশ ২: (দেশের নাম লেখো)")
    lines.append("(একই কাঠামোতে)")
    lines.append("")
    lines.append("### দেশ ৩: (যদি প্রাসঙ্গিক হয়)")
    lines.append("(একই কাঠামোতে)")
    lines.append("")
    lines.append("## বাংলাদেশ কী শিখতে পারে")
    lines.append("- প্রয়োগযোগ্য ৩-৪টি শিক্ষা পয়েন্ট আকারে দাও")
    lines.append("")
    lines.append("নিয়ম: বাস্তব, সত্যিকারের দেশ ও নীতির উদাহরণ দাও, কাল্পনিক কিছু বানিয়ো না।")
    return "\n".join(lines)


# ==================================================
# SECTION 6: GOVERNMENT RESPONSE
# ==================================================

def prompt_government_response(user_text, context_institutions):
    context_lines = []
    if context_institutions:
        for i in context_institutions:
            name_bn = i.get("name_bn", "")
            abbr = i.get("abbr", "")
            role = i.get("role", "")
            context_lines.append("- " + name_bn + " (" + abbr + ") - " + role)
    context_str = "\n".join(context_lines)

    lines = []
    lines.append("তুমি বাংলাদেশের নীতি বিশ্লেষক।")
    lines.append("")
    lines.append("মূল টপিক/টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("প্রাসঙ্গিক প্রতিষ্ঠান তথ্য:")
    lines.append(context_str)
    lines.append("")
    lines.append("কাজ: যদি এটি একটি সমস্যা/চ্যালেঞ্জ সংক্রান্ত টপিক হয়, তাহলে নিচের কাঠামোয় বিশ্লেষণ দাও। সমস্যা না হলে প্রাসঙ্গিক সরকারি কার্যক্রম নিয়ে লেখো।")
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## সরকারের গৃহীত পদক্ষেপ")
    lines.append("- নির্দিষ্ট মন্ত্রণালয়/অধিদপ্তর/প্রকল্পের নাম সহ কী কী পদক্ষেপ নেওয়া হয়েছে")
    lines.append("")
    lines.append("## বিদ্যমান চ্যালেঞ্জ ও সীমাবদ্ধতা")
    lines.append("- বাস্তবায়নে কী কী বাধা/সমস্যা আছে")
    lines.append("")
    lines.append("## সম্ভাব্য করণীয় (Way Forward)")
    lines.append("- কোন প্রতিষ্ঠান কী ভূমিকা রাখতে পারে, স্বল্প ও দীর্ঘমেয়াদী সুপারিশ")
    lines.append("")
    lines.append("নিয়ম: বাস্তবে নেই এমন প্রকল্প/পরিসংখ্যান বানিয়ে বোলো না।")
    return "\n".join(lines)


# ==================================================
# SECTION 7: FINAL SYNTHESIS
# ==================================================

def prompt_final_synthesis(user_text, all_sections_text):
    lines = []
    lines.append("তুমি একজন অভিজ্ঞ BCS লেখক ও সম্পাদক।")
    lines.append("")
    lines.append("নিচে একটা টপিকের উপর বিভিন্ন ধাপে তৈরি করা বিশ্লেষণের অংশ দেওয়া আছে। এগুলো একত্রিত করে সংক্ষিপ্ত সারাংশ তৈরি করো।")
    lines.append("")
    lines.append("মূল টপিক:")
    lines.append(user_text)
    lines.append("")
    lines.append("বিভিন্ন অংশের তথ্য:")
    lines.append(all_sections_text)
    lines.append("")
    lines.append("কাজ: উপরের সবকিছু থেকে একটা Executive Summary এবং Quick Revision Flashcard তৈরি করো।")
    lines.append("")
    lines.append("আউটপুট ফরম্যাট (বাংলা):")
    lines.append("")
    lines.append("## Executive Summary (৫-৭ লাইনে সম্পূর্ণ সারমর্ম)")
    lines.append("...")
    lines.append("")
    lines.append("## Quick Revision Flashcard")
    lines.append("- গুরুত্বপূর্ণ আইন: ...")
    lines.append("- গুরুত্বপূর্ণ সংবিধান অনুচ্ছেদ: ...")
    lines.append("- গুরুত্বপূর্ণ আন্তর্জাতিক কনভেনশন: ...")
    lines.append("- গুরুত্বপূর্ণ দেশের দৃষ্টান্ত: ...")
    lines.append("- গুরুত্বপূর্ণ প্রতিষ্ঠান: ...")
    lines.append("- সম্ভাব্য পরীক্ষার প্রশ্ন (২টা তৈরি করো)")
    return "\n".join(lines)


# ==================================================
# ENHANCE MODE (Quick mode)
# ==================================================

def build_enhance_prompt(user_text, context_institutions, length_mode):
    context_lines = []
    if context_institutions:
        for i in context_institutions:
            name_bn = i.get("name_bn", "")
            name_en = i.get("name_en", "")
            abbr = i.get("abbr", "")
            role = i.get("role", "")
            context_lines.append("- " + name_bn + " (" + name_en + ", " + abbr + ") - " + role)
    if not context_lines:
        context_lines.append("প্রাসঙ্গিক কিছু পাওয়া যায়নি, নিজের নির্ভুল জ্ঞান ব্যবহার করো।")
    context_str = "\n".join(context_lines)

    length_map = {
        "short": "৩-৪ লাইনে সংক্ষিপ্ত রাখো।",
        "medium": "৮-১০ লাইনে লেখো।",
        "long": "বিস্তারিত অনুচ্ছেদ লেখো।"
    }
    length_instruction = length_map.get(length_mode, "৮-১০ লাইনে লেখো।")

    lines = []
    lines.append("তুমি একজন বিশেষজ্ঞ BCS লেখার সহকারী।")
    lines.append("")
    lines.append("কাজ: নিচের generic বাক্যকে rewrite করো যাতে প্রাসঙ্গিক মন্ত্রণালয়/প্রতিষ্ঠান/আইনের নাম উল্লেখ থাকে।")
    lines.append("")
    lines.append("প্রাসঙ্গিক তথ্য:")
    lines.append(context_str)
    lines.append("")
    lines.append("মূল টেক্সট:")
    lines.append(user_text)
    lines.append("")
    lines.append("নির্দেশনা: " + length_instruction)
    lines.append("")
    lines.append("আউটপুট:")
    lines.append("### বাংলা উন্নত সংস্করণ:")
    lines.append("...")
    lines.append("### English Enhanced Version:")
    lines.append("...")
    lines.append("### ব্যবহৃত প্রতিষ্ঠান/আইন:")
    lines.append("- ...")
    lines.append("")
    lines.append("নিয়ম: বাস্তবে নেই এমন কিছু বানিয়ো না।")
    return "\n".join(lines)
# ==================================================
# SECTION 8: ENGLISH HOOK + 4+4+4 + CONCLUSION ESSAY
# ==================================================

def prompt_hook_essay(user_text, context_institutions):
    context_lines = []
    if context_institutions:
        for i in context_institutions:
            name_bn = i.get("name_bn", "")
            name_en = i.get("name_en", "")
            abbr = i.get("abbr", "")
            role = i.get("role", "")
            context_lines.append("- " + name_en + " (" + abbr + ") - " + role)
    if not context_lines:
        context_lines.append("No specific institution data found, use your own accurate knowledge.")
    context_str = "\n".join(context_lines)

    lines = []
    lines.append("You are an elite English essay writing coach specializing in BCS/competitive exam writing with native-level command of sophisticated vocabulary, varied sentence structures, and advanced clause usage (relative clauses, subordinate clauses, participial phrases, cleft sentences).")
    lines.append("")
    lines.append("TASK: Write a polished, exam-ready English essay/answer on the topic below, strictly following the HOOK + 4+4+4 + CONCLUSION structure.")
    lines.append("")
    lines.append("Relevant background information (use where applicable, do not force irrelevant facts):")
    lines.append(context_str)
    lines.append("")
    lines.append("TOPIC / SOURCE TEXT:")
    lines.append(user_text)
    lines.append("")
    lines.append("STRUCTURE TO FOLLOW STRICTLY:")
    lines.append("")
    lines.append("### HOOK (1-2 sentences)")
    lines.append("Open with a striking statistic, a rhetorical question, a bold claim, or a vivid contrast that immediately grabs the examiner's attention and introduces the topic's significance.")
    lines.append("")
    lines.append("### BODY PARAGRAPH 1 - 4 points")
    lines.append("Present exactly 4 well-developed sentences/points on the FIRST major dimension of the topic (e.g., causes/background). Each sentence must use sophisticated vocabulary and at least one subordinate/relative clause. Mention specific institutions, laws, or data where relevant.")
    lines.append("")
    lines.append("### BODY PARAGRAPH 2 - 4 points")
    lines.append("Present exactly 4 well-developed sentences/points on the SECOND major dimension (e.g., impacts/challenges). Same stylistic requirement: rich vocabulary, complex sentence structures, specific references.")
    lines.append("")
    lines.append("### BODY PARAGRAPH 3 - 4 points")
    lines.append("Present exactly 4 well-developed sentences/points on the THIRD major dimension (e.g., solutions/way forward/international examples). Same stylistic requirement.")
    lines.append("")
    lines.append("### CONCLUSION (3-4 sentences)")
    lines.append("Synthesize the argument with a forward-looking, authoritative closing statement. Avoid simply repeating the body; instead, elevate the argument with a call to action or a broader implication.")
    lines.append("")
    lines.append("STYLE RULES:")
    lines.append("- Use advanced, exam-impressive vocabulary (e.g., 'exacerbate', 'underpin', 'galvanize', 'inextricably linked', 'notwithstanding', 'in tandem with') naturally, not forcibly.")
    lines.append("- Vary sentence openings and lengths; avoid starting every sentence with the subject.")
    lines.append("- Use at least one of these clause types in every sentence where natural: relative clause (which/who/that), subordinate clause (although/since/given that), participial phrase (having done X), or cleft sentence (It is X that...).")
    lines.append("- Do NOT invent fake institutions, laws, or statistics. If unsure, use general but accurate phrasing.")
    lines.append("- Maintain formal, academic register throughout, suitable for a competitive civil service exam.")
    lines.append("")
    lines.append("After the essay, add this section:")
    lines.append("")
    lines.append("### Vocabulary & Clause Bank (for self-study)")
    lines.append("- List 8-10 advanced words/phrases used above with a one-line meaning each")
    lines.append("- List 4-5 clause/sentence patterns used above with a short label (e.g., 'Relative clause: ...')")
    return "\n".join(lines)

# ==================================================
# GENERATE FUNCTION
# ==================================================

def generate(model, prompt):
    response = model.generate_content(prompt)
    if response is None:
        raise ValueError("Gemini থেকে কোনো response পাওয়া যায়নি")
    if not hasattr(response, "text"):
        raise ValueError("Gemini response-এ text নেই")
    if not response.text:
        raise ValueError("Gemini থেকে খালি response এসেছে")
    return response.text