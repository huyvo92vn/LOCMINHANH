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
1. **Thông tin liên hệ**: email `info@locminhanh.com` do chủ dự án cung cấp. Tên pháp lý, MST `0402332326`, địa chỉ đăng ký và điện thoại `0905 677 429` lấy từ [hồ sơ thuế công khai](https://masothue.com/0402332326-cong-ty-tnhh-xay-dung-va-thuong-mai-loc-minh-anh); chủ doanh nghiệp cần xác nhận số này dùng tiếp khách, địa chỉ có tiếp khách hay không. Điền thêm Zalo, giờ làm việc, Facebook và bản đồ khi đã xác minh.
2. **Form báo giá**: email liên hệ `info@locminhanh.com` đã được chủ dự án cung cấp. Email **không tự động là nơi nhận form**. Hiện form chỉ kiểm tra dữ liệu, không gửi đi; trang Liên hệ hiển thị hướng dẫn gửi email trực tiếp. Nếu dùng [Formspree](https://formspree.io) hoặc dịch vụ khác, cấu hình và kiểm thử URL HTTPS tại `LMA.formEndpoint`, thêm thông báo quyền riêng tư về đơn vị xử lý dữ liệu trước khi bật gửi thật.
3. **Bản đồ**: Google Maps > Chia sẻ > Nhúng bản đồ, dán phần `src` vào `LMA.mapEmbed`.
4. **Tên miền**: đổi `BASE` trong `tools/build.py` (và chạy lại), hoặc thay URL trong `sitemap.xml`, `robots.txt`, thẻ canonical/OG nếu dùng tên miền riêng.
5. **Hình minh họa**: sáu SVG tự tạo mô tả loại công trình có thể tư vấn, không phải ảnh công trình đã thi công. Trang chi tiết minh họa (`du-an/*.html`) có `noindex`, không nằm trong sitemap. Ảnh công đoạn thi công JPEG cần xác minh tác giả, quyền sử dụng và nguồn gốc trước khi gắn với dự án thật. Không tự đặt số dự án, chứng chỉ hoặc danh tính đội ngũ.
6. **Schema.org** (`GeneralContractor`): tên pháp lý, MST, điện thoại, địa chỉ đăng ký và email đã được cập nhật; xác nhận quyền sử dụng số điện thoại làm kênh tư vấn trước khi triển khai rộng.

## Triển khai
- **GitHub Pages**: sau khi repository được tạo và mã được đẩy lên, Settings > Pages > Source: `main` / `/ (root)`. Mặc định URL là `https://huyvo92vn.github.io/LOCMINHANH/` (toàn bộ đường dẫn là tương đối nên chạy được ở thư mục con); cập nhật URL cơ sở nếu dùng tên miền khác.
- **Netlify / Cloudflare Pages / hosting thường**: kéo thả hoặc upload cả thư mục, không cần cấu hình build.

## Sửa header/footer/nội dung chung
Chạy `python3 tools/build.py` sau khi sửa dữ liệu trong file đó (cần Python 3). Hoặc sửa trực tiếp từng file HTML.

## Thương hiệu
Màu, font ở biến CSS đầu `style.css`. Font Be Vietnam Pro tải từ Google Fonts, dự phòng Arial. Logo dùng nguyên bản (chỉ cắt khoảng trắng thừa); header dùng biểu tượng LMA kèm chữ vì logo đầy đủ nhỏ hơn 120px, dưới mức tối thiểu của Brand Kit.
