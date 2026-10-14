
import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="VISION Smart Classroom Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 VISION Smart Classroom Assistant")
st.caption("Teacher Control Center | MDP Project")

# Session values
if "saved_notes" not in st.session_state:
    st.session_state.saved_notes = 0

# Sidebar
st.sidebar.header("Class Controls")

teacher = st.sidebar.text_input(
    "Teacher Name", "Demo Teacher"
)

course = st.sidebar.text_input(
    "Course Name", "CSE - AI & Robotics"
)

attendance = st.sidebar.number_input(
    "Students Present",
    min_value=0,
    max_value=200,
    value=32
)

# Dashboard metrics
c1, c2, c3, c4 = st.columns(4)

c1.metric("Students Present", attendance)
c2.metric("Notes Saved", st.session_state.saved_notes)
c3.metric("Camera", "Demo Mode")
c4.metric("Google Drive", "Not Connected")

st.divider()

# Two main sections
left, right = st.columns(2)

with left:
    st.subheader("📷 Classroom Camera")

    classroom_file = st.camera_input(
        "Capture classroom image"
    )

    if classroom_file is None:
        classroom_file = st.file_uploader(
            "Or upload classroom image",
            type=["jpg", "jpeg", "png"]
        )

    classroom = None

    if classroom_file:
        classroom = Image.open(
            classroom_file
        ).convert("RGB")

        st.image(
            classroom,
            caption="Classroom View",
            use_container_width=True
        )

with right:
    st.subheader("📝 Whiteboard Notes")

    board_file = st.file_uploader(
        "Upload whiteboard image",
        type=["jpg", "jpeg", "png"],
        key="board"
    )

    processed = None

    if board_file:
        board = Image.open(board_file).convert("RGB")

        contrast = st.slider(
            "Contrast",
            0.5, 2.5, 1.2, 0.1
        )

        sharpness = st.slider(
            "Sharpness",
            0.5, 3.0, 1.3, 0.1
        )

        processed = ImageEnhance.Contrast(
            board
        ).enhance(contrast)

        processed = ImageEnhance.Sharpness(
            processed
        ).enhance(sharpness)

        st.image(
            processed,
            caption="Enhanced Whiteboard",
            use_container_width=True
        )

        buffer = BytesIO()
        processed.save(buffer, format="PNG")

        st.download_button(
            "⬇️ Download Board Notes",
            data=buffer.getvalue(),
            file_name="board_notes.png",
            mime="image/png"
        )

        if st.button("Save Note"):
            st.session_state.saved_notes += 1
            st.success("Note count updated for this session.")

st.divider()

# Picture-in-Picture preview
st.subheader("🖼️ Picture-in-Picture Preview")

if classroom is not None and processed is not None:
    base = classroom.copy()

    inset = processed.copy()
    inset.thumbnail(
        (base.width // 3, base.height // 3)
    )

    margin = 15
    x = base.width - inset.width - margin
    y = margin

    draw = ImageDraw.Draw(base)
    draw.rectangle(
        [
            x - 4, y - 4,
            x + inset.width + 4,
            y + inset.height + 4
        ],
        fill="white",
        outline="black",
        width=2
    )

    base.paste(inset, (x, y))

    st.image(
        base,
        caption="Classroom with Board Overlay",
        use_container_width=True
    )

    pip_buffer = BytesIO()
    base.save(pip_buffer, format="PNG")

    st.download_button(
        "Download PiP Preview",
        data=pip_buffer.getvalue(),
        file_name="classroom_pip.png",
        mime="image/png"
    )
else:
    st.info(
        "Upload both a classroom image and a "
        "whiteboard image to create the PiP preview."
    )

st.divider()

# Cloud integration placeholder
st.subheader("☁️ Cloud Storage")

st.info(
    "Google Drive integration is not connected yet. "
    "The Google Drive API must be configured for "
    "automatic cloud uploads."
)

st.write("Teacher:", teacher)
st.write("Course:", course)

st.caption(
    "VISION MDP | Application & Cloud Module | "
    + datetime.now().strftime("%d-%m-%Y")
)
