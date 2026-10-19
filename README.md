# Website Lộc Minh Anh (LMA)

Website tĩnh nhiều trang cho công ty tổng thầu xây dựng Lộc Minh Anh. HTML5 + CSS + JavaScript thuần, không framework, không bước build. Mở `index.html` là chạy.

## Cấu trúc
```
index.html            Trang chủ
gioi-thieu.html       Giới thiệu
dich-vu.html          Dịch vụ (tổng quan + 6 dịch vụ chi tiết)
du-an.html            Dự án (bộ lọc) + nhật ký công trường
du-an/*.html          6 trang chi tiết dự án mẫu
quy-trinh.html        Quy trình và cam kết
tin-tuc.html          Blog, bài viết trong tin-tuc/
tuyen-dung.html  lien-he.html  404.html
style.css  script.js  sitemap.xml  robots.txt
assets/img/           Logo, favicon, ảnh OG, ảnh công trường
tools/build.py        (tùy chọn) sinh lại toàn bộ HTML từ một nơi
```

## Việc cần làm trước khi chạy thật
1. **Thông tin liên hệ**: mở `script.js`, điền khối `LMA` ở đầu file (hotline, Zalo, email, địa chỉ, giờ làm việc, Facebook, bản đồ). Toàn site tự cập nhật; nút gọi nhanh và Zalo trên di động hoạt động ngay.
2. **Form báo giá**: tạo form tại [Formspree](https://formspree.io), dán URL vào `LMA.formEndpoint`. Khi để trống, form chỉ kiểm tra dữ liệu và hiện thông báo "chế độ xem thử", không gửi đi.
3. **Bản đồ**: Google Maps > Chia sẻ > Nhúng bản đồ, dán phần `src` vào `LMA.mapEmbed`.
4. **Tên miền**: đổi `BASE` trong `tools/build.py` (và chạy lại), hoặc thay URL trong `sitemap.xml`, `robots.txt`, thẻ canonical/OG nếu dùng tên miền riêng.
5. **Nội dung giữ chỗ** dạng `[cập nhật]`: số liệu, mã số thuế, năm thành lập, đội ngũ, dự án mẫu (`du-an/*.html`), lời chứng thực mẫu. Không có số liệu nào được tự đặt.
6. **Schema.org** (`GeneralContractor`): thêm `telephone`, `address` đầy đủ vào JSON-LD khi có thông tin.

## Triển khai
- **GitHub Pages**: Settings > Pages > Source: `main` / `/ (root)`. Site chạy tại `https://huyvo92vn.github.io/LOCMINHANH/` (toàn bộ đường dẫn là tương đối nên chạy được ở thư mục con).
- **Netlify / Cloudflare Pages / hosting thường**: kéo thả hoặc upload cả thư mục, không cần cấu hình build.

## Sửa header/footer/nội dung chung
Chạy `python3 tools/build.py` sau khi sửa dữ liệu trong file đó (cần Python 3). Hoặc sửa trực tiếp từng file HTML.

## Thương hiệu
Màu, font ở biến CSS đầu `style.css`. Font Be Vietnam Pro tải từ Google Fonts, dự phòng Arial. Logo dùng nguyên bản (chỉ cắt khoảng trắng thừa); header dùng biểu tượng LMA kèm chữ vì logo đầy đủ nhỏ hơn 120px, dưới mức tối thiểu của Brand Kit.
