import streamlit as st
import os
import timm
import torch
from torchvision import transforms
from PIL import Image

st.title("Cats and Dogs Classification")
uploaded_image = st.file_uploader("upload  image file to predict")

transform = transforms.Compose([transforms.Resize((224, 224)),
                               transforms.ToTensor(),
                               transforms.Normalize([0.5]*3, [0.5]*3)])


def load_model():
    model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=False, num_classes=2)
    state_dict = torch.load('swin_model.pth', map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    return model

model = load_model()
if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image=image, caption="Uploaded Image", use_column_width=True)

    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    class_names = ['Cat', 'Dog']
    st.subheader(f'Prediction: {class_names[pred]} {probs[0][pred]*100:.2f}%')

st.markdown("-------")
st.subheader("Author: Sazid")