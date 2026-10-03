import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Công Cụ Tính Lãi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

# Hiển thị Logo
try:
    st.image("logo.jpg", width=150)
except Exception:
    pass

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm _ Lưu Quốc Quang")
st.markdown("Nhập thông tin khoản tiền gửi của bạn để tính toán tiền lãi chi tiết.")

st.divider()

# BẢNG DỮ LIỆU LÃI SUẤT THAM KHẢO (%/NĂM) CỦA CÁC NGÂN HÀNG
# Dữ liệu theo các mốc kỳ hạn phổ biến: 1, 3, 6, 9, 12, 18, 24, 36 tháng
BANG_LAI_SUAT = {
    "Vietcombank": {1: 1.6, 3: 1.9, 6: 2.9, 9: 2.9, 12: 4.7, 18: 4.7, 24: 4.7, 36: 4.7},
    "BIDV": {1: 1.7, 3: 2.0, 6: 3.0, 9: 3.0, 12: 4.7, 18: 4.7, 24: 4.8, 36: 4.8},
    "VietinBank": {1: 1.7, 3: 2.0, 6: 3.0, 9: 3.0, 12: 4.7, 18: 4.7, 24: 4.8, 36: 4.8},
    "Agribank": {1: 1.7, 3: 2.0, 6: 3.0, 9: 3.0, 12: 4.7, 18: 4.7, 24: 4.8, 36: 4.8},
    "MBBank": {1: 2.3, 3: 2.7, 6: 3.6, 9: 3.7, 12: 4.8, 18: 5.1, 24: 5.6, 36: 5.6},
    "Techcombank": {1: 2.3, 3: 2.6, 6: 3.6, 9: 3.6, 12: 4.6, 18: 4.6, 24: 4.6, 36: 4.6},
    "VPBank": {1: 2.8, 3: 3.1, 6: 4.3, 9: 4.3, 12: 5.0, 18: 5.2, 24: 5.4, 36: 5.4},
    "ACB": {1: 2.3, 3: 2.7, 6: 3.5, 9: 3.7, 12: 4.5, 18: 4.7, 24: 4.7, 36: 4.7},
    "Tự nhập thủ công": {}
}


def get_lai_suat_theo_ky_han(ngan_hang, ky_han):
    """Lấy lãi suất chuẩn hoặc suy ra theo kỳ hạn gần nhất nếu chưa có"""
    rates = BANG_LAI_SUAT.get(ngan_hang, {})
    if not rates:
        return 5.0  # Mặc định nếu không tìm thấy
    
    # Nếu kỳ hạn có sẵn trong bảng
    if ky_han in rates:
        return rates[ky_han]
    
    # Nếu kỳ hạn lẻ, lấy kỳ hạn nhỏ hơn gần nhất trong bảng
    mocs = sorted(rates.keys())
    if ky_han < mocs[0]:
        return rates[mocs[0]]
    for m in reversed(mocs):
        if ky_han >= m:
            return rates[m]
    return rates[mocs[-1]]


# HIỂN THỊ BẢNG LÃI SUẤT THAM KHẢO
with st.expander("📌 Xem Bảng Lãi Suất Tham Khảo Các Ngân Hàng (%/năm)", expanded=False):
    st.markdown("Lãi suất niêm yết dành cho khách hàng cá nhân (gửi tại quầy/online):")
    
    # Chuyển đổi dữ liệu sang định dạng hiển thị bảng
    bang_hien_thi = []
    for nh, rates in BANG_LAI_SUAT.items():
        if nh != "Tự nhập thủ công":
            row = {"Ngân hàng": nh}
            for kh in [1, 3, 6, 9, 12, 18, 24, 36]:
                row[f"{kh}T"] = f"{rates.get(kh, '-')}%"
            bang_hien_thi.append(row)
            
    st.dataframe(bang_hien_thi, use_container_width=True)

st.subheader("📝 Nhập Thông Tin Tiền Gửi")

# Tạo 2 cột nhập liệu
col1, col2 = st.columns(2)

