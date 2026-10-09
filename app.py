import streamlit as st
import google.generativeai as genai
import json
import datetime
import os
import random

from utils.extractor import extract_text_from_pdf, extract_text_from_url
from utils.retriever import load_institutions, retrieve_relevant
from utils.gemini_helper import (
    prompt_topic_breakdown,
    prompt_bd_law_mapping,
    prompt_constitution,
    prompt_international_law,
    prompt_comparative_countries,
    prompt_government_response,
    prompt_final_synthesis,
    build_enhance_prompt,
    prompt_hook_essay,
    generate,
)

st.set_page_config(page_title="BCS Master Note Generator", layout="wide", page_icon="📘")
st.title("📘 BCS Master Note Generator")
st.caption("টপিক/আর্টিকেল/PDF/URL দাও এবং সম্পূর্ণ গবেষণাধর্মী Master Note পাও")


def init_session():
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = ""
    if "sections" not in st.session_state:
        st.session_state.sections = {}
    if "final_note" not in st.session_state:
        st.session_state.final_note = ""


init_session()

if not st.session_state.api_key:
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    st.session_state.api_key = default_key


# ================= SIDEBAR: API KEY =================
st.sidebar.header("🔑 API Settings")
new_key = st.sidebar.text_input("Gemini API Key", type="password", value=st.session_state.api_key)

apply_col, test_col = st.sidebar.columns(2)

apply_clicked = apply_col.button("✅ Apply", use_container_width=True)
if apply_clicked:
    st.session_state.api_key = new_key
    st.sidebar.success("আপডেট হয়েছে")

test_clicked = test_col.button("🧪 Test", use_container_width=True)
if test_clicked:
    try:
        genai.configure(api_key=new_key)
        test_model = genai.GenerativeModel("gemini-3.5-flash-lite")
        test_model.generate_content("Hi")
        st.sidebar.success("✅ কাজ করছে")
    except Exception as e:
        st.sidebar.error("❌ " + str(e)[:120])

api_key = st.session_state.api_key


# ================= SIDEBAR: MODEL =================
st.sidebar.header("🤖 Model")

MODEL_OPTIONS = {
    "Gemini 3.5 Flash-Lite (recommended)": "gemini-3.5-flash-lite",
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Custom": "custom"
}

sel_label = st.sidebar.selectbox("মডেল সিলেক্ট করো", list(MODEL_OPTIONS.keys()))
model_choice = MODEL_OPTIONS[sel_label]

if model_choice == "custom":
    model_name = st.sidebar.text_input("Custom model name", "gemini-3.5-flash-lite")
else:
    model_name = model_choice

st.sidebar.caption("ব্যবহৃত হবে: " + model_name)


# ================= SIDEBAR: MODE =================
st.sidebar.header("✍️ মোড")

app_mode = st.sidebar.radio(
    "কী করতে চাও?",
    ["Master Note (সম্পূর্ণ বিশ্লেষণ)", "Quick Enhance (দ্রুত)", "English Hook Essay (Hook+4+4+4+Conclusion)"]
)

length_mode = st.sidebar.selectbox("দৈর্ঘ্য (Quick Enhance মোডে)", ["short", "medium", "long"], index=1)


# ================= LOAD INSTITUTIONS =================
try:
    institutions = load_institutions()
except Exception:
    institutions = []


# ================= INPUT AREA =================
st.subheader("📝 ইনপুট দাও")
input_type = st.radio("টাইপ", ["Text", "PDF", "URL"], horizontal=True)
user_text = ""

if input_type == "Text":
    user_text = st.text_area("টপিক/আর্টিকেল লেখো", height=180)

if input_type == "PDF":
    uploaded_pdf = st.file_uploader("PDF আপলোড করো", type=["pdf"])
    if uploaded_pdf is not None:
        extracted_pdf = extract_text_from_pdf(uploaded_pdf)
        is_valid_pdf = extracted_pdf and not extracted_pdf.startswith("Error")
        if is_valid_pdf:
            user_text = extracted_pdf
            st.text_area("Extracted Text", user_text, height=180)
        if not is_valid_pdf:
            st.error("PDF থেকে টেক্সট পাওয়া যায়নি")

