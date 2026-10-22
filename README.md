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
1. **Thông tin liên hệ**: email `info@locminhanh.com` đã được cung cấp. Mở `script.js` để điền các thông tin thật còn thiếu (hotline, Zalo, địa chỉ, giờ làm việc, Facebook, bản đồ). Toàn site tự cập nhật; nút gọi và Zalo chỉ chuyển sang số thật sau khi cấu hình.
2. **Form báo giá**: email liên hệ `info@locminhanh.com` đã được chủ dự án cung cấp. Email **không tự động là nơi nhận form**. Hiện form chỉ kiểm tra dữ liệu, không gửi đi; trang Liên hệ hiển thị hướng dẫn gửi email trực tiếp. Nếu dùng [Formspree](https://formspree.io) hoặc dịch vụ khác, cấu hình và kiểm thử URL HTTPS tại `LMA.formEndpoint`, thêm thông báo quyền riêng tư về đơn vị xử lý dữ liệu trước khi bật gửi thật.
3. **Bản đồ**: Google Maps > Chia sẻ > Nhúng bản đồ, dán phần `src` vào `LMA.mapEmbed`.
4. **Tên miền**: đổi `BASE` trong `tools/build.py` (và chạy lại), hoặc thay URL trong `sitemap.xml`, `robots.txt`, thẻ canonical/OG nếu dùng tên miền riêng.
5. **Nội dung giữ chỗ** dạng `[cập nhật]`: số liệu, mã số thuế, năm thành lập, đội ngũ, dự án mẫu (`du-an/*.html`). Chỉ công bố dữ liệu thật đã được chủ dự án xác nhận. Các trang chi tiết dự án mẫu có `noindex` và không nằm trong sitemap; bỏ `noindex` khi thay bằng dự án thật. Đã bỏ lời chứng thực giả và danh sách vị trí tuyển dụng mẫu khỏi giao diện.
6. **Schema.org** (`GeneralContractor`): thêm `telephone`, `address` đầy đủ vào JSON-LD khi có thông tin.

## Triển khai
- **GitHub Pages**: sau khi repository được tạo và mã được đẩy lên, Settings > Pages > Source: `main` / `/ (root)`. Mặc định URL là `https://huyvo92vn.github.io/LOCMINHANH/` (toàn bộ đường dẫn là tương đối nên chạy được ở thư mục con); cập nhật URL cơ sở nếu dùng tên miền khác.
- **Netlify / Cloudflare Pages / hosting thường**: kéo thả hoặc upload cả thư mục, không cần cấu hình build.

## Sửa header/footer/nội dung chung
Chạy `python3 tools/build.py` sau khi sửa dữ liệu trong file đó (cần Python 3). Hoặc sửa trực tiếp từng file HTML.

## Thương hiệu
Màu, font ở biến CSS đầu `style.css`. Font Be Vietnam Pro tải từ Google Fonts, dự phòng Arial. Logo dùng nguyên bản (chỉ cắt khoảng trắng thừa); header dùng biểu tượng LMA kèm chữ vì logo đầy đủ nhỏ hơn 120px, dưới mức tối thiểu của Brand Kit.
