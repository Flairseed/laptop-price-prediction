import streamlit as st
import pandas as pd
import joblib

@st.cache_resource
def load_model():
    return joblib.load("GradientBoosting.pkl")

@st.cache_resource
def load_predictions():
    return [0, 0]

with st.sidebar:
    with st.form("features_form"):
        st.header("Input the parameters")

        cpu_freq = st.slider("CPU Frequency (GHZ)", 0.9, 3.6)
        ram = st.select_slider("RAM (GB)", [ 2, 4, 6, 8, 12, 16, 24, 32, 64])
        weight = st.slider("Weight (kg)", 0.7, 4.7)
        storage_1_size = st.select_slider("Storage 1 Size (GB)", [8, 16, 32, 64, 128, 180, 240, 256, 500, 508, 512, 1000, 2000])
        storage_type = st.radio("Storage 1 Type", ['HDD', 'SSD', 'Others'])
        storage_2_size = st.select_slider("Storage 2 Size (GB)", [0, 256, 500, 512, 1000, 2000])
        res = st.selectbox("Resolution", ["1366x768", "1440x900", "1600x900", "1920x1080", "1920x1200", "2160x1440", "2304x1440", "2256x1504", "2400x1600", "2560x1440", "2560x1600", "2736x1824", "2880x1800", "3200x1800", "3840x2160"])
        touchscreen = st.toggle("Touchscreen")
        ips = st.toggle("IPS Panel Display")
        is_intel = st.toggle("CPU Company Intel")
        gpu = st.radio("GPU Company", ['Intel', 'Nvidia', 'Others'])
        company = st.selectbox("Company", ['Acer', 'Asus', 'Dell', 'HP', 'Lenovo', 'Others'])
        opsys = st.selectbox("Operating System", ['Windows 10 Systems', 'Windows 7', 'Others'])
        type = st.selectbox("Type Name", ['Notebook', 'Ultrabook', 'Workstation', 'Others'])

        raw_inputs = pd.DataFrame({
            "CPU Frequency (GHZ)": [cpu_freq],
            "RAM (GB)": [ram],
            "Weight (kg)": [weight],
            "Storage 1 Size (GB)": [storage_1_size],
            "Storage 1 Type": [storage_type],
            "Storage 2 Size (GB)": [storage_2_size],
            "Resolution": [res],
            "Touchscreen": [touchscreen],
            "IPS Panel Display": [ips],
            "CPU Company Intel": [is_intel],
            "GPU Company": [gpu],
            "Company": [company],
            "Operating System": [opsys],
            "Type Name": [type]
            })

        dimensions = res.split("x")
        pixels = int(dimensions[0]) * int(dimensions[1])

        acer = False
        asus = False
        dell = False
        hp = False
        lenovo = False
        others_company = False
        if company == "Acer":
            acer = True
        elif company == "Asus":
            asus = True
        elif company == "Dell":
            dell = True
        elif company == "HP":
            hp = True
        elif company == "Lenovo":
            lenovo = True
        else:
            others_company = True
        
        intel = False
        nvidia = False
        others_gpu = False
        if gpu == "Intel":
            intel = True
        elif gpu == "Nvidia":
            nvidia = True
        else:
            others_gpu = True        

        others_opsys = False
        windows_10 = False
        windows_7 = False
        if opsys == "Windows 10 Systems":
            windows_10 = True
        elif opsys == "Windows 7":
            windows_7 = True
        else:
            others_opsys = True
        
        notebook = False
        ultrabook = False
        workstation = False
        others_type = False
        if type == "Notebook":
            notebook = True
        elif type == "Ultrabook":
            ultrabook = True
        elif type == "Workstation":
            workstation = True
        else:
            others_type = True

        hdd = False
        others_storage_type = False
        ssd = False
        if storage_type == "HDD":
            hdd = True
        elif storage_type == "SSD":
            ssd = True
        else:
            others_storage_type = True

        features = [
            cpu_freq,
            ram,
            weight,
            storage_1_size,
            storage_2_size,
            touchscreen,
            pixels,
            is_intel,
            acer,
            asus,
            dell,
            hp,
            lenovo,
            others_company,
            intel,
            nvidia,
            others_gpu,
            others_opsys,
            windows_10,
            windows_7,
            notebook,
            ultrabook,
            workstation,
            hdd,
            others_storage_type,
            ssd,
            ips,
            others_type,
        ]

        st.form_submit_button("Predict")

st.title("Laptop Price Prediciton App")
st.header("Predict the price of the laptop based on the specifications on the sidebar.")
st.caption("The model used is a gradient boosting regressor.")

st.divider()

st.subheader("User Inputs:")
st.dataframe(raw_inputs)

st.subheader("Prediction:")
predictions = load_predictions()
predictions[1] = round(load_model().predict([features])[0], 2)
st.metric(label="Price (Euro)", value=f"{predictions[1]} €", delta=f"{round(predictions[1]-predictions[0], 2)} €")
predictions[0] = predictions[1]