if input_type == "URL":
    url_input = st.text_input("URL দাও")
    extract_clicked = st.button("🔗 Extract")
    if extract_clicked:
        url_is_valid = url_input and url_input.strip() != ""
        if url_is_valid:
            with st.spinner("Extracting..."):
                extracted_url = extract_text_from_url(url_input)
            extraction_ok = extracted_url and not extracted_url.startswith("Error")
            if extraction_ok:
                st.session_state.extracted_text = extracted_url
                st.success("সফল হয়েছে")
            if not extraction_ok:
                st.error("Extract করা যায়নি: " + str(extracted_url))
        if not url_is_valid:
            st.error("একটা URL দাও")

    if st.session_state.extracted_text:
        user_text = st.session_state.extracted_text
        st.text_area("Extracted Text", user_text, height=180)


st.markdown("---")


# ================= HELPER FUNCTIONS =================
def inputs_are_valid():
    if not api_key.strip():
        st.error("Sidebar-এ API Key দিয়ে Apply করো")
        return False
    if not model_name.strip():
        st.error("Model নাম দাও")
        return False
    if not user_text.strip():
        st.error("টপিক/টেক্সট দাও")
        return False
    return True


def safe_generate(model, prompt, step_name):
    try:
        output = generate(model, prompt)
        return output
    except Exception as e:
        error_text = str(e)
        st.warning(step_name + " জেনারেট করতে সমস্যা হয়েছে: " + error_text[:150])
        return "(" + step_name + " তৈরি করা যায়নি)"


# ================= MODE 1: MASTER NOTE =================
if app_mode == "Master Note (সম্পূর্ণ বিশ্লেষণ)":

    generate_clicked = st.button("🚀 Master Note তৈরি করো", type="primary", use_container_width=True)

    if generate_clicked:
        valid = inputs_are_valid()
        if valid:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            relevant = retrieve_relevant(user_text, institutions)

            progress_bar = st.progress(0, text="শুরু হচ্ছে...")
            sections = {}

            step_list = [
                ("breakdown", "বিষয় বিশ্লেষণ", prompt_topic_breakdown(user_text)),
                ("law", "বাংলাদেশের আইন ম্যাপিং", prompt_bd_law_mapping(user_text, relevant)),
                ("constitution", "সংবিধান বিশ্লেষণ", prompt_constitution(user_text)),
                ("intl_law", "আন্তর্জাতিক আইন ও তত্ত্ব", prompt_international_law(user_text)),
                ("comparative", "আন্তর্জাতিক দৃষ্টান্ত", prompt_comparative_countries(user_text)),
                ("govt", "সরকারের পদক্ষেপ", prompt_government_response(user_text, relevant)),
            ]

            total_steps = len(step_list) + 1
            current_step = 0

            for step_key, step_label, step_prompt in step_list:
                progress_fraction = current_step / total_steps
                progress_bar.progress(progress_fraction, text="জেনারেট হচ্ছে: " + step_label)
                sections[step_key] = safe_generate(model, step_prompt, step_label)
                current_step = current_step + 1

            progress_bar.progress(current_step / total_steps, text="Final Summary তৈরি হচ্ছে...")
            combined_text = "\n\n".join(sections.values())
            synthesis_prompt = prompt_final_synthesis(user_text, combined_text)
            synthesis_result = safe_generate(model, synthesis_prompt, "Final Synthesis")

            progress_bar.progress(1.0, text="সম্পন্ন!")

            final_note = "# 📘 Master Note\n\n"
            final_note = final_note + synthesis_result + "\n\n---\n\n"
            final_note = final_note + sections.get("breakdown", "") + "\n\n---\n\n"
            final_note = final_note + sections.get("law", "") + "\n\n---\n\n"
            final_note = final_note + sections.get("constitution", "") + "\n\n---\n\n"
            final_note = final_note + sections.get("intl_law", "") + "\n\n---\n\n"
            final_note = final_note + sections.get("comparative", "") + "\n\n---\n\n"
            final_note = final_note + sections.get("govt", "")

            st.session_state.sections = sections
            st.session_state.final_note = final_note

    if st.session_state.final_note:
        st.success("Master Note তৈরি হয়েছে")

        tab_names = ["সম্পূর্ণ Note", "বিষয় বিশ্লেষণ", "আইন", "সংবিধান",
                     "আন্তর্জাতিক আইন", "দেশের দৃষ্টান্ত", "সরকারের পদক্ষেপ"]
        tabs = st.tabs(tab_names)

        with tabs[0]:
            st.markdown(st.session_state.final_note)
            file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                "📥 Master Note ডাউনলোড করো",
                st.session_state.final_note,
                file_name="master_note_" + file_timestamp + ".md",
                mime="text/markdown"
            )

        section_keys = ["breakdown", "law", "constitution", "intl_law", "comparative", "govt"]
        tab_index = 1
        for key in section_keys:
            with tabs[tab_index]:
                content = st.session_state.sections.get(key, "কিছু পাওয়া যায়নি")
                st.markdown(content)
            tab_index = tab_index + 1


