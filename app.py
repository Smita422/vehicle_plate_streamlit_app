import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration, WebRtcMode
import av
from detect_plate import detect_plate_from_frame
from streamlit_webrtc import WebRtcMode

st.title("🚗 Live Number Plate Detection (EasyOCR)")
st.markdown("This app detects vehicle plates using your browser's webcam.")

RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class PlateProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        processed_img = detect_plate_from_frame(img)
        return av.VideoFrame.from_ndarray(processed_img, format="bgr24")

webrtc_streamer(
    key="vehicle-detection",
    mode=WebRtcMode.SENDRECV,  # ✅ Add this line!
    video_processor_factory=PlateProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
