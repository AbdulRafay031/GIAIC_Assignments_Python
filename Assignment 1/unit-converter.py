import streamlit as st

def convert_length(value, from_unit, to_unit):
    units = {
        'Meter': 1,
        'Kilometer': 1000,
        'Mile': 1609.34,
        'Foot': 0.3048
    }
    return value * units[from_unit] / units[to_unit]

def convert_weight(value, from_unit, to_unit):
    units = {
        'Gram': 1,
        'Kilogram': 1000,
        'Pound': 453.592,
        'Ounce': 28.3495
    }
    return value * units[from_unit] / units[to_unit]

def convert_temperature(value, from_unit, to_unit):
    result = None
    if from_unit == 'Celsius':
        if to_unit == 'Fahrenheit':
            result = (value * 9/5) + 32
        elif to_unit == 'Kelvin':
            result = value + 273.15
    elif from_unit == 'Fahrenheit':
        if to_unit == 'Celsius':
            result = (value - 32) * 5/9
        elif to_unit == 'Kelvin':
            result = (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin':
        if to_unit == 'Celsius':
            result = value - 273.15
        elif to_unit == 'Fahrenheit':
            result = (value - 273.15) * 9/5 + 32
    return result

def convert_volume(value, from_unit, to_unit):
    units = {
        'Liter': 1,
        'Milliliter': 0.001,
        'Gallon': 3.78541,
        'Cup': 0.24
    }
    return value * units[from_unit] / units[to_unit]

# ------------------ Streamlit App ------------------ #

st.set_page_config(page_title="Unit Converter", page_icon="🔁")
st.title("🔁 Universal Unit Converter")

category = st.selectbox("Choose a category:", ["Length", "Weight", "Temperature", "Volume"])

if category == "Length":
    units = ['Meter', 'Kilometer', 'Mile', 'Foot']
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    value = st.number_input(f"Enter value in {from_unit}:", min_value=0.0, format="%.4f")
    if st.button("Convert Length"):
        result = convert_length(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

elif category == "Weight":
    units = ['Gram', 'Kilogram', 'Pound', 'Ounce']
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    value = st.number_input(f"Enter value in {from_unit}:", min_value=0.0, format="%.4f")
    if st.button("Convert Weight"):
        result = convert_weight(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

elif category == "Temperature":
    units = ['Celsius', 'Fahrenheit', 'Kelvin']
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    value = st.number_input(f"Enter temperature in {from_unit}:", format="%.2f")
    if st.button("Convert Temperature"):
        result = convert_temperature(value, from_unit, to_unit)
        if result is not None:
            st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")
        else:
            st.error("Invalid conversion selected.")

elif category == "Volume":
    units = ['Liter', 'Milliliter', 'Gallon', 'Cup']
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    value = st.number_input(f"Enter value in {from_unit}:", min_value=0.0, format="%.4f")
    if st.button("Convert Volume"):
        result = convert_volume(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