# ================= MODE 2: QUICK ENHANCE =================
if app_mode == "Quick Enhance (দ্রুত)":

    enhance_clicked = st.button("✨ Enhance করো", type="primary", use_container_width=True)

    if enhance_clicked:
        valid = inputs_are_valid()
        if valid:
            with st.spinner("Generating..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name)
                    relevant = retrieve_relevant(user_text, institutions)
                    prompt = build_enhance_prompt(user_text, relevant, length_mode)
                    result = generate(model, prompt)
                    st.markdown(result)
                    st.download_button("📥 Download", result, file_name="enhanced.txt")
                except Exception as e:
                    st.error("Error: " + str(e))
# ================= MODE 3: ENGLISH HOOK ESSAY =================
if app_mode == "English Hook Essay (Hook+4+4+4+Conclusion)":

    st.info("এই মোড Hook + 4 points + 4 points + 4 points + Conclusion স্টাইলে sophisticated vocabulary ও clause ব্যবহার করে একটা exam-ready English essay তৈরি করবে।")

    hook_essay_clicked = st.button("✍️ Hook Essay তৈরি করো", type="primary", use_container_width=True)

    if hook_essay_clicked:
        valid = inputs_are_valid()
        if valid:
            with st.spinner("Crafting your essay with sophisticated vocabulary..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name)
                    relevant = retrieve_relevant(user_text, institutions)
                    essay_prompt = prompt_hook_essay(user_text, relevant)
                    essay_result = generate(model, essay_prompt)
                    st.markdown(essay_result)

                    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        "📥 Download Essay",
                        essay_result,
                        file_name="hook_essay_" + file_timestamp + ".txt",
                        mime="text/plain"
                    )

                    try:
                        entry = {
                            "time": str(datetime.datetime.now()),
                            "mode": "hook_essay",
                            "input": user_text[:1500],
                            "output": essay_result
                        }
                        history = []
                        if os.path.exists("history.json"):
                            history = json.load(open("history.json", encoding="utf-8"))
                        history.append(entry)
                        json.dump(history, open("history.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                    except Exception:
                        pass

                except Exception as e:
                    st.error("Error: " + str(e))

# ================= SIDEBAR EXTRAS =================
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Flashcard Practice")

flashcard_clicked = st.sidebar.button("🎲 Random প্রতিষ্ঠান")
if flashcard_clicked and institutions:
    random_inst = random.choice(institutions)
    inst_name = random_inst.get("name_bn", "")
    inst_abbr = random_inst.get("abbr", "")
    inst_role = random_inst.get("role", "")
    st.sidebar.markdown("**" + inst_name + " (" + inst_abbr + ")**")
    st.sidebar.write(inst_role)

st.sidebar.markdown("---")
clear_clicked = st.sidebar.button("🗑️ History ক্লিয়ার")
if clear_clicked:
    if os.path.exists("history.json"):
        os.remove("history.json")
    st.sidebar.success("মুছে ফেলা হয়েছে")