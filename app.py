import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Công Cụ Tính Lãi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm _ Lưu Quốc Quang")
st.markdown("Nhập thông tin khoản tiền gửi của bạn để tính toán tiền lãi chi tiết.")

st.divider()

# Tạo 2 cột để sắp xếp giao diện nhập liệu
col1, col2 = st.columns(2)

with col1:
    # 1. Nhập số tiền gửi
    so_tien_gui = st.number_input(
        "1. Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )

    # 2. Nhập kỳ hạn gửi
    ky_han_thang = st.number_input(
        "2. Kỳ hạn gửi (tháng):",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

with col2:
    # 3. Nhập lãi suất (%/năm)
    lai_suat_nam = st.number_input(
        "3. Lãi suất (%/năm):",
        min_value=0.1,
        max_value=20.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

    # 4. Chọn hình thức nhận lãi
    hinh_thuc_nhan_lai = st.selectbox(
        "4. Hình thức nhận lãi:",
        options=[
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý (mỗi 3 tháng)"
        ]
    )

# Tính toán các giá trị
# Công thức chung: Tiền lãi = (Số tiền gửi * Lãi suất năm * Số ngày gửi) / 365
# Hoặc quy đổi quy chuẩn theo tháng/kỳ hạn:
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
    so_lan_nhan_lai = ky_han_thang / 3
    tong_tien_lai = so_tien_gui * lai_suat_thang * ky_han_thang
    nhan_lai_label = "Tiền lãi nhận mỗi quý (3 tháng)"

tong_goc_va_lai = so_tien_gui + tong_tien_lai

st.divider()

# Hiển thị kết quả
st.subheader("📊 Kết Quả Tính Toán")

# Kiểm tra trường hợp đặc biệt cho nhận lãi theo quý
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

    # Chi tiết tóm tắt dạng bảng/hộp thông tin
    st.info(
        f"💡 **Tóm tắt:** Bạn gửi **{so_tien_gui:,.0f} VNĐ** trong **{ky_han_thang} tháng** "
        f"với lãi suất **{lai_suat_nam}%/năm** (hình thức **{hinh_thuc_nhan_lai}**).\n\n"
        f"• Số tiền lãi mỗi kỳ nhận được: **{lai_dinh_ky:,.0f} VNĐ**\n\n"
        f"• Tổng số tiền nhận được khi đáo hạn: **{tong_goc_va_lai:,.0f} VNĐ**"
    )
