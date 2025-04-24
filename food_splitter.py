import streamlit as st
from collections import defaultdict

st.title("🍛 แบ่งค่าอาหารกับเพื่อนๆ")

# ใช้ session_state เพื่อเก็บเมนูระหว่างการใช้งาน
if "menu_items" not in st.session_state:
    st.session_state.menu_items = []

st.header("เพิ่มเมนูอาหาร")

menu_name = st.text_input("ชื่อเมนู")
menu_price = st.number_input("ราคา", min_value=0.0, step=1.0)
people_raw = st.text_input("ชื่อคนที่แชร์เมนูนี้ (คั่นด้วย , เช่น เก๋า,ฝ้าย,บีม)")

if st.button("เพิ่มเมนู"):
    if menu_name and people_raw:
        shared_by = [name.strip() for name in people_raw.split(",")]
        st.session_state.menu_items.append({
            "name": menu_name,
            "price": menu_price,
            "shared_by": shared_by
        })
        st.success(f"เพิ่มเมนู '{menu_name}' แล้ว!")
    else:
        st.warning("กรอกชื่อเมนูและคนที่กินด้วยน้าา~")

# แสดงรายการทั้งหมดที่กรอก
if st.session_state.menu_items:
    st.header("📋 รายการที่เพิ่ม")
    for item in st.session_state.menu_items:
        st.write(f"- {item['name']} ({item['price']} บาท) แชร์โดย {', '.join(item['shared_by'])}")

    st.header("📊 สรุปค่าใช้จ่ายแต่ละคน")

    payments = defaultdict(float)
    for item in st.session_state.menu_items:
        share_price = item["price"] / len(item["shared_by"])
        for person in item["shared_by"]:
            payments[person] += share_price

    for person, total in payments.items():
        st.write(f"👉 {person} ต้องจ่าย: {total:.2f} บาท")
