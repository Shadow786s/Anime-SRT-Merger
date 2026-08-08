import streamlit as st
import pysrt
from moviepy.editor import VideoFileClip
import os
import tempfile

st.set_page_config(page_title="Video & SRT Merger", page_icon="🎬")

st.title("🎬 Multi-Video & SRT Merger")
st.write("अपने वीडियो और SRT फाइल्स को लाइन से अपलोड करें।")

# फाइल अपलोड करने का ऑप्शन
videos = st.file_uploader("यहाँ सभी Video फाइल्स अपलोड करें (mp4)", type=['mp4'], accept_multiple_files=True)
srts = st.file_uploader("यहाँ सभी SRT फाइल्स अपलोड करें (.srt)", type=['srt'], accept_multiple_files=True)

if st.button("Merge Files"):
    if len(videos) != len(srts):
        st.error("❌ वीडियो और SRT फाइल्स की गिनती बराबर होनी चाहिए! (जैसे 3 वीडियो तो 3 SRT)")
    elif len(videos) > 0:
        st.info("⏳ प्रोसेसिंग चालू है... कृपया इंतज़ार करें। (बड़े वीडियो में समय लग सकता है)")
        
        try:
            # एक टेम्पररी फोल्डर बनाएँ जहाँ काम होगा
            temp_dir = tempfile.mkdtemp()
            final_srt = pysrt.SubRipFile()
            current_time_offset = 0.0

            for i in range(len(videos)):
                # फाइल्स को सिस्टम में सेव करें ताकि कोड उन्हें पढ़ सके
                video_path = os.path.join(temp_dir, videos[i].name)
                srt_path = os.path.join(temp_dir, srts[i].name)
                
                with open(video_path, "wb") as f:
                    f.write(videos[i].read())
                with open(srt_path, "wb") as f:
                    f.write(srts[i].read())

                # SRT फाइल ओपन करें
                subs = pysrt.open(srt_path)
                
                # टाइम शिफ्ट करें
                if current_time_offset > 0:
                    subs.shift(seconds=current_time_offset)
                
                for sub in subs:
                    final_srt.append(sub)

                # वीडियो की लंबाई (Duration) निकालें
                clip = VideoFileClip(video_path)
                current_time_offset += clip.duration
                clip.close()

            # फाइनल SRT सेव करें
            output_srt_path = os.path.join(temp_dir, "Final_Merged_Subtitles.srt")
            final_srt.save(output_srt_path, encoding='utf-8')

            st.success("✅ SRT मर्जर पूरा हो गया!")
            
            # डाउनलोड बटन दें
            with open(output_srt_path, "rb") as f:
                st.download_button(
                    label="⬇️ Final SRT फाइल डाउनलोड करें",
                    data=f,
                    file_name="Final_Merged_Subtitles.srt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"कुछ गलती हो गई: {e}")