with col1:
    # 1. Chọn Ngân hàng
    ngan_hang_chon = st.selectbox(
        "1. Chọn Ngân hàng gửi:",
        options=list(BANG_LAI_SUAT.keys())
    )

    # 2. Nhập số tiền gửi
    so_tien_gui = st.number_input(
        "2. Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )

    # 3. Nhập kỳ hạn gửi
    ky_han_thang = st.number_input(
        "3. Kỳ hạn gửi (tháng):",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

with col2:
    # Tự động tra cứu lãi suất dựa trên ngân hàng và kỳ hạn đã chọn
    lai_suat_tu_dong = get_lai_suat_theo_ky_han(ngan_hang_chon, ky_han_thang)

    # 4. Nhập / Tự động tính Lãi suất (%/năm)
    if ngan_hang_chon == "Tự nhập thủ công":
        lai_suat_nam = st.number_input(
            "4. Lãi suất (%/năm):",
            min_value=0.1,
            max_value=20.0,
            value=6.0,
            step=0.1,
            format="%.2f"
        )
    else:
        # Cho phép chỉnh sửa lại nếu muốn, mặc định lấy lãi suất tự động
        lai_suat_nam = st.number_input(
            f"4. Lãi suất (%/năm) [Tự động từ {ngan_hang_chon}]:",
            min_value=0.1,
            max_value=20.0,
            value=float(lai_suat_tu_dong),
            step=0.1,
            format="%.2f"
        )

    # 5. Chọn hình thức nhận lãi
    hinh_thuc_nhan_lai = st.selectbox(
        "5. Hình thức nhận lãi:",
        options=[
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý (mỗi 3 tháng)"
        ]
    )

# --- TÍNH TOÁN KẾT QUẢ ---
lai_suat_thang = (lai_suat_nam / 100) / 12

if hinh_thuc_nhan_lai == "Cuối kỳ":
    tong_tien_lai = so_tien_gui * lai_suat_thang * ky_han_thang
    lai_dinh_ky = tong_tien_lai  # Nhận 1 lần vào cuối kỳ
    nhan_lai_label = "Tiền lãi nhận cuối kỳ"

elif hinh_thuc_nhan_lai == "Hàng tháng":
    lai_dinh_ky = so_tien_gui * lai_suat_thang
    tong_tien_lai = lai_dinh_ky * ky_han_thang
    nhan_lai_label = "Tiền lãi nhận hàng tháng"

elif hinh_thuc_nhan_lai == "Hàng quý (mỗi 3 tháng)":
    lai_dinh_ky = so_tien_gui * lai_suat_thang * 3
    tong_tien_lai = so_tien_gui * lai_suat_thang * ky_han_thang
    nhan_lai_label = "Tiền lãi nhận mỗi quý (3 tháng)"

tong_goc_va_lai = so_tien_gui + tong_tien_lai

st.divider()

# --- HIỂN THỊ KẾT QUẢ ---
st.subheader("📊 Kết Quả Tính Toán")

if hinh_thuc_nhan_lai == "Hàng quý (mỗi 3 tháng)" and ky_han_thang < 3:
    st.warning("⚠️ Kỳ hạn nhỏ hơn 3 tháng nên không thể áp dụng hình thức nhận lãi hàng quý.")
else:
    # Hiển thị dạng Metric
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(
            label=nhan_lai_label,
            value=f"{lai_dinh_ky:,.0f} VNĐ"
        )
        st.metric(
            label="Tổng tiền lãi nhận được",
            value=f"{tong_tien_lai:,.0f} VNĐ"
        )

    with m_col2:
        st.metric(
            label="Tổng tiền gốc gửi ban đầu",
            value=f"{so_tien_gui:,.0f} VNĐ"
        )
        st.metric(
            label="Tổng Tiền Gốc + Lãi",
            value=f"{tong_goc_va_lai:,.0f} VNĐ"
        )

    # Chi tiết tóm tắt
    ngan_hang_str = f" tại **{ngan_hang_chon}**" if ngan_hang_chon != "Tự nhập thủ công" else ""
    st.info(
        f"💡 **Tóm tắt:** Bạn gửi **{so_tien_gui:,.0f} VNĐ**{ngan_hang_str} trong **{ky_han_thang} tháng** "
        f"với lãi suất **{lai_suat_nam}%/năm** (hình thức **{hinh_thuc_nhan_lai}**).\n\n"
        f"• Số tiền lãi mỗi kỳ nhận được: **{lai_dinh_ky:,.0f} VNĐ**\n\n"
        f"• Tổng số tiền nhận được khi đáo hạn: **{tong_goc_va_lai:,.0f} VNĐ**"
    )